from aenum import Enum


class ParameterKeys(Enum):
    FIRST_NAME = "given-name", "First name"
    LAST_NAME = "last-name", "Last name"
    DOB = "date-time", "date of birthday"
    SSN = "number-sequence", "social security number"
    EMAIL = "email", "email address"

    def get_key(self):
        return self.value[0]

    def get_description(self):
        return self.value[1]
