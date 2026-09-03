# Design

## Context

The README serves as the primary entry point for understanding the SDLC Automation Demo repository. The introduction section (lines 1-16) establishes what the project is and why it exists. The Petstore app is described on line 10, followed by an explanation of why this simple app works well for demonstrations (lines 11-12).

The sub-agent investigation identified that adding the sentence after line 10 creates the best logical flow: what the app is → what it demonstrates → why that works for demos.

## Decision

- Insert the sentence "The Petstore project is used to demonstrate an event-driven software delivery workflow." after line 10 of README.md
- The sentence becomes part of the existing second paragraph in the introduction
- No special formatting (bold, italics, or code blocks) is needed
- The sentence uses terminology consistent with the README's existing vocabulary: "event-driven" aligns with automation triggers discussed throughout the document

## Risks

- **Low risk**: This is a single-sentence documentation change with no code impact
- **Mitigation**: The change has been validated to align with existing README structure and tone
- **Merge control**: This is explicitly marked as a temporary cache-validation change requiring human approval before merge

## Validation Plan

- Run existing repository validation: `python3 -m pytest -q`
- Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-175-readme-workflow-note/`
- Verify README rendering is correct
- Confirm no application behavior changes
