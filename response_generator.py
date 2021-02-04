import random

from abc import abstractmethod
from typing import Tuple

from parameter_keys import ParameterKeys
from personal_info import PersonalInfo


class ResponseGenerator:

    @abstractmethod
    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        ...


class WelcomeResponseGenerator(ResponseGenerator):
    _WELCOME_LIST = [
        "Hello! How can I help you?",
        "Good day! What can I do for you today?",
        "Greetings! How can I assist?",
        "Hi! How are you doing?",
    ]

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        response = random.choice(self._WELCOME_LIST)
        return True, response


class EndQASessionResponseGenerator(ResponseGenerator):
    _RESPONSE_TEXT_LIST = [
        "Ok, {name}. We noted your personal information and we are going to find the relevant {intent} for you and contact you "
        "soon. "
    ]

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        first_name = personal_info.get_param_value(key=ParameterKeys.FIRST_NAME.get_key())
        intent_description = str(personal_info.main_user_intent)
        response = random.choice(self._RESPONSE_TEXT_LIST).format(name=first_name, intent=intent_description)

        return True, response


class FallbackResponseGenerator(ResponseGenerator):
    _RESPONSE_TEXT_LIST = [
        "Sorry, I don't understand you. Could you please repeat. ",
        "I didn't get that. Can you say it again? ",
        "I missed what you said. What was that? ",
        "Sorry, could you say that again? ",
        "Sorry, can you say that again? ",
        "Can you say that again? ",
        "Sorry, I didn't get that. Can you rephrase? ",
        "Sorry, what was that? ",
        "One more time? ",
        "What was that? ",
        "Say that one more time? ",
        "I didn't get that. Can you repeat? ",
        "I missed that, say that again? ",
    ]

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        response = random.choice(self._RESPONSE_TEXT_LIST)

        return True, response


class FinishResponseGenerator(ResponseGenerator):

    _FINISH_TEXT_LIST = [
        "Ok, %s, bye. Have a good day!",
        "Good bye, %s",
        "Have a nice day, %s",
    ]

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        first_name = personal_info.get_param_value(key=ParameterKeys.FIRST_NAME.get_key())
        response = random.choice(self._FINISH_TEXT_LIST) % first_name

        return True, response
