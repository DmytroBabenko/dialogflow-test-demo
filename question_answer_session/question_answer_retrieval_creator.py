from question_answer_session.qa_retrieval import QARetrieval, \
    NameQARetrieval, DOBQARetrieval, SSNQARetrieval, \
    EmailQARetrieval
from question_answer_session.qa_type import QAType


class QuestionAnswerRetrievalCreator:

    @staticmethod
    def create(qa_type: QAType) -> QARetrieval:
        if qa_type == QAType.NAME:
            return NameQARetrieval()

        if qa_type == QAType.DOB:
            return DOBQARetrieval()

        if qa_type == QAType.SSN:
            return SSNQARetrieval()

        if qa_type == QAType.EMAIL:
            return EmailQARetrieval()

        return None
