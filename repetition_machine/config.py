from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    repeatInt : int = 100
    repeatHitInt : int = 40