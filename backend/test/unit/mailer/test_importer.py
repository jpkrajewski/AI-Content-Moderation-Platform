from datetime import date

import pytest
from moderation.mailer.templates.importer import TemplateType, get_template


@pytest.mark.parametrize(
    ("template_type", "context"),
    [
        (
            TemplateType.DAILY,
            {
                "report_date": date.today().strftime("%B %d, %Y"),
                "submitted_count": 12,
                "flagged_by_ai_count": 5,
                "moderator_reviewed_count": 10,
                "rejected_count": 2,
                "approved_count": 8,
                "dashboard_url": "https://yourplatform.com/moderation",
            },
        ),
    ],
)
def test_template_rendering(template_type, context):
    template = get_template(template_type)
    rendered = template.render(**context)

    assert context["report_date"] in rendered
    assert str(context["submitted_count"]) in rendered
    assert str(context["flagged_by_ai_count"]) in rendered
    assert context["dashboard_url"] in rendered
