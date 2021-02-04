import random

from abc import abstractmethod

from input_action_type import InputActionType
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo


class ResponseGenerator:

    @abstractmethod
    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        ...

    @abstractmethod
    def get_expected_next_action_type(self) -> InputActionType:
        ...


class WelcomeResponseGenerator(ResponseGenerator):
    _WELCOME_LIST = [
        "Hello! How can I help you?",
        "Good day! What can I do for you today?",
        "Greetings! How can I assist?",
        "Hi! How are you doing?",
    ]

    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        response = random.choice(self._WELCOME_LIST)
        return response

    def get_expected_next_action_type(self) -> InputActionType:
        return InputActionType.ANY


class FinishResponseGenerator(ResponseGenerator):
    _FINISH_TEXT_LIST = [
        "Ok, %s, bye. Have a good day!",
        "Good bye, %s",
        "Have a nice day, %s",
    ]

    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        first_name = personal_info.get_param_value(key=ParameterKeys.FIRST_NAME.get_key())
        response = random.choice(self._FINISH_TEXT_LIST) % first_name

        return response

    def get_expected_next_action_type(self) -> InputActionType:
        return InputActionType.ANY

