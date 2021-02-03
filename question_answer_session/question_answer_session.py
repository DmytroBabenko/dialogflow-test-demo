from enum import Enum
from typing import List

from personal_info import PersonalInfo
from question_answer_session.qa_response_generator import QAResponseGenerator
from question_answer_session.qa_type import QAType
from question_answer_session.question_answer_generator_creator import QuestionAnswerGeneratorCreator
from response_generator import EndQASessionResponseGenerator


class QuestionAnswerSession:
    class QAStatus(Enum):
        INTRO = 0,
        RECTIFICATION = 1,
        FINISHED = 2,

    class QATypeStatusItem:
        def __init__(self, qa_type: QAType, status):
            self.qa_type = qa_type
            self.status = status

    def __init__(self):
        self._qa_type_chain: List[QuestionAnswerSession.QATypeStatusItem] = [
            QuestionAnswerSession.QATypeStatusItem(QAType.NAME, QuestionAnswerSession.QAStatus.INTRO),
            QuestionAnswerSession.QATypeStatusItem(QAType.DOB, QuestionAnswerSession.QAStatus.INTRO),
            QuestionAnswerSession.QATypeStatusItem(QAType.SSN, QuestionAnswerSession.QAStatus.INTRO),
            QuestionAnswerSession.QATypeStatusItem(QAType.EMAIL, QuestionAnswerSession.QAStatus.INTRO),
        ]

        self._curr_qa_chain_pos = 0
        self._session_started: bool = False

    def generate_response(self, personal_info: PersonalInfo) -> str:
        self._session_started = True
        cur_qa_type = self._qa_type_chain[self._curr_qa_chain_pos].qa_type
        cur_qa_status = self._qa_type_chain[self._curr_qa_chain_pos].status
        qa_generator: QAResponseGenerator = QuestionAnswerGeneratorCreator.create(cur_qa_type)

        if cur_qa_status == QuestionAnswerSession.QAStatus.INTRO:
            response = qa_generator.generate_intro_question()
            self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.RECTIFICATION
            return response
        elif cur_qa_status == QuestionAnswerSession.QAStatus.RECTIFICATION:
            finish, response = qa_generator.generate_response(personal_info)
            if not finish:
                return response

            self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.FINISHED

            if self._curr_qa_chain_pos < len(self._qa_type_chain) - 1:
                self._curr_qa_chain_pos += 1
                qa_generator: QAResponseGenerator = QuestionAnswerGeneratorCreator.create(
                    self._qa_type_chain[self._curr_qa_chain_pos].qa_type)
                response = qa_generator.generate_intro_question()
                self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.RECTIFICATION
                return response

        end_qa_response_generator = EndQASessionResponseGenerator()
        _, response = end_qa_response_generator.generate_response(personal_info)
        return response

    def generate_unsuitable_input_action_response(self, input_action_description: str, personal_info: PersonalInfo):
        if self._curr_qa_chain_pos < len(self._qa_type_chain):
            qa_generator: QAResponseGenerator = QuestionAnswerGeneratorCreator.create(
                self._qa_type_chain[self._curr_qa_chain_pos].qa_type)

            return qa_generator.generate_unsuitable_intent_response(personal_info=personal_info,
                                                                    indent_description=input_action_description)

        return None

    def generate_end_qa_response(self, personal_info: PersonalInfo):
        end_qa_response_generator = EndQASessionResponseGenerator()
        _, response = end_qa_response_generator.generate_response(personal_info)
        return response

    def should_ask_anything(self, personal_info):
        for item in self._qa_type_chain:
            if item.status != QuestionAnswerSession.QAStatus.FINISHED:
                return True
        return False

    def get_expected_next_qa_type(self):
        if self._curr_qa_chain_pos < len(self._qa_type_chain):
            return self._qa_type_chain[self._curr_qa_chain_pos].qa_type

        return QAType.UNDEFINED

    def was_session_started(self) -> bool:
        return self._session_started
