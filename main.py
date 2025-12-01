from logging import info
from tkinter import Tk
from core.question import KEYWORD_REGISTRY, QUESTION_REGISTRY, TOPIC_REGISTRY
from utilities import configure_log
from app import ProblemSheetGeneratorApp

# TODO: Design UI.
# TODO: Make pdf of questions and answers viewable in the app.
# TODO: Temporarily store files and give option to save or export them for permanant storage.
# TODO: Have problem sheet templates with typical collections of questions.
# TODO: Each question topic be configurable.
# TODO: Make core and core.mathematics into packages.
# TODO: Write tests.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")
    info(f"Topic registry: {TOPIC_REGISTRY}")

    root = Tk()

    app: ProblemSheetGeneratorApp = ProblemSheetGeneratorApp(root)
    app.build()

    root.mainloop()