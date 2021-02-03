from dialog_tracker import DialogTracker
from input_action_type import InputActionType
from parameter_keys import ParameterKeys

dialog_tracker = DialogTracker()

response = dialog_tracker.track(user_input_action=InputActionType.OPEN_LOAN, query_result={
    'queryText': 'My name is Mike Tayson!',
    'action': 'input.open_loan',
    'parameters': {
    }
})
#
# response = dialog_tracker.track(user_input_action=InputActionType.NAME_CALLING, query_result={
#     'queryText': 'My name is Mike Tayson!',
#     'action': 'input.open_loan',
#     'parameters': {
#     }
# })

response = dialog_tracker.track(user_input_action=InputActionType.NAME_CALLING, query_result={
    'queryText': 'My name is Mike Tayson!',
    'action': 'input.open_loan',
    'parameters': {
        "given-name": 'Mike'
    }
})

response = dialog_tracker.track(user_input_action=InputActionType.UNKNOWN, query_result={
    'queryText': 'My name is Mike Tyson!',
    'action': 'input.open_loan',
    'parameters': {
        "last-name": 'Tyson'
    }
})

response = dialog_tracker.track(user_input_action=InputActionType.DOB_CALLING, query_result={
    'queryText': 'My name is Mike Tyson!',
    'action': 'input.open_loan',
    'parameters': {
        "date-time": '1992-06-03T12:00:00+03:00'
    }
})

response = dialog_tracker.track(user_input_action=InputActionType.SSN_CALLING, query_result= {
    'queryText': '3rd of September',
    'action': 'input.dob',
    'parameters': {
      'number-sequence': '678-098-6732'
    }
})


response = dialog_tracker.track(user_input_action=InputActionType.END, query_result= {
    'queryText': '3rd of September',
    'action': 'input.dob',
    'parameters': {
      'date-time': '2021-09-03T12:00:00+03:00'
    }
})
a = 10
