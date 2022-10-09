from dataclasses import dataclass, fields
from typing import NamedTuple, Optional, TypedDict


# # Outlines: TypedDict

class MyClass(TypedDict):
    a: int = 1
    b: int = 10
    v: Optional[int] = None

mc = MyClass()

mc == {}
# mc["a"]   # Raise KeyError


# # Outlines: NamedTuple
class Employee(NamedTuple):
    name: str
    id: int = 3
    extra_info = None

e = Employee(name=3)

e.id  # provides default value
# e.__dict__  # NamedTuple can't have ___dict__ (but dataclass can have)

try:
    e = Employee()
except TypeError as exc:
    print("Missing default value")
    print(exc)

e2 = e._replace(name="new_name")

print(f"e1: {e2}")
print(f"{e} will not changed with e2")


# # Outlines: dataclass

@dataclass
class Emp:
    name: str
    id: int = 3

e = Emp('shit')
e.id = 4

e2 = Emp('good')
e2.__dict__


e3 = Emp("good", id=None)

e3


class EmpChildWrong(Emp):
    child: str


e4 = EmpChildWrong("good")  # child will not be a force name

@dataclass
class EmpChildRight(Emp):
    child: str = "happy"

ec2 = EmpChildRight("not")

ec2

dir(EmpChildRight)
EmpChildRight.__dict__

fields(EmpChildRight)[0].type


# %% [markdown]
# # Outlines: pydantic
# pip install pydantic
# advantage
# - auto type conversion
# - auto env reading

from pathlib import Path
DIRNAME = Path(__file__).absolute().resolve().parent
import os

from pydantic import BaseModel, BaseSettings

# ## Outlines: normal nested

class Nested(BaseSettings):
    text: str = "hello"

class MyConfig(BaseSettings):
    top_level: str = "foo"
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '_'


# ## Outlines: read from env
os.environ["TOP_LEVEL"] = "env_bar"
os.environ["NESTED_TEXT"] = "env_world"

config = MyConfig()

print(config)

assert config.top_level == "env_bar"
assert config.nested.text == "env_world"


del os.environ["TOP_LEVEL"]
del os.environ["NESTED_TEXT"]


# ## Outlines: read from env file
_env_file = DIRNAME / "pydantic_env"
with _env_file.open("w") as f:
    f.write("""TOP_LEVEL=file_bar
NESTED_TEXT=file_world""")

config = MyConfig(_env_file=_env_file)
assert config.top_level == "file_bar"
assert config.nested.text == "file_world"  # the nested setting can't read _env_file recursively

# ## Outlines: read from env file but override by env


os.environ["NESTED_TEXT"] = "env_world"
config = MyConfig(_env_file=_env_file)
assert config.top_level == "file_bar"
assert config.nested.text == "env_world"  # the nested setting can't read _env_file recursively
