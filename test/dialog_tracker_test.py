import unittest

from dialog_tracker import DialogTracker
from input_action_type import InputActionType


class DialogTrackerTest(unittest.TestCase):



    def test_1(self):
        dialog_tracker = DialogTracker()

        response = dialog_tracker.track(user_input_action=InputActionType.OPEN_LOAN, query_result={
            'queryText': 'My name is Mike Tayson!',
            'action': 'input.open_loan',
            'parameters': {
            }
        })

        a = 10
