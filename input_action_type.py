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
    WELCOME = 0,
    OPEN_LOAN = 1,
    NAME_CALLING = 2,
    DOB_CALLING = 3,
    SSN_CALLING = 4,
    EMAIL_CALLING = 5,
    END = 6,
    ANY = 7,
    UNKNOWN = -1

    def is_intent(self):
        if self is InputActionType.OPEN_LOAN:
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

    # def __str__(self):
    #     #TODO: add description
    #     return str(self)

QA_SESSION_TYPES = [InputActionType.NAME_CALLING, InputActionType.DOB_CALLING]

INPUT_ACTION_NAME_TYPE_MAPPER = {
    'input.welcome': InputActionType.WELCOME,
    'input.open_loan': InputActionType.OPEN_LOAN,
    'input.name_calling': InputActionType.NAME_CALLING,
    'input.dob': InputActionType.DOB_CALLING,
    'input.ssn': InputActionType.SSN_CALLING,
    'input.email': InputActionType.EMAIL_CALLING,
    'input.fallback': InputActionType.UNKNOWN,
    "input.end": InputActionType.END
}
