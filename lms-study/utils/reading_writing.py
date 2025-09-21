from dataclasses import asdict
import json

from study_data import AllQuestions, Level, Question


def save_questions_to_file(all_questions: AllQuestions, filename: str):
    with open(filename, "w") as f:
        json.dump(asdict(all_questions), f, indent=4)


def dict_to_question(question):
    return Question(**question)


def dict_to_level(level):
    return Level(
        number=level["number"],
        questions=[dict_to_question(q) for q in level["questions"]],
    )


def load_all_questions_from_file(filename: str) -> AllQuestions:
    with open(filename, "r") as f:
        data = json.load(f)
    levels = [dict_to_level(l) for l in data["levels"]]
    return AllQuestions(levels=levels)
