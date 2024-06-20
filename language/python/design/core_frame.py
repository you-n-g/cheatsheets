"""
# We'll check the design with `ruff check` &  `mypy`

"""
from typing import Generic, TypeVar

ASpecificBaseTask = TypeVar("ASpecificBaseTask", bound="BaseTask")
# Define a type, that refer to a more specific subclass than general `BaseTask`


# Core Framework
class BaseTask:
    ...


class BaseSolver(Generic[ASpecificBaseTask]):
    """
    From a semantic perspective,
    It defines a framework. But it is not designed to handle general BaseTask.
    Instead, it is designed to handle a specific subclass of BaseTask (But all kinds of specific subclasses can be handled in this class).
    """

    def g(self, a: ASpecificBaseTask) -> ASpecificBaseTask:
        return a


# concrete framework
class MTask(BaseTask):
    ...


class MSolver(BaseSolver[MTask]):

    def g(self, a: MTask) -> MTask:
        """`MSolver.g` only works when a is MTask"""
        return a


ms = MSolver()
print(isinstance(ms, BaseSolver))  # it will not affect the type checking
