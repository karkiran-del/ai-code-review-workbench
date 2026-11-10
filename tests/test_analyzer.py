import unittest

from code_review_workbench.analyzer import analyze_source


class AnalyzeSourceTests(unittest.TestCase):
    def test_valid_source(self):
        result = analyze_source("def greet():\n    return 'hello'\n")
        self.assertTrue(result["syntax_valid"])
        self.assertEqual(result["metrics"]["functions"], 1)

    def test_syntax_error(self):
        result = analyze_source("def broken(:\n    pass\n")
        self.assertFalse(result["syntax_valid"])
        self.assertEqual(result["findings"][0]["rule_id"], "PY001")

    def test_eval_is_flagged(self):
        result = analyze_source("value = eval(user_input)\n")
        rule_ids = {finding["rule_id"] for finding in result["findings"]}
        self.assertIn("SEC001", rule_ids)

    def test_possible_secret_is_flagged(self):
        result = analyze_source('api_key = "abcdefghijk123"\n')
        rule_ids = {finding["rule_id"] for finding in result["findings"]}
        self.assertIn("SEC003", rule_ids)


if __name__ == "__main__":
    unittest.main()
