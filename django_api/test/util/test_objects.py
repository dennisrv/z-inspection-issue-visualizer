from src.api.models import Issue
import random
from faker import Faker


class TestObjects:

    fake = Faker()
    rnd = random.Random()

    @classmethod
    def create_issue(cls):
        return Issue(
            title=cls.fake.name(),
            areas=cls.rnd.choices(["Ethical", "Social", "Medical", "Technical", "Regulatory"], k=cls.rnd.randint(1, 5)),
            description=cls.fake.text(),
            issue_type=cls.rnd.choice(["ethical-issue", "flag"]),
            related=cls.rnd.choices([
                {
                    "principle": "Respect for human autonomy",
                    "requirement": "Human agency and oversight",
                    "subRequirement": "Fundamental rights"
                },
                {
                    "principle": "Fairness",
                    "requirement": "Accountability",
                    "subRequirement": "Auditability"
                },
                {
                    "principle": "Explicability",
                    "requirement": "Transparency",
                    "subRequirement": "Explainability"
                },
            ], k=cls.rnd.randint(1, 3))
        )