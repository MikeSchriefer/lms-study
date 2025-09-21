import os
from pathlib import Path
import re

from google import genai
from structlog import get_logger
from utils.study_data import all_questions, AllQuestions, Question, Level

logger = get_logger()

client = genai.Client()


def generate_test_questions(level):
    # Retrieve and upload PDFs using the File API
    study_guides = [
        client.files.upload(
            file=f"study_guides/{pdf}", config=dict(mime_type="application/pdf")
        )
        for pdf in os.listdir("study_guides")
    ]

    # set prompt
    prompt = """
  Using these pdf study guides, please create a test with question, choices, and correct answer.
  I would like for them to come directly from the source material and include every question in random order.
  """
    # submit prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[*study_guides, prompt]
    )
    logger.info(response.text)
    return response


def get_study_guides(level: str):
    root_dir = Path("study_guides/")
    study_guides = []
    # Iterate over immediate subdirectories only
    for subdir in root_dir.iterdir():
        if subdir.is_dir() and subdir.name.lower() == f"level_{level}":
            # Process files one at a time in this subdir
            for file_path in subdir.iterdir():
                if file_path.is_file():
                    study_guides.append(
                        client.files.upload(
                            file=file_path, config=dict(mimetype="application/pdf")
                        )
                    )


def parse_test_questions(full_question_text: str, level: str):

    blocks = full_question_text.strip().split("---")

    current_level = Level(level)

    for block in blocks:
        # Extract question text (everything after **Question n** until choices)
        question_match = re.search(
            r"\*\*Question \d+\*\*\n(.+?)(?=\na\.|\n\bTrue\b|\n\bFalse\b)",
            block,
            re.DOTALL,
        )
        question = question_match.group(1).strip() if question_match else None
        if not question:
            continue

        # Extract all choices (lines starting with a letter and dot) or True/False options
        choices = re.findall(r"^[a-d]\. .+", block, re.MULTILINE)
        if not choices:
            # For True/False type questions without lettered choices
            tf_choices = re.findall(r"^(True|False)$", block, re.MULTILINE)
            choices = tf_choices if tf_choices else []

        # Extract the correct answer line after Correct Answer
        correct_answer_match = re.search(r"\*\*Correct Answer:\*\*\s*(.+)", block)
        correct_answer = (
            correct_answer_match.group(1).strip() if correct_answer_match else None
        )

        current_level.add_question(
            Question(question=question, choices=choices, correct_answer=correct_answer)
        )

    all_questions.add_level(current_level)

    logger.info(
        "finished generating questions fore level {level}",
        sample_question=level.questions[1].question,
    )
