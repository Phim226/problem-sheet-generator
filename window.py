from logging import info
from tkinter import Tk
from core.question.question_registry import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log
from app.app import ProblemSheetGeneratorApp
from core.sheet_generator import SheetGenerator

# TODO: Design UI.
# TODO: Make pdf of questions and answers viewable in the app.
# TODO: Temporarily store files and give option to save or export them for permanant storage.
# TODO: Have problem sheet templates with typical collections of questions.
# TODO: Each problem sheet stored in a ProblemSheet object containing #questions, question topics etc.
# TODO: Each question topic be configurable.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    root = Tk()

    generator: SheetGenerator = SheetGenerator()

    app: ProblemSheetGeneratorApp = ProblemSheetGeneratorApp(root, generator)
    app.build()

    root.mainloop()