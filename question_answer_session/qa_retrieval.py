import random

from abc import abstractmethod
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo


class QARetrieval:

    @abstractmethod
    def generate_intro_question(self) -> str:
        ...

    @abstractmethod
    def parse_answer(self, query_result: dict, personal_info: PersonalInfo) -> bool:
        ...

    @abstractmethod
    def clarify_question(self, personal_info: PersonalInfo) -> str:
        ...


class NameQARetrieval(QARetrieval):
    _QA_PART_NAME = "providing name"

    _NAME_KEYS = {ParameterKeys.FIRST_NAME, ParameterKeys.LAST_NAME}

    class NameCallingTemplateText:
        INTRO_LIST = [
            "First of all, could you please provide me your first and last name",
            "How can I call you",
            "Tell me please your first and last name",
        ]

        NO_FIRST_AND_LAST_NAME_LIST = [
            "I did not get your first and last name, could you repeat please"
        ]

        NO_FIRST_NAME_LIST = [
            "Your last name is %. Could you please say your first name, I did not get it"
        ]

        NO_LAST_NAME_LIST = [
            "%s, and what is your last name?"
        ]

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        first_name: str = personal_info.get_param_value(ParameterKeys.FIRST_NAME.get_key())
        last_name: str = personal_info.get_param_value(ParameterKeys.LAST_NAME.get_key())

        if not first_name and not last_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_FIRST_AND_LAST_NAME_LIST)
        elif not first_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_FIRST_NAME_LIST) % last_name
        elif not last_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_LAST_NAME_LIST) % first_name

        return ""

    def generate_intro_question(self) -> str:
        return random.choice(NameQARetrieval.NameCallingTemplateText.INTRO_LIST)

    def parse_answer(self, query_result: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.FIRST_NAME.get_key() in query_result:
            personal_info.set_param_value(key=ParameterKeys.FIRST_NAME.get_key(),
                                          value=query_result[ParameterKeys.FIRST_NAME.get_key()])

        if ParameterKeys.LAST_NAME in query_result:
            personal_info.set_param_value(key=ParameterKeys.FIRST_NAME.get_key(),
                                          value=query_result[ParameterKeys.FIRST_NAME.get_key()])

        if personal_info.contain_first_name() and personal_info.contains_last_name():
            return True

        return False


class DOBQARetrieval(QARetrieval):
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

    def parse_answer(self, query_result: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.DOB.get_key() in query_result:
            personal_info.set_param_value(key=ParameterKeys.DOB.get_key(),
                                          value=query_result[ParameterKeys.DOB.get_key()])

        if personal_info.contains_info(key=ParameterKeys.DOB.get_key()):
            return True

        return False

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        return random.choice(self._NOT_DOB)


class SSNQARetrieval(QARetrieval):
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

    def parse_answer(self, query_result: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.SSN.get_key() in query_result:
            personal_info.set_param_value(key=ParameterKeys.SSN.get_key(),
                                          value=query_result[ParameterKeys.SSN.get_key()])

        if personal_info.contains_info(key=ParameterKeys.SSN.get_key()):
            return True

        return False

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        return random.choice(self._NOT_SSN)


class EmailQARetrieval(QARetrieval):
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

    def parse_answer(self, query_result: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.EMAIL.get_key() in query_result:
            personal_info.set_param_value(key=ParameterKeys.EMAIL.get_key(),
                                          value=query_result[ParameterKeys.EMAIL.get_key()])

        if personal_info.contains_info(key=ParameterKeys.EMAIL.get_key()):
            return True

        return False

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        first_name: str = personal_info.get_param_value(ParameterKeys.FIRST_NAME.get_key())
        return random.choice(self._NOT_EMAIL).format(name=first_name)
