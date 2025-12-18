from logging import info
from problem_sheet_generator.app.ui import SheetConfig
from problem_sheet_generator.app.ui import QuestionConfig
from problem_sheet_generator.core.sheet_generator import SheetGenerator
from problem_sheet_generator.core.question import KEYWORD_REGISTRY, QUESTION_REGISTRY
from problem_sheet_generator.utilities import configure_log

# Use this code to bypass GUI.
# TODO: Need to manually create QuestionConfig and pass appropriate arguments to generate() before this code can be used.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    sheet_generator = SheetGenerator(SheetConfig())
    sheet_generator.generate()