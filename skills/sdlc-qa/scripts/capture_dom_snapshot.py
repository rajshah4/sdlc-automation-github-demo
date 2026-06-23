#!/usr/bin/env python3
"""Capture a DOM snapshot showing the UI structure."""

from __future__ import annotations

import re
from urllib.request import urlopen


def format_html_snippet(html: str) -> str:
    """Extract and format key parts of the HTML."""
    lines = []
    
    # Extract the toolbar section
    toolbar_match = re.search(r'(<section class="toolbar".*?</section>)', html, re.DOTALL)
    if toolbar_match:
        lines.append("Toolbar Controls:")
        lines.append("=" * 60)
        toolbar = toolbar_match.group(1)
        
        # Extract labels and inputs
        for label_match in re.finditer(r'<label>(.*?)</label>', toolbar, re.DOTALL):
            label_content = label_match.group(1)
            # Clean up whitespace
            label_content = re.sub(r'\s+', ' ', label_content).strip()
            lines.append(f"  • {label_content}")
        
        # Extract button
        button_match = re.search(r'<button[^>]*>(.*?)</button>', toolbar)
        if button_match:
            lines.append(f"  • Button: {button_match.group(1)}")
    
    lines.append("")
    
    # Extract the results section structure
    results_match = re.search(r'(<section>.*?<h2>Available Pets</h2>.*?</section>)', html, re.DOTALL)
    if results_match:
        lines.append("Results Section:")
        lines.append("=" * 60)
        lines.append("  • Heading: Available Pets")
        
        # Check for summary element
        if 'id="result-summary"' in html:
            summary_match = re.search(r'<p id="result-summary"[^>]*>(.*?)</p>', html)
            lines.append(f"  • #result-summary element (class='summary', aria-live='polite')")
        
        # Check for error element
        if 'id="fee-error"' in html:
            error_match = re.search(r'<p id="fee-error"[^>]*>(.*?)</p>', html)
            lines.append(f"  • #fee-error element (class='error', aria-live='polite')")
        
        # Check for results list
        if 'id="results"' in html:
            lines.append(f"  • #results list (class='results')")
    
    return '\n'.join(lines)


def main() -> int:
    url = "http://localhost:4173"
    
    print("=" * 60)
    print("DOM Structure Snapshot")
    print("=" * 60)
    print()
    
    try:
        with urlopen(f"{url}/index.html", timeout=5) as response:
            html = response.read().decode("utf-8")
        
        snapshot = format_html_snippet(html)
        print(snapshot)
        
        print()
        print("=" * 60)
        print("Key UI Elements Present:")
        print("=" * 60)
        
        elements = {
            '#query': 'id="query"' in html,
            '#species': 'id="species"' in html,
            '#max-fee': 'id="max-fee"' in html,
            '#search-button': 'id="search-button"' in html,
            '#result-summary': 'id="result-summary"' in html,
            '#fee-error': 'id="fee-error"' in html,
            '#results': 'id="results"' in html,
        }
        
        for element_id, present in elements.items():
            status = "✓" if present else "✗"
            print(f"  {status} {element_id}")
        
        if all(elements.values()):
            print("\nAll expected UI elements present ✓")
            return 0
        else:
            print("\nSome UI elements missing ✗")
            return 1
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
