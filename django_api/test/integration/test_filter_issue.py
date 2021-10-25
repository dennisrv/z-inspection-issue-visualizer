from integration.neo4j_test_case import Neo4jTestCase
from src.api.models import (
    filter_issues,
    Issue,
    SubRequirement,
    KeyRequirement,
    EthicalPrinciple,
)
from util.test_objects import TestObjects


class FilterIssueTest(Neo4jTestCase):

    def test_filter_issue(self):
        related_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in related_issues:
            # ensure issues relate to this
            issue.related = list({v['subRequirement']: v for v in issue.related + [{
                "principle": "Fairness",
                "requirement": "Accountability",
                "subRequirement": "Auditability"
            }]}.values())
            issue.save_new()

        unrelated_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in unrelated_issues:
            # ensure issues don't relate to this
            issue.related = [rel for rel in issue.related if rel['subRequirement'] != "Auditability"]
            issue.save_new()

        fairness_nodes = filter_issues(titles_of_related_nodes=['Fairness'])

        fairness_issues = [i for i in fairness_nodes if type(i) is Issue]
        self.assertEqual(5, len(fairness_issues))

        self.assertEqual(8, len(fairness_nodes))  # 5 issues + requirements + principle

    def test_aggregation_key_requirement_should_not_return_sub_requirements(self):
        related_issues = [TestObjects.create_issue() for _ in range(5)]

        for issue in related_issues:
            issue.save_new()

        no_subs = filter_issues(aggregation_level="KeyRequirement")
        sub_requirements = [n for n in no_subs if type(n) is SubRequirement]
        self.assertEqual(0, len(sub_requirements))

        key_requirements = [n for n in no_subs if type(n) is KeyRequirement]
        self.assertGreater(len(key_requirements), 0)

        principles = [n for n in no_subs if type(n) is EthicalPrinciple]
        self.assertGreater(len(principles), 0)

    def test_aggregation_principle_should_not_return_lower(self):
        related_issues = [TestObjects.create_issue() for _ in range(5)]

        for issue in related_issues:
            issue.save_new()

        no_keys = filter_issues(aggregation_level="EthicalPrinciple")
        sub_requirements = [n for n in no_keys if type(n) is SubRequirement]
        self.assertEqual(0, len(sub_requirements))

        key_requirements = [n for n in no_keys if type(n) is KeyRequirement]
        self.assertEqual(0, len(key_requirements))

        principles = [n for n in no_keys if type(n) is EthicalPrinciple]
        self.assertGreater(len(principles), 0)

    def test_filter_issue_with_all_params_not_none(self):
        related_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in related_issues:
            # ensure issues relate to this
            issue.related = list({v['subRequirement']: v for v in issue.related + [{
                "principle": "Fairness",
                "requirement": "Accountability",
                "subRequirement": "Auditability"
            }]}.values())
            issue.save_new()
        for issue in related_issues[:2]:
            issue.description += "some random test text"
            issue.save_update()

        for issue in related_issues[2:4]:
            issue.title += "some random test text"
            issue.save_update()

        unrelated_issues = [TestObjects.create_issue() for _ in range(5)]
        for issue in unrelated_issues:
            # ensure issues don't relate to this
            issue.related = [rel for rel in issue.related if rel['subRequirement'] != "Auditability"]
            issue.save_new()

        fairness_nodes = filter_issues(contains_text="some random test text", titles_of_related_nodes=['Fairness'], aggregation_level="EthicalPrinciple")

        fairness_issues = [i for i in fairness_nodes if type(i) is Issue]
        self.assertEqual(4, len(fairness_issues))

        self.assertEqual(5, len(fairness_nodes))  # 4 issues + principle
