QUESTION_REGISTRY = {}

def register_question_type(name: str):
    def wrapper(cls: type):
        QUESTION_REGISTRY[name] = cls
        return cls
    return wrapper

def create_question(name, topic, **kwargs):
    cls = QUESTION_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unkown question type: {name}")
    return cls(topic, **kwargs)