import aenum
from enum import Enum


class IntentType(aenum.Enum):
    LOAN = 0, "loan"
    CREDIT = 1, 'credit'
    INSURANCE = 2, "insurance"
    UNDEFINED = -1, "undefined"

    def __str__(self):
        return self.value[1]


class InputActionType(Enum):
    WELCOME = 0, "welcome"
    OPEN_LOAN = 1, "open loan"
    INSURANCE = 2, "insurance"
    NAME_CALLING = 3, "your name"
    DOB_CALLING = 4, "date of birthday"
    SSN_CALLING = 5, "social security number"
    EMAIL_CALLING = 6, "email calling"
    END = 7, "finish"
    ANY = 8, "this"
    UNKNOWN = -1, "that"

    def is_intent(self):
        #TODO: create list of intent and check if self in list
        if self is InputActionType.OPEN_LOAN:
            return True

        if self is InputActionType.INSURANCE:
            return True

        return False

    def is_question_answering(self):
        if self is InputActionType.NAME_CALLING:
            return True

        if self is InputActionType.DOB_CALLING:
            return True

        if self is InputActionType.SSN_CALLING:
            return True

        if self is InputActionType.EMAIL_CALLING:
            return True

        return False

    def is_fallback(self):
        if self is InputActionType.UNKNOWN:
            return True

        return False

    def __str__(self):
        return self.value[1]


INPUT_ACTION_NAME_TYPE_MAPPER = {
    'input.welcome': InputActionType.WELCOME,
    'input.open_loan': InputActionType.OPEN_LOAN,
    'input.insurance': InputActionType.INSURANCE,
    'input.name_calling': InputActionType.NAME_CALLING,
    'input.dob': InputActionType.DOB_CALLING,
    'input.ssn': InputActionType.SSN_CALLING,
    'input.email': InputActionType.EMAIL_CALLING,
    'input.fallback': InputActionType.UNKNOWN,
    "input.end": InputActionType.END
}
