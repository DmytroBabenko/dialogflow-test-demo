import unittest

from app import app


class APITest(unittest.TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()


    def test_open_loan_intent(self):
        data = {'queryText': 'I want top oopen the loan', 'action': 'input.open_loan', 'parameters': {}, 'allRequiredParamsPresent': True, 'fulfillmentMessages': [{'text': {'text': ['']}}], 'outputContexts': [{'name': 'projects/dauntless-ether-301609/locations/global/agent/sessions/45177ca1-91f2-3fcd-64c2-8dc5fff6e175/contexts/__system_counters__', 'parameters': {'no-input': 0.0, 'no-match': 0.0, 'number': 4.0, 'number.original': '4', 'number1': 5.0, 'number1.original': '5'}}], 'intent': {'name': 'projects/dauntless-ether-301609/locations/global/agent/intents/5b0e3799-d9a7-4a97-8d4f-2228503423d1', 'displayName': 'add.numbers'}, 'intentDetectionConfidence': 1.0, 'languageCode': 'en'}

        res = self.client.post('/dialog', data=data)


        a = 10



