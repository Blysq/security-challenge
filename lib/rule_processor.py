from lib.rules.sql_injection import SQLInjectionRule

class RuleProcessor:
	def __init__(self):
		self.rules = []
		self.add_all_rules()

	def filter_rules(self, rule_type):
		tmp_rules = []

		for rule in self.rules:
			if rule.get_exploit_type() == rule_type:
				tmp_rules.append(rule)

		self.rules = tmp_rules

	def test_all_rules(self, request, body, url):
		found_candidates = []

		for rule in self.rules:
			if rule.test(request, body, url) == True and rule.get_exploit_type() not in found_candidates:
				found_candidates.append(rule.get_exploit_type())

		return found_candidates

	def add_all_rules(self):
		self.rules.append(SQLInjectionRule())
