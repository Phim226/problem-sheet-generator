from logging import info
from app.ui import SheetConfig
from app.ui import QuestionConfig
from core.sheet_generator import SheetGenerator
from core.question import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log

# Use this code to bypass GUI.
# TODO: Need to manually create QuestionConfig and pass appropriate arguments to generate() before this code can be used.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    sheet_generator = SheetGenerator(SheetConfig())
    sheet_generator.generate()