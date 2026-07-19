# Source Adapter Contract v0.1

**Status:** candidate, non-canonical.  
**Parents:** `hummbl-research#67`, `knowledge-as-code#9`, `knowledge-as-code#10`.

The common operations are `discover`, `resolve`, `retrieve`, `snapshot`, `normalize`, `verify`, `cite`, `refresh`, and `delete_or_invalidate`. Each is explicitly `supported`, `unsupported`, `restricted`, or `authorization_gated`; unsupported operations never silently degrade.

Result `status` and `completeness` remain separate. Partial, rate-limited, unauthorized, stale, superseded, deleted, checksum-mismatched, or policy-blocked retrievals cannot masquerade as complete success. Results retain source and adapter identity, exact locators, version, privacy class, license-posture reference, acquisition method, integrity state, transformations, parents, and structured errors.

Private adapters must use the authorized-private data plane and retain that posture downstream. This marker does not replace the policy authority in `governance-as-code#8`.

## Fixture coverage

Five valid structural patterns: scholarly API, versioned repository, archive item, timestamped multimedia, and authorization-gated private connector.

Eight adversarial patterns: partial-as-complete, unsupported success, rate-limit misreporting, stale-as-current, checksum mismatch misreporting, private/public confusion, live validation without a receipt, and receipt arithmetic mismatch.

## Validation

```bash
python3 scripts/validate_adapter_contract.py --self-test fixtures/adapters/adapter-contract-v0.1.fixtures.json
```

Fixture validation does not establish live access, provider approval, rate-limit compliance, or production promotion.
