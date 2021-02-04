from enum import Enum

from input_action_type import InputActionType


class QAType(Enum):
    NAME = 0,
    DOB = 1,
    SSN = 2,
    EMAIL = 3,
    UNDEFINED = -1


QA_TYPE_ACTION_TYPE_MAPPER = {
    QAType.NAME: InputActionType.NAME_CALLING,
    QAType.DOB: InputActionType.DOB_CALLING,
    QAType.SSN: InputActionType.SSN_CALLING,
    QAType.EMAIL: InputActionType.EMAIL_CALLING,
    QAType.UNDEFINED: InputActionType.UNKNOWN
}
