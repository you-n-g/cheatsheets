# NOTE: more are in data_obj.py file


import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class MyConfig(BaseSettings):
    a: int | None = 1

    model_config = SettingsConfigDict(
        env_prefix="TEST_",
        env_parse_none_str="None",  # NOTE: this is the key to accept None
        # extra="allow",
    )

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if isinstance(obj, dict) and "a" in obj:
            obj = obj.copy()
            if obj["a"] == "None":
                obj["a"] = None
        return super().model_validate(obj, **kwargs)

os.environ["TEST_A"] = "2"

CONF = MyConfig()

print(CONF)


os.environ["TEST_A"] = "None"

CONF = MyConfig()

print(CONF)
