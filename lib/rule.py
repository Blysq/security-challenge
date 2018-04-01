class Rule:
	def __init__(self):
		self.name = None

	def test(self, request, body, url):
		return True

	def get_exploit_type(self):
		return self.__class__.__name__

	def create_payload(self, inputs, value):
		payload = {}

		for input in inputs:
			if not input.has_attr('type') or not input.has_attr('name'):
				continue

			if input['type'] == 'submit':
				if input.has_attr('value'):
					payload[input['name']] = input['value']
			else:
				payload[input['name']] = "%s" % value

		return payload