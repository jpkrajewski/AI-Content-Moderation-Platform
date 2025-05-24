from pydantic import BaseModel


def list_pydantic_to_list_dict(list_: list[BaseModel]) -> list[dict]:
    return [o.model_dump() for o in list_]
