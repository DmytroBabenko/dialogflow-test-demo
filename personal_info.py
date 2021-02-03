from input_action_type import IntentType
from parameter_keys import ParameterKeys


class PersonalInfo:
    def __init__(self):
        self._param_value_dict = dict()
        self._main_user_intent: IntentType = IntentType.UNDEFINED

    @property
    def main_user_intent(self):
        return self._main_user_intent

    @main_user_intent.setter
    def main_user_intent(self, value: IntentType):
        self._main_user_intent = value

    def set_param_value(self, key, value):
        self._param_value_dict[key] = value

    def get_param_value(self, key):
        if key not in self._param_value_dict:
            return None

        return self._param_value_dict[key]

    def contain_first_name(self):
        if ParameterKeys.FIRST_NAME in self._param_value_dict:
            return True
        return False

    def contains_last_name(self):
        if ParameterKeys.LAST_NAME in self._param_value_dict:
            return True

        return False
