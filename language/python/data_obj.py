"""
This file is designed for showing the usage of some class to manage meaningful data.
What is meaningful data?
- Data typed
- Info
"""
from dataclasses import dataclass, fields
from typing import NamedTuple, Optional, TypedDict
from pprint import pprint


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

from pydantic import BaseModel, BaseSettings, Extra

# ## Outlines: normal nested

class Nested(BaseSettings):
    text: str = "hello"
    good_boy: str = "james"

    # class Config:
    #     env_nested_delimiter = '_'
    # class Config:
    #     extra = Extra.allow

class MyConfig(BaseSettings):
    top_level: str = "foo"
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '_'
        # env_nested_delimiter = '__'
        # extra = Extra.ignore
        # extra = Extra.allow


# ## Outlines: read from env
os.environ["TOP_LEVEL"] = "env_bar"
os.environ["NESTED_TEXT"] = "env_world"
# os.environ["NESTED__GOOD_BOY"] = "env_boy"


config = MyConfig()

print(config)

assert config.top_level == "env_bar"
assert config.nested.text == "env_world"

# exit()

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


# ## Outlines: test extra
# pydantic can't handle when nested delimiter appear in the naming.
# - Following code can't will raise validation error
# os.environ["NESTED_GOOD_BOY"] = "env_boy"
# config = MyConfig(_env_file=_env_file)
# print(config)
# assert config.top_level == "file_bar"
# assert config.nested.text == "env_world"  # the nested setting can't read _env_file recursively


# ## Outlines: BUG setting..

# The following code will raise error...if we use `GOOD_BOY` instead of `good_boy`
# - related issue https://github.com/pydantic/pydantic/issues/4599
from pydantic import BaseSettings, BaseModel


# Version1:  all lower case
class Nested(BaseSettings):
    good_boy: str = "james"


class MyConfig(BaseSettings):
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '__'


os.environ["NESTED__GOOD_BOY"] = "env_boy"
config = MyConfig()
print(config)

# Version 2: case sensitive works
class Nested(BaseSettings):
    GOOD_BOY: str = "james"


class MyConfig(BaseSettings):
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '__'
        case_sensitive = True


os.environ["nested__GOOD_BOY"] = "env_boy_v02"
config = MyConfig()
print(config)
del os.environ["nested__GOOD_BOY"]   # this will override


# Version3:  BaseModel does not solve this issue...
class Nested(BaseModel):
    GOOD_BOY: str = "james"

class MyConfig(BaseSettings):
    nested: Nested = Nested()


    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '__'


os.environ["NESTED__GOOD_BOY"] = "env_boy_v03"
config = MyConfig()
print(config)


# Version4: maybe we should use BaseModel for the nested setting
class Nested(BaseModel):
    good_boy: str = "james"


class MyConfig(BaseSettings):
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '__'


os.environ["NESTED__GOOD_BOY"] = "env_boy_v04"
config = MyConfig()
print(config)


# Version final:
# - BaseModel for nested setting is a more standard implementation
# - all environments are automatically converted to lower case, so the varaiable name should align with it.
class Nested(BaseModel):
    good_boy: str = "james"


class MyConfig(BaseSettings):
    nested: Nested = Nested()

    class Config:
        # env_prefix = "MY_"  # the prefix can't be mixed with the `env_nested_delimiter`
        env_nested_delimiter = '__'

os.environ["NESTED__GOOD_BOY"] = "env_boy"
config = MyConfig()
print(config)

