from dialog_tracker import DialogTracker
from input_action_type import InputActionType


class DialogProcessor:
    def __init__(self):
        self._cur_dialog_tracker: DialogTracker = None

    def process(self, input_action_type: InputActionType, query_result):
        if self._is_start_dialog(input_action_type, query_result):
            if self._cur_dialog_tracker:
                self._cur_dialog_tracker.show_personal_information()
            self._cur_dialog_tracker = DialogTracker()

        response = self._cur_dialog_tracker.track(user_input_action=input_action_type, query_result=query_result)

        if self._is_end_dialog(input_action_type, query_result):
            self._cur_dialog_tracker.show_personal_information()
            self._cur_dialog_tracker = None

        return response

    def _is_start_dialog(self, input_action_type: InputActionType, query_result):
        return input_action_type == InputActionType.WELCOME

    def _is_end_dialog(self, input_action_type: InputActionType, query_result):
        return input_action_type == InputActionType.END
