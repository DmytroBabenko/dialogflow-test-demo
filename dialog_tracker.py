from input_action_type import InputActionType
from personal_info import PersonalInfo
from question_answer_session.question_answer_session import QuestionAnswerSession
from response_generator_factory import ResponseGeneratorFactory


class DialogTracker:
    def __init__(self):
        self._expected_input_action: InputActionType = InputActionType.WELCOME
        self._personal_info: PersonalInfo = PersonalInfo()
        self._qa_session: QuestionAnswerSession = QuestionAnswerSession()

    def track(self, user_input_action: InputActionType, query_result: dict):
        response_generator = ResponseGeneratorFactory.create(user_input_action=user_input_action,
                                                             expected_input_action=self._expected_input_action,
                                                             qa_session=self._qa_session)

        response = response_generator.generate_response_and_parse_info(query_result['parameters'], self._personal_info)
        self._expected_input_action = response_generator.get_expected_next_action_type()
        return response

    def show_personal_information(self):
        """

        :rtype: object
        """
        print(str(self._personal_info))