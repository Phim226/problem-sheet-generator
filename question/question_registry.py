from __future__ import annotations
from inspect import getfullargspec
from typing import Any, Callable, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from question.question import Question


"""
This is the question registry. The register_question_type function defines
a class decorator that takes a question type name as an input that
registers them in the registry. For example if we wanted to define a new
question type class to create linear algebra questions, we might create the
class

        @register_question_type("linear_algebra")
        class LinearAlgebraQuestion(Question):
            ......
            ......
            ......

When the program is executed then the decorator adds a new entry
("linear_algebra": LinearAlgebraQuestion) to the QUESTION_REGISTRY
dictionary. When the create_question function is called with "linear_algebra"
as an input (with appropriate inputs for topic and **kwargs) then, after
validating that "linear_algebra" is a key in the registry, it will return the
LinearAlgebraQuestion class. Creating a new question class without the
decorator and attempting to use it by calling the create_question function
will result in a ValueError.

The **kwargs in the create_question function represents the full set of
optional inputs across all subclasses of Question. More information about
these optional parameters can be found in the questions.py file in the
appropriate classes. The type hint "bool" refers to the optional parameter
"nested" in the Question class."""

# TODO: Figure out a way of passing appropriate kwargs into each class (kwargs registry?).
# TODO: Write better docstring

QUESTION_REGISTRY: dict[str, Type[Question]] = {}
KEYWORD_REGISTRY: dict[str, Any] = {}

def get_kwargs(func: Callable) -> dict[str, Any]:
    spec = getfullargspec(func)
    kwargs = {key: value for key, value in zip(
        reversed(spec.args),
        reversed(spec.defaults)
        )
    }
    return dict(list(reversed(kwargs.items())))

def register_question_type(name: str) -> Callable[[Type[Question]], Type[Question]]:
    def wrapper(cls: Type[Question]) -> Type[Question]:
        QUESTION_REGISTRY[name] = cls
        KEYWORD_REGISTRY[name] = get_kwargs(cls.__init__)
        return cls
    return wrapper

def create_question(name: str, topic: str, **kwargs: bool) -> Question:
    if name == "question":
        msg = f"{name} is not a valid question type"
        raise ValueError(msg)

    cls = QUESTION_REGISTRY.get(name)
    if cls is None:
        msg = f"Unknown question type: {name}"
        raise ValueError(msg)
    return cls(topic, **kwargs)