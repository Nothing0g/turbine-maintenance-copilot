from turbine_copilot.service import CopilotService

def test_degraded_lp_bearing_requires_review():
    result = CopilotService().diagnosis("LP-BRG-02", hours=24)
    assert result.status == "review_required"
    assert result.human_review_required is True
    assert result.evidence

def test_healthy_hp_bearing_is_not_flagged():
    result = CopilotService().diagnosis("HP-BRG-01", hours=24)
    assert result.status == "normal"
    assert result.human_review_required is False
