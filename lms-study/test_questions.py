import os

from google import genai
from structlog import get_logger

logger = get_logger()

client = genai.Client()


def generate_test_questions():
    # Retrieve and upload PDFs using the File API
    study_guides = [
        client.files.upload(
            file=f"study_guides/{pdf}", config=dict(mime_type="application/pdf")
        )
        for pdf in os.listdir("study_guides")
    ]

    prompt = """
  Using these pdf study guides, please create a five question test with question, choices, and correct answer.
  I would like for them to come directly from the source material and be a random sampling of five in a random order.
  """

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[*study_guides, prompt]
    )
    logger.info(response.text)
    return response


def parse_test_questions():
    pass
