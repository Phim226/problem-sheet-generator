from pylatex import Command, Document
from pylatex.utils import NoEscape

class Sheet():

    def __init__(
            self, title: str = "",
            file_name: str = "",
            author: str = "",
            date: str = "",
            margin: tuple[str] = ("2.5cm", "2.5cm")
    ):
        self._document: Document = Document(
            geometry_options = {"left": margin[0], "right": margin[1]}
        )

        self._title: str = title

        self._file_name: str = file_name if file_name else title.strip().replace(" ", "_")

        self._fill_preamble(title, author, date)

    @property
    def document(self) -> Document:
        return self._document

    @property
    def title(self) -> str:
        return self._title

    @property
    def file_name(self) -> str:
        return self._file_name

    def _fill_preamble(self, title: str, author: str = "", date: str = "") -> None:
        self._document.preamble.append(Command("title", title))
        self._document.preamble.append(Command("author", author))
        self._document.preamble.append(Command("date", date))
        self._document.append(NoEscape(r"\maketitle"))

"""
class QuestionSheet(Sheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AnswerSheet(Sheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) """
