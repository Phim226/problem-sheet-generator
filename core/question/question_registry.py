from __future__ import annotations
from inspect import getfullargspec
from typing import Any, Callable, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from question import Question


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
# TODO: Maybe change keyword and topic registry to database tables in sqlite.

QUESTION_REGISTRY: dict[str, Type[Question]] = {}
KEYWORD_REGISTRY: dict[str, Any] = {}
TOPIC_REGISTRY: dict[str, dict[str, list[str]]] = {}
TOPIC_DISPLAY_REGISTRY: dict[str, str] = {}

def get_kwargs(func: Callable) -> dict[str, Any]:
    spec = getfullargspec(func)

    if spec.defaults is None:
        return {}

    kwargs = {key: value for key, value in zip(
        reversed(spec.args),
        reversed(spec.defaults)
        )
    }
    return dict(list(reversed(kwargs.items())))

def register_type() -> Callable[[Type[Question]], Type[Question]]:
    def wrapper(cls: Type[Question]) -> Type[Question]:
        name_id = cls.name[0]
        TOPIC_REGISTRY[name_id] = {}
        TOPIC_DISPLAY_REGISTRY[name_id] = cls.name[1]
        return cls
    return wrapper

def register_question() -> Callable[[Type[Question]], Type[Question]]:
    def wrapper(cls: Type[Question]) -> Type[Question]:
        if not hasattr(cls, "topic"):
            msg = f"{cls} doesn't have the topic attribute"
            raise ValueError(msg)

        topic_id = cls.topic[0]
        QUESTION_REGISTRY[topic_id] = cls
        KEYWORD_REGISTRY[topic_id] = get_kwargs(cls.__init__)

        if hasattr(cls.__base__, "name"):
            TOPIC_REGISTRY[cls.__base__.name[0]].update({topic_id: list(cls.subtopics.keys())})

        TOPIC_DISPLAY_REGISTRY[topic_id] = cls.topic[1]
        TOPIC_DISPLAY_REGISTRY.update(cls.subtopics)
        return cls
    return wrapper

def create_question(topic: str, subtopic: str, **kwargs: bool) -> Question:
    if topic not in list(QUESTION_REGISTRY.keys()):
        msg = f"{topic} is not a valid question type"
        raise ValueError(msg)

    cls = QUESTION_REGISTRY.get(topic)
    if cls is None:
        msg = f"Unknown question type: {topic}"
        raise ValueError(msg)
    return cls(subtopic, **kwargs)