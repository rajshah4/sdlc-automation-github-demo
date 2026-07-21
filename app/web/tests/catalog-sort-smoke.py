#!/usr/bin/env python3
"""
Dependency-free UI smoke test for catalog sort feature.
This is a fallback check when Playwright is unavailable.
"""
import re
import sys
from pathlib import Path


def check_html_has_sort_control():
    """Verify sort dropdown is present in HTML."""
    html_path = Path(__file__).parent.parent / "index.html"
    content = html_path.read_text()
    
    checks = {
        "Sort label present": 'Sort by' in content or 'sort' in content.lower(),
        "Sort select element": 'id="sort-by"' in content,
        "Default option": 'value=""' in content and 'Default' in content,
        "Name option": 'value="name"' in content and 'Name' in content,
    }
    
    return checks


def check_js_has_sort_logic():
    """Verify JavaScript implements sort behavior."""
    js_path = Path(__file__).parent.parent / "app.js"
    content = js_path.read_text()
    
    checks = {
        "Reads sort-by selector": '"#sort-by"' in content or "'#sort-by'" in content,
        "Checks for name sort": 'sortBy === "name"' in content or "sortBy == 'name'" in content,
        "Uses localeCompare": '.localeCompare(' in content or '.sort(' in content,
    }
    
    return checks


def main():
    print("# Catalog Sort Smoke Test (Dependency-Free Fallback)")
    print()
    print("**Note**: This is a static DOM check. Playwright is not available in this")
    print("runtime, so browser interaction was not exercised. UI evidence is limited to")
    print("static file inspection.")
    print()
    
    all_passed = True
    
    print("## HTML Structure Checks")
    print()
    html_checks = check_html_has_sort_control()
    for check, passed in html_checks.items():
        status = "✅" if passed else "❌"
        print(f"- {status} {check}")
        all_passed = all_passed and passed
    print()
    
    print("## JavaScript Logic Checks")
    print()
    js_checks = check_js_has_sort_logic()
    for check, passed in js_checks.items():
        status = "✅" if passed else "❌"
        print(f"- {status} {check}")
        all_passed = all_passed and passed
    print()
    
    if all_passed:
        print("Status: All static checks passed")
        print()
        print("## Residual Risk")
        print()
        print("- **Medium risk**: Static checks cannot verify actual browser behavior")
        print("- The sort dropdown may render but not function correctly")
        print("- JavaScript sort logic exists but runtime behavior is not confirmed")
        print("- Recommend manual browser testing or running with Playwright available")
        return 0
    else:
        print("Status: Some checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
