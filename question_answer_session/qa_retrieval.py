import random
import datetime

from abc import abstractmethod
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo, NameInfo, DOBInfo


class QARetrieval:

    @abstractmethod
    def generate_intro_question(self) -> str:
        ...

    @abstractmethod
    def parse_answer(self, query_parameters: dict, personal_info: PersonalInfo) -> bool:
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
        name_info = personal_info.name_info

        if not name_info:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_FIRST_AND_LAST_NAME_LIST)

        if not name_info.first_name and not name_info.last_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_FIRST_AND_LAST_NAME_LIST)
        elif not name_info.first_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_FIRST_NAME_LIST) % name_info.last_name
        elif not name_info.last_name:
            return random.choice(NameQARetrieval.NameCallingTemplateText.NO_LAST_NAME_LIST) % name_info.first_name

        return ""

    def generate_intro_question(self) -> str:
        return random.choice(NameQARetrieval.NameCallingTemplateText.INTRO_LIST)

    def parse_answer(self, query_parameters: dict, personal_info: PersonalInfo) -> bool:
        if not personal_info.name_info:
            personal_info.name_info = NameInfo()

        if ParameterKeys.FIRST_NAME.get_key() in query_parameters:
            personal_info.name_info.first_name = query_parameters[ParameterKeys.FIRST_NAME.get_key()]

        if ParameterKeys.LAST_NAME.get_key() in query_parameters:
            personal_info.name_info.last_name = query_parameters[ParameterKeys.LAST_NAME.get_key()]

        if personal_info.name_info.first_name and personal_info.name_info.last_name:
            return True

        return False


class DOBQARetrieval(QARetrieval):
    _TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    _INTRO_LIST = [
        "And provide me your date of birthday",
    ]

    _NOT_DOB = [
        "Sorry, I did not get your date of birthday. Could you please provide ",
        "Sorry, I did not get it. Please provide your day month and year of your birthday"
    ]

    _NOT_YEAR = [
        "Could you repeat please your year of birthday",
        "And in which year of your birthday"
    ]

    _NOT_MONTH = [
        "Could you repeat please your month of birthday",
        "And in which month of your birthday"
    ]

    _NOT_DAY = [
        "Could you repeat please your day of birthday",
        "And in which day of your birthday"
    ]

    _NOT_MONTH_AND_DAY = [
        "And what is your day and month of birthday",
        "And provide please your day and month of birthday"
    ]

    _NOT_MONTH_AND_YEAR = [
        "And what is your year and month of birthday",
        "And provide please your year and month of birthday"
    ]

    _NOT_YEAR_AND_DAY = [
        "And what is your year and day of birthday",
        "And provide please your year and day of birthday"
    ]

    _UNSUITABLE_INTENT_ANSWER_START_LIST = [
        "Let's finish with providing date of birthday  and later move on to the {intent_desc} part. "
    ]

    def __init__(self):
        self._first_retrieval: bool = True

    def generate_intro_question(self):
        return random.choice(self._INTRO_LIST)

    def parse_answer(self, query_parameters: dict, personal_info: PersonalInfo) -> bool:
        if not personal_info.dob_info:
            personal_info.dob_info = DOBInfo()

        if ParameterKeys.DOB.get_key() in query_parameters:
            date_time_str = query_parameters[ParameterKeys.DOB.get_key()]
            date_obj = datetime.datetime.strptime(date_time_str, self._TIMESTAMP_FORMAT)

            now_date = datetime.datetime.now()

            if not personal_info.dob_info.year and (date_obj.year != now_date.year or not self._first_retrieval):
                personal_info.dob_info.year = date_obj.year

            if not personal_info.dob_info.month and (date_obj.month != now_date.month or not self._first_retrieval):
                personal_info.dob_info.month = date_obj.month

            if not personal_info.dob_info.day and (date_obj.day != now_date.day or not self._first_retrieval):
                personal_info.dob_info.day = date_obj.day

            self._first_retrieval = False

        if personal_info.dob_info.contains_all_info():
            return True

        return False

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        if not personal_info.dob_info:
            return random.choice(self._NOT_DOB)

        if not personal_info.dob_info.year and not personal_info.dob_info.month and not personal_info.dob_info.day:
            return random.choice(self._NOT_DOB)

        if not personal_info.dob_info.year and not personal_info.dob_info.month:
            return random.choice(self._NOT_MONTH_AND_YEAR)

        if not personal_info.dob_info.month and not personal_info.dob_info.day:
            return random.choice(self._NOT_MONTH_AND_DAY)

        if not personal_info.dob_info.day and not personal_info.dob_info.year:
            return random.choice(self._NOT_YEAR_AND_DAY)

        if not personal_info.dob_info.year:
            return random.choice(self._NOT_YEAR)

        if not personal_info.dob_info.month:
            return random.choice(self._NOT_MONTH)

        if not personal_info.dob_info.day:
            return random.choice(self._NOT_DAY)

        return ""


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

    def parse_answer(self, query_parameters: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.SSN.get_key() in query_parameters:
            personal_info.ssn = query_parameters[ParameterKeys.SSN.get_key()]

        if personal_info.ssn:
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

    def parse_answer(self, query_parameters: dict, personal_info: PersonalInfo) -> bool:
        if ParameterKeys.EMAIL.get_key() in query_parameters:
            personal_info.email = query_parameters[ParameterKeys.EMAIL.get_key()]

        if personal_info.email:
            return True

        return False

    def clarify_question(self, personal_info: PersonalInfo) -> str:
        first_name: str = personal_info.name_info.first_name
        return random.choice(self._NOT_EMAIL).format(name=first_name)
