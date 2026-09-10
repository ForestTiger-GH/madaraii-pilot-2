from cbr_unified.build import _fingerprints
from cbr_unified.registry import get_source


def test_build_identity_depends_on_source_revision_and_spec_not_timestamps():
    spec = [get_source("mortgage_debt")]
    base = {
        "source_id": "mortgage_debt",
        "source_revision_id": "mortgage_debt@sha256:" + "a" * 64,
        "status": "ok",
    }
    first, spec_sha_1 = _fingerprints([{**base, "acquired_at_utc": "2026-09-11T00:00:00Z"}], spec)
    second, spec_sha_2 = _fingerprints([{**base, "acquired_at_utc": "2026-09-11T01:00:00Z"}], spec)
    changed, spec_sha_3 = _fingerprints(
        [{**base, "source_revision_id": "mortgage_debt@sha256:" + "b" * 64}],
        spec,
    )

    assert first == second
    assert first != changed
    assert spec_sha_1 == spec_sha_2 == spec_sha_3
    assert first.startswith("bld_")
