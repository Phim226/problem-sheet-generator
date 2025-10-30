from logging import info
from tkinter import Button, Tk
from main import create_document
from question.question_registry import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log

if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")
    root = Tk()
    root.title("Problem Sheet Generator")
    root.geometry("500x500")

    button = Button(
        root,
        text = "Generate Problem Sheet",
        command = create_document
    )
    button.grid()

    root.mainloop()