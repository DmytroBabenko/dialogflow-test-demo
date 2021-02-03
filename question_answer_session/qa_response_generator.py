import random

from abc import abstractmethod
from typing import Tuple

from parameter_keys import ParameterKeys
from personal_info import PersonalInfo
from response_generator import ResponseGenerator


class QAResponseGenerator(ResponseGenerator):

    @abstractmethod
    def generate_intro_question(self):
        ...

    @abstractmethod
    def generate_unsuitable_intent_response(self, personal_info: PersonalInfo, indent_description: str):
        ...


class NameCallingQAResponseGenerator(QAResponseGenerator):
    _QA_PART_NAME = "providing name"

    class NameCallingTemplateText:
        INTRO_LIST = [
            "First of all, could you please provide me your first and last name",
            "How can I call you",
            "Tell me please your first and last name",
        ]

        UNSUITABLE_INTENT_ANSWER_START_LIST = [
            "Let's finish with providing name  and later move on to the  {intent_desc} part. "
        ]

        # UNSUITABLE_INTENT_ANSWER_END_LIST = [
        #     f"Let's finish with name  and later move on to the %s part"
        # ]

        NO_FIRST_AND_LAST_NAME_LIST = [
            "I did not get your first and last name, could you repeat please"
        ]

        NO_FIRST_NAME_LIST = [
            "Your last name is %. Could you please say your first name, I did not get it"
        ]

        NO_LAST_NAME_LIST = [
            "%s, and what is your last name?"
        ]

    def generate_intro_question(self) -> str:
        return random.choice(NameCallingQAResponseGenerator.NameCallingTemplateText.INTRO_LIST)

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        first_name: str = personal_info.get_param_value(ParameterKeys.FIRST_NAME)
        last_name: str = personal_info.get_param_value(ParameterKeys.LAST_NAME)

        if not first_name and not last_name:
            return False, random.choice(
                NameCallingQAResponseGenerator.NameCallingTemplateText.NO_FIRST_AND_LAST_NAME_LIST)
        elif not first_name:
            return False, random.choice(
                NameCallingQAResponseGenerator.NameCallingTemplateText.NO_FIRST_NAME_LIST) % last_name
        elif not last_name:
            return False, random.choice(
                NameCallingQAResponseGenerator.NameCallingTemplateText.NO_LAST_NAME_LIST) % first_name

        return True, ""

    def generate_unsuitable_intent_response(self, personal_info: PersonalInfo, indent_description: str):
        response = random.choice(
            NameCallingQAResponseGenerator.NameCallingTemplateText.UNSUITABLE_INTENT_ANSWER_START_LIST).format(
            intent_desc=indent_description)

        response += self.generate_response(personal_info)[1]

        return response


class DOBQAResponseGenerator(QAResponseGenerator):
    _INTRO_LIST = [
        "And provide me your date of birthday",
    ]

    _NOT_DOB = [
        "Sorry, I did not get your date of birthday. Could you please provide "
    ]

    _UNSUITABLE_INTENT_ANSWER_START_LIST = [
        "Let's finish with providing date of birthday  and later move on to the {intent_desc} part. "
    ]

    def generate_intro_question(self):
        return random.choice(self._INTRO_LIST)

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        dob: str = personal_info.get_param_value(ParameterKeys.DOB)

        if not dob:
            return False, random.choice(self._NOT_DOB)

        return True, ""

    def generate_unsuitable_intent_response(self, personal_info: PersonalInfo, indent_description: str):
        response = random.choice(self._UNSUITABLE_INTENT_ANSWER_START_LIST).format(intent_desc=indent_description)

        response += self.generate_response(personal_info)[1]

        return response


class SSNQAResponseGenerator(QAResponseGenerator):
    _INTRO = [
        "Please tell me your social security number. ",
    ]

    _NOT_SSN = [
        "Sorry, I did not get yours SSN number. Could you provide it again. "
    ]

    _UNSUITABLE_INTENT_ANSWER_START_LIST = [
        "Let's wait until I write your correctly social security number  and later move on to the {intent_desc} part. "
    ]

    def generate_intro_question(self):
        return random.choice(self._INTRO)

    def generate_unsuitable_intent_response(self, personal_info: PersonalInfo, indent_description: str):
        response = random.choice(self._UNSUITABLE_INTENT_ANSWER_START_LIST).format(intent_desc=indent_description)

        response += self.generate_response(personal_info)[1]

        return response

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        ssn = personal_info.get_param_value(ParameterKeys.SSN)
        if not ssn:
            return False, random.choice(self._NOT_SSN)

        return True, ""


class EmailQAResponseGenerator(QAResponseGenerator):
    _INTRO = [
        "And tell me your email address ",
        "Please, provide your email address ",
        "Could you tell your email address ",
        "And what is your valid email address "
    ]

    _UNSUITABLE_INTENT_ANSWER_START_LIST = [
        "Let's wait until I write your correctly email address and later move on to the {intent_desc} part. "
    ]

    _NOT_EMAIL = [
        "{name}, I did not get your email, could you repeat it again"
    ]

    def generate_intro_question(self):
        return random.choice(self._INTRO)

    def generate_unsuitable_intent_response(self, personal_info: PersonalInfo, indent_description: str):
        response = random.choice(self._UNSUITABLE_INTENT_ANSWER_START_LIST).format(intent_desc=indent_description)

        response += self.generate_response(personal_info)[1]

        return response

    def generate_response(self, personal_info: PersonalInfo) -> Tuple[bool, str]:
        email: str = personal_info.get_param_value(ParameterKeys.EMAIL)
        first_name: str = personal_info.get_param_value(ParameterKeys.FIRST_NAME)
        if not email:
            return False, random.choice(self._NOT_EMAIL).format(name=first_name)

        return True, ""
