from input_action_type import InputActionType
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo
from response_generator_creator import ResponseGeneratorCreator


class DialogTracker:
    def __init__(self):
        self._expected_input_action: InputActionType = InputActionType.WELCOME
        self._personal_info: PersonalInfo = PersonalInfo()

    def track(self, user_input_action: InputActionType, query_result: dict):
        response_generator = ResponseGeneratorCreator.create(user_input_action=user_input_action,
                                                             expected_input_action=self._expected_input_action)

        response = response_generator.generate_response_and_parse_info(query_result, self._personal_info)
        self._expected_input_action = response_generator.get_expected_next_action_type()
        return response


    def save_personal_information(self):
        print("#########-Personal information#########################")
        for item in ParameterKeys:
            print(f"{item.get_description()}: ", self._personal_info.get_param_value(item.get_key()))
