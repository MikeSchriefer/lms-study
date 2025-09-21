from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    question: str
    choices: List[str]
    correct_answer: str


@dataclass
class Level:
    number: str
    questions: List[Question] = field(default_factory=list)

    def add_question(self, question: Question):
        self.questions.append(question)


@dataclass
class AllQuestions:
    levels: List[Level] = field(default_factory=list)

    def add_level(self, level: Level):
        self.levels.append(level)


all_questions = AllQuestions()
