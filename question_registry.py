from typing import Dict, Type, TypeVar, Callable
Question = TypeVar("T", bound=type)

QUESTION_REGISTRY: Dict[str, Type[Question]] = {}

def register_question_type(name: str) -> Callable[[Type[Question]], Type[Question]]:
    def wrapper(cls: Type[Question]) -> Type[Question]:
        QUESTION_REGISTRY[name] = cls
        return cls
    return wrapper

def create_question(name: str, topic: str, **kwargs: bool) -> Question:
    cls = QUESTION_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unkown question type: {name}")
    return cls(topic, **kwargs)