from abc import abstractmethod

class Answer():


    def __init__(self):
        pass

    @property
    def answer_latex(self):
        return self._answer_latex


class VectorCalculusAnswer(Answer):

    def __init__(self):
        super().__init__()