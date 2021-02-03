from question_answer_session.qa_response_generator import QAResponseGenerator, NameCallingQAResponseGenerator, \
    DOBQAResponseGenerator, SSNQAResponseGenerator, EmailQAResponseGenerator
from question_answer_session.qa_type import QAType


class QuestionAnswerGeneratorCreator:

    @staticmethod
    def create(qa_type: QAType) -> QAResponseGenerator:
        if qa_type == QAType.NAME:
            return NameCallingQAResponseGenerator()

        if qa_type == QAType.DOB:
            return DOBQAResponseGenerator()

        if qa_type == QAType.SSN:
            return SSNQAResponseGenerator()

        if qa_type == QAType.EMAIL:
            return EmailQAResponseGenerator()

        return None
