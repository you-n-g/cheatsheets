# %% [markdown]
# # Outlines: pydantic
# pip install pydantic
# advantage
# - auto type conversion
# - auto env reading
print("Pydantic " + "-" * 30)

from pathlib import Path
DIRNAME = Path(__file__).absolute().resolve().parent
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings

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

print(f"{config=}")

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

class MyConfigFile(BaseSettings):
    top_level: str = "foo"
    nested: Nested = Nested()

    class Config:
        env_nested_delimiter = '_'
        env_file = str(_env_file)
        extra = "allow"

config = MyConfigFile()
assert config.top_level == "file_bar"
assert config.nested.text == "file_world"  # the nested setting can't read _env_file recursively

# ## Outlines: read from env file but override by env


os.environ["NESTED_TEXT"] = "env_world"
config = MyConfigFile()
assert config.top_level == "file_bar"
assert config.nested.text == "env_world"  # the nested setting can't read _env_file recursively
del os.environ["NESTED_TEXT"]


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


# # Outlines: solve the inheritance issue with different outlines.

from rich.console import Console
console = Console()
console.rule("[bold red]Test Inehrience")

from pydantic_settings import PydanticBaseSettingsSource, EnvSettingsSource, SettingsConfigDict


class EnvExtBaseSettings(BaseSettings):

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # 1) walk from base class
        parent_env_settings = []
        def base_iter(settings_cls):
            for cl in settings_cls.__bases__:
                if issubclass(cl, EnvExtBaseSettings) and cl is not EnvExtBaseSettings:
                    yield cl
                    yield from base_iter(cl)
        # 2) Build EnvSettingsSource from base classes, so we can add parent Env Sources
        for base_cls in base_iter(settings_cls):
            parent_env_settings.append(
                EnvSettingsSource(
                    base_cls,
                    case_sensitive=base_cls.model_config.get('case_sensitive'),
                    env_prefix=base_cls.model_config.get('env_prefix'),
                    env_nested_delimiter=base_cls.model_config.get('env_nested_delimiter'),
                ))
        return init_settings, env_settings, *parent_env_settings, dotenv_settings, file_secret_settings


class ExSetBase(EnvExtBaseSettings):
    # class ExSetBase(BaseSettings):
    a: str = "default_a"
    model_config = SettingsConfigDict(env_prefix = "BASE_")

class ExSetSub(ExSetBase):
    b: str  = "default_b"
    model_config = SettingsConfigDict(env_prefix = "SUB_")

os.environ["BASE_A"] = "base_mod_a"
os.environ["SUB_B"] = "sub_mod_b"
print(ExSetBase())
print("=" * 20)
print(ExSetSub())
os.environ["SUB_A"] = "sub_mod_a"
print("=" * 20)
print(ExSetSub())

del os.environ["BASE_A"], os.environ["SUB_B"], os.environ["SUB_A"]

# # Outlines: outlines

console.rule("[bold red]Test inehritance with validator")
from pydantic import BaseModel, ValidationInfo, field_validator


class TextModel(BaseModel):
    text: str
    test2: str

    @field_validator('text', mode='after')
    @classmethod
    def remove_stopwords(cls, v: str, info: ValidationInfo) -> str:
        print("Even after mode, you got nothing", info.data)
        return "reset value"


print(TextModel(text="hello", test2="foo"))

class TextModel2(BaseModel):
    text: str

class TextModel2Sub(TextModel2):
    test2: str = ""

class TextModel2SubSub(TextModel2Sub):
    test3: str

    @field_validator('test2', mode='after')
    @classmethod
    def test2_val(cls, v: str, info: ValidationInfo) -> str:
        print("Even after mode, you got nothing in test2", info.data)
        return "reset value"

    @field_validator('test3', mode='after')
    @classmethod
    def test3_val(cls, v: str, info: ValidationInfo) -> str:
        print("Even after mode, you got nothing in test3", info.data)
        return "reset value"

print(TextModel2SubSub(text="hello", test2="foo", test3="bar"))
print(TextModel2SubSub(text="hello", test3="bar"))  # this will not trigger test2_val

print("*" * 10)
