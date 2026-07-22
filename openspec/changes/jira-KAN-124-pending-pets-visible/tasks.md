# Tasks

## OpenSpec Artifacts
- [x] Create proposal.md with source issue, assumptions, non-goals
- [x] Create specs/catalog/spec.md with requirements and scenarios
- [x] Create design.md with context, decision, risks, validation plan
- [x] Create tasks.md checklist

## Evidence Gathering
- [x] **Stop 1 - Ticket**: Jira KAN-124 - "Customers are seeing pets that are not available"
- [x] **Stop 2 - Wiki/Docs**: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default search must exclude pending pets
- [x] **Stop 3 - Logs**: Checked `docs/logs/pending-pet-visible.ndjson` - confirms PENDING_PET_VISIBLE error with pet-103 (Nova)
- [x] **Stop 4 - Repo/Files**: Analyzed `app/petstore_app/catalog.py` line 50 - identified empty status bypass bug

## Implementation
- [ ] Fix `catalog.py` line 41 to normalize empty status to "available"
- [ ] Add regression test for empty status parameter
- [ ] Run pytest validation
- [ ] Validate OpenSpec artifacts

## PR and Handoff
- [ ] **Stop 5 - Tests/PR**: Create draft PR with evidence waypoints
- [ ] Add `openhands-review` label to PR for automated review
- [ ] Post status update to Jira KAN-124

## Human Control Points
- Human reviews PR
- Human approves merge
- Human controls deployment
