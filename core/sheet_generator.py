from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.ui import SheetConfig
    from app.ui import QuestionConfig
from logging import error, info
from os import remove
from os.path import exists
from pathlib import Path
from subprocess import CalledProcessError
from random import choice
from pylatex import Document, Enumerate
from core.sheet import Sheet
from core.question import create_question, TOPIC_REGISTRY, Question


# TODO: Include docstrings
# TODO: Update name of files to delete based on inputted filenames
class SheetGenerator():


    def __init__(self, config: SheetConfig):
        self._question_sheet: Sheet = Sheet(
            title = config.problem_title,
            file_name = config.problem_filename,
            author = config.author,
            date = config.date,
            margin = (config.margin_left, config.margin_right)
        )
        self._answer_sheet: Sheet = Sheet(
            title = config.answer_title,
            file_name = config.answer_filename,
            author = config.author,
            date = config.date,
            margin = (config.margin_left, config.margin_right)
        )

    def _choose_random_topic_and_subtopic(self, question_type: str) -> tuple[str]:
        topics: dict[str, list[str]] = TOPIC_REGISTRY[question_type]
        topic = choice(list(topics.keys()))
        return topic, choice(topics[topic])

    # TODO: Change the names of the output files to include the creation date.
    def generate(
            self,
            selected_questions: list[QuestionConfig],
            generate_tex: bool = True
    ) -> None:
        questions_doc = self._question_sheet.document

        answers_list = []
        with questions_doc.create(Enumerate()) as enum:
            for selected_q in selected_questions:
                for _ in range(selected_q.num_questions):
                    topics = [topic for topic in selected_q.topics]

                    if topics[1] is None:
                        topics[1], topics[2] = self._choose_random_topic_and_subtopic(topics[0])

                    elif topics[2] is None:
                        topics[2] = choice(TOPIC_REGISTRY[topics[0]][topics[1]])

                    else:
                        # When the subtopic comes from the QuestionConfig then it has the topic tacked
                        # to the front to avoid conflicts in the question selection tree, so needs to
                        # be removed.
                        topics[2] = topics[2].replace(f"{topics[1]}_", "")

                    question: Question = create_question(
                        topics[1],
                        topics[2]
                    )
                    enum.add_item(question.question)
                    answers_list.append(question.answer)
                    info(f"Answer: {question.answer}")

        answers_doc = self._answer_sheet.document

        with answers_doc.create(Enumerate()) as enum:
            for answer in answers_list:
                enum.add_item(answer)

        try:
            self._generate_output_files(questions_doc, self._question_sheet.file_name, not generate_tex)
            self._generate_output_files(answers_doc, self._answer_sheet.file_name, not generate_tex)
        except CalledProcessError as e:
            msg = (
                " LaTeX failed to process. This is most likely due to a mistake in the LaTeX syntax,"
                " the output files can't be overwritten or an issue with your LaTeX installation"
                " (such as not having Perl installed). See the log file for more details.\n\nAn"
                " attempt will now be made to delete the output files to prevent issues when"
                " rerunning the code."
            )
            error(f"{type(e).__name__}:{msg}")

            self._delete_files()

        info("Generation complete.")

    @staticmethod
    def _generate_output_files(document: Document, name: str, clean_tex: bool = False) -> None:
        if exists("output"):
            document.generate_pdf(f"output/{name}", clean_tex = clean_tex)
            return

        path = Path("output")
        path.mkdir(exist_ok = True)
        document.generate_pdf(f"output/{name}", clean_tex = clean_tex)

    # TODO: Files to delete need to reference output files name. Currently hardcoded.
    @staticmethod
    def _delete_files():
        files = [
            "output/questions.fdb_latexmk", "output/questions.pdf", "output/questions.tex",
            "output/answers.fdb_latexmk", "output/answers.pdf", "output/answers.tex"
        ]
        for file in files:
            try:
                remove(file)
            except PermissionError as e:
                msg = (
                    " is being used by other processes and cannot be deleted. Close it before"
                    " attempting to rerun the problem sheet generation process."
                )
                error(f"{type(e).__name__}: {file}{msg}")
            except FileNotFoundError:
                continue


