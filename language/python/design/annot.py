# annotations


from typing import List, Sequence, Protocol


class IA: pass
class IB(IA): pass

class P(Protocol):
    def h(self) -> List[IA]: ...


class A:
    def f(self) -> List[IA]:
        return [IA()]

    def g(self) -> Sequence[IA]:
        return [IA()]

    def h(self) -> List[IA]:
        return [IA()]


class B(A):
    def f(self) -> List[IB]:
        # NOTE: it is a invalid override in linting.
        return [IB()]

    def g(self) -> Sequence[IB]:
        # NOTE: it is a valid overriding
        return [IB()]

    def h(self) -> List[IB]:
        # NOTE: it is a invalid override in linting.
        # So protocal does not help here
        return [IB()]


# generic 

from typing import Generic, TypeVar, List
# Define a type variable
T = TypeVar('T')
class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()
    def is_empty(self) -> bool:
        return len(self._items) == 0
# Usage
int_stack = Stack[int]()
int_stack.push(1)
int_stack.push(2.)  # NOTE: it is runnable  but does not confirm with linting rules.
print(int_stack.pop())  # Output: 2.0
print(int_stack.pop())  # Output: 1

int_stack = Stack() 
int_stack.push(1)
int_stack.push(2.) 
print(int_stack.pop())  # Output: 2.0
print(int_stack.pop())  # Output: 1
