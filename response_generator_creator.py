from input_action_type import InputActionType
from question_answer_session.question_answer_session import QuestionAnswerSession
from response_generator import WelcomeResponseGenerator, FinishResponseGenerator
from response_generator_decorator import FallbackResponseGenerator, UnsuitableResponseGenerator


class ResponseGeneratorCreator:

    @staticmethod
    def create(user_input_action: InputActionType, expected_input_action: InputActionType):
        if user_input_action == expected_input_action:
            return ResponseGeneratorCreator._create(user_input_action)

        if expected_input_action == InputActionType.ANY:
            return ResponseGeneratorCreator._create(user_input_action)

        if user_input_action == InputActionType.UNKNOWN:
            return FallbackResponseGenerator(response_generator=QuestionAnswerSession())

        return UnsuitableResponseGenerator(response_generator=QuestionAnswerSession(),
                                           input_action_type=user_input_action,
                                           expected_action_type=expected_input_action)

    @staticmethod
    def _create(input_action: InputActionType):
        if input_action == InputActionType.WELCOME:
            return WelcomeResponseGenerator()

        if input_action == InputActionType.OPEN_LOAN:
            return QuestionAnswerSession()

        if input_action.is_question_answering():
            return QuestionAnswerSession()

        if input_action == InputActionType.END:
            return FinishResponseGenerator()

        return FallbackResponseGenerator(None)
