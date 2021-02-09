from input_action_type import IntentType


class PersonalInfo:
    def __init__(self):
        self.name_info: NameInfo = NameInfo()
        self.dob_info: DOBInfo = DOBInfo()
        self.ssn: str = None
        self.email: str = None
        self.main_user_intent: IntentType = IntentType.UNDEFINED

    def __str__(self) -> str:
        result = "###########-Personal-Information-#############\n"
        if self.name_info:
            result += f"Name: {self.name_info.first_name} {self.name_info.last_name}\n"
        if self.dob_info:
            result += f"Date of birthday: {self.dob_info.day}\\{self.dob_info.month}\\{self.dob_info.year}\n"

        result += f"social security number: {self.ssn}\n"
        result += f"email: {self.email}\n"

        return result


class NameInfo:
    def __init__(self, first_name: str = None, last_name: str = None):
        self.first_name: str = first_name
        self.last_name: str = last_name


class DOBInfo:
    def __init__(self, day: int = None, month: int = None, year: int = None):
        self.day: int = day
        self.month: int = month
        self.year: int = year

    def contains_all_info(self) -> bool:
        if not self.year:
            return False
        if not self.month:
            return False
        if not self.day:
            return False

        return True
