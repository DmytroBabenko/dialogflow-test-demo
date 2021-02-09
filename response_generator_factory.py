from input_action_type import InputActionType
from question_answer_session.question_answer_session import QuestionAnswerSession
from response_generator import WelcomeResponseGenerator, FinishResponseGenerator
from response_generator_decorator import FallbackResponseGenerator, UnsuitableResponseGenerator


class ResponseGeneratorFactory:


    @staticmethod
    def create(user_input_action: InputActionType, expected_input_action: InputActionType,
               qa_session: QuestionAnswerSession = None):
        if not qa_session:
            qa_session = QuestionAnswerSession()
        if user_input_action == expected_input_action:
            return ResponseGeneratorFactory._create(user_input_action, qa_session)

        if expected_input_action == InputActionType.ANY:
            return ResponseGeneratorFactory._create(user_input_action, qa_session)

        if user_input_action == InputActionType.UNKNOWN:
            return FallbackResponseGenerator(response_generator=qa_session)

        return UnsuitableResponseGenerator(response_generator=qa_session,
                                           input_action_type=user_input_action,
                                           expected_action_type=expected_input_action)

    @staticmethod
    def _create(input_action: InputActionType, qa_session: QuestionAnswerSession):
        if input_action == InputActionType.WELCOME:
            return WelcomeResponseGenerator()

        if input_action == InputActionType.OPEN_LOAN:
            return qa_session

        if input_action == InputActionType.INSURANCE:
            return qa_session

        if input_action.is_question_answering():
            return qa_session

        if input_action == InputActionType.END:
            return FinishResponseGenerator()

        return FallbackResponseGenerator(qa_session)
