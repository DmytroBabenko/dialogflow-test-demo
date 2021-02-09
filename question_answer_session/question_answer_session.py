import random

from enum import Enum
from typing import List, Dict

from input_action_type import InputActionType
from parameter_keys import ParameterKeys
from personal_info import PersonalInfo
from question_answer_session.qa_retrieval import QARetrieval
from question_answer_session.qa_type import QAType, QA_TYPE_ACTION_TYPE_MAPPER
from question_answer_session.question_answer_retrieval_creator import QuestionAnswerRetrievalCreator
from response_generator import ResponseGenerator


class QuestionAnswerSession(ResponseGenerator):
    _END_RESPONSE_TEXT_LIST = [
        "Ok, {name}. We noted your personal information and we are going to find the relevant {intent} for you and contact you "
        "soon. "
    ]

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
        self._qa_retrieval_dict: Dict[QAType, QARetrieval] = dict()

    def generate_response_and_parse_info(self, query_parameters: dict, personal_info: PersonalInfo) -> str:
        self._session_started = True
        cur_qa_type = self._get_current_qa_type()
        cur_qa_status = self._qa_type_chain[self._curr_qa_chain_pos].status
        if cur_qa_type not in self._qa_retrieval_dict:
            self._qa_retrieval_dict[cur_qa_type] = QuestionAnswerRetrievalCreator.create(cur_qa_type)

        if cur_qa_status == QuestionAnswerSession.QAStatus.INTRO:
            response = self._qa_retrieval_dict[cur_qa_type].generate_intro_question()
            self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.RECTIFICATION
            return response
        elif cur_qa_status == QuestionAnswerSession.QAStatus.RECTIFICATION:
            if not self._qa_retrieval_dict[cur_qa_type].parse_answer(query_parameters=query_parameters, personal_info=personal_info):
                return self._qa_retrieval_dict[cur_qa_type].clarify_question(personal_info)

            self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.FINISHED

            self._curr_qa_chain_pos += 1
            if self._curr_qa_chain_pos < len(self._qa_type_chain):
                self._qa_retrieval_dict[cur_qa_type]: QARetrieval = QuestionAnswerRetrievalCreator.create(
                    self._qa_type_chain[self._curr_qa_chain_pos].qa_type)
                response = self._qa_retrieval_dict[cur_qa_type].generate_intro_question()
                self._qa_type_chain[self._curr_qa_chain_pos].status = QuestionAnswerSession.QAStatus.RECTIFICATION
                return response

        return self._generate_end_of_qa_session_response(personal_info)

    @staticmethod
    def _parse_answer(qa_retrieval: QARetrieval, query_parameters: dict, personal_info: PersonalInfo):
        try:
            return qa_retrieval.parse_answer(query_parameters=query_parameters, personal_info=personal_info)
        except:
            return False

    def get_expected_next_action_type(self) -> InputActionType:
        if self._curr_qa_chain_pos >= len(self._qa_type_chain):
            return InputActionType.END

        cur_qa_type = self._get_current_qa_type()
        return QA_TYPE_ACTION_TYPE_MAPPER[cur_qa_type]

    def _get_current_qa_type(self):
        if self._curr_qa_chain_pos >= len(self._qa_type_chain):
            return QAType.UNDEFINED

        cur_qa_type = self._qa_type_chain[self._curr_qa_chain_pos].qa_type
        return cur_qa_type

    def _generate_end_of_qa_session_response(self, personal_info: PersonalInfo) -> str:
        first_name = personal_info.name_info.first_name
        intent_description = str(personal_info.main_user_intent)
        response = random.choice(self._END_RESPONSE_TEXT_LIST).format(name=first_name, intent=intent_description)

        return response

    def should_ask_anything(self):
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
