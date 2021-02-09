import random

from abc import abstractmethod

from input_action_type import InputActionType
from personal_info import PersonalInfo
from response_generator import ResponseGenerator


class ResponseGeneratorDecorator(ResponseGenerator):
    def __init__(self, response_generator: ResponseGenerator):
        self._response_generator: ResponseGenerator = response_generator

    @abstractmethod
    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        if not self._response_generator:
            return ""

        return self._response_generator.generate_response_and_parse_info(query_result, personal_info)

    @abstractmethod
    def get_expected_next_action_type(self) -> InputActionType:
        if not self._response_generator:
            return InputActionType.ANY

        return self._response_generator.get_expected_next_action_type()


class FallbackResponseGenerator(ResponseGeneratorDecorator):
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

    def __init__(self, response_generator: ResponseGenerator):
        super().__init__(response_generator)

    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        response = random.choice(self._RESPONSE_TEXT_LIST)
        response += super().generate_response_and_parse_info(query_result, personal_info)

        return response

    def get_expected_next_action_type(self) -> InputActionType:
        return super().get_expected_next_action_type()


class UnsuitableResponseGenerator(ResponseGeneratorDecorator):
    _UNSUITABLE_TEXT_LIST = [
        "Let's finish with {cur_intent_desc}  and later move on to the  {intent_desc} part. "
    ]

    def __init__(self, response_generator: ResponseGenerator,
                 input_action_type: InputActionType, expected_action_type: InputActionType):
        super().__init__(response_generator)
        self._input_action_type = input_action_type
        self._expected_action_type = expected_action_type

    def generate_response_and_parse_info(self, query_result: dict, personal_info: PersonalInfo) -> str:
        response = random.choice(self._UNSUITABLE_TEXT_LIST).format(cur_intent_desc=str(self._expected_action_type),
                                                                    intent_desc=str(self._input_action_type))
        response += super().generate_response_and_parse_info(query_result, personal_info)

        return response

    def get_expected_next_action_type(self) -> InputActionType:
        return super().get_expected_next_action_type()

