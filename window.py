from logging import info
from tkinter import Tk
from main import create_document
from question.question_registry import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log
from app.app import ProblemSheetGeneratorApp

# TODO: Design UI.
# TODO: Add number of questions functionality.
# TODO: Make pdf of questions and answers viewable in the app.
# TODO: Temporarily store files and give option to save or export them for permanant storage.
# TODO: Have problem sheet templates with typical collections of questions.
# TODO: Each problem sheet stored in a ProblemSheet object containing #questions, question topics etc.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    root = Tk()

    app = ProblemSheetGeneratorApp(root)
    app.build()

    """ button = Button(
        root,
        text = "Generate Problem Sheet",
        command = create_document
    )
    button.grid() """

    root.mainloop()