from enum import Enum


class QAType(Enum):
    NAME = 0,
    DOB = 1,
    SSN = 2,
    EMAIL = 3,
    UNDEFINED = -1
