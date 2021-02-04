from typing import Set

from input_action_type import InputActionType
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo
from question_answer_session.question_answer_session import QuestionAnswerSession
from response_generator import FallbackResponseGenerator, FinishResponseGenerator, WelcomeResponseGenerator


class DialogTracker:
    def __init__(self):
        self.personal_info: PersonalInfo = PersonalInfo()
        self.user_intents: Set[InputActionType] = set()
        self._qa_session: QuestionAnswerSession = QuestionAnswerSession()
        self._expected_input_action: InputActionType = InputActionType.WELCOME

    def track(self, user_input_action: InputActionType, query_result: dict):
        self._update_personal_info(user_input_action, query_result)

        if user_input_action == InputActionType.WELCOME:
            return WelcomeResponseGenerator().generate_response(personal_info=self.personal_info)[1]

        if user_input_action.is_intent():
            if self._qa_session.should_ask_anything(personal_info=self.personal_info):
                intent_type = user_input_action.convert_to_intent_type()
                if self._qa_session.was_session_started():
                    return self._qa_session.generate_unsuitable_input_action_response(
                        input_action_description=str(intent_type),
                        personal_info=self.personal_info)
                return self._qa_session.generate_response(self.personal_info)
            else:
                return self._qa_session.generate_response(personal_info=self.personal_info)

        elif user_input_action.is_question_answering():
            return self._qa_session.generate_response(self.personal_info)
        elif user_input_action.is_fallback():
            response = FallbackResponseGenerator().generate_response(self.personal_info)[1]
            if self._qa_session.should_ask_anything(personal_info=self.personal_info):
                if self._qa_session.was_session_started():
                    response += self._qa_session.generate_response(self.personal_info)

            return response

        # self.save_personal_information()
        return FinishResponseGenerator().generate_response(self.personal_info)[1]

    def _update_personal_info(self, user_input_action: InputActionType, query_result: dict):
        parameters = query_result.get('parameters')
        for key, value in parameters.items():
            if value:
                self.personal_info.set_param_value(key, value)

        if user_input_action.is_intent():
            self.personal_info.main_user_intent = user_input_action.convert_to_intent_type()

    def save_personal_information(self):
        print("#########-Personal information#########################")
        for item in ParameterKeys:
            print(f"{item.get_description()}: ",  self.personal_info.get_param_value(item.get_key()))

