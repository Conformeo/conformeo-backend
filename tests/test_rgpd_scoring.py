import pytest
from app.services.rgpd_scoring import compute_rgpd_score, RiskLevel

def test_full_conformity():
    answers = {"q1_base_legal": True, "q2_records": True}
    res = compute_rgpd_score(answers)
    assert res["score"] == 100
    assert res["level"] == RiskLevel.ok

def test_partial():
    answers = {"q1_base_legal": True, "q2_records": False}
    res = compute_rgpd_score(answers)
    assert 0 < res["score"] < 100


