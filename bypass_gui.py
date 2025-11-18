from logging import info
from app.ui.question_configurer import SheetConfig
from core.sheet_generator import SheetGenerator
from core.question.question_registry import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log

# Use this code to bypass GUI.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    sheet_generator = SheetGenerator(SheetConfig())
    sheet_generator.generate()