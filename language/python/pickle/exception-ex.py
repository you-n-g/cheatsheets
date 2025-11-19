import pickle
from rich.console import Console

class MyBadRequestError(Exception):
    def __init__(self, message, model, llm_provider):
        super().__init__(message)
        self.model = model
        self.llm_provider = llm_provider

def test_pickle(obj):
    Console().rule("[green]Test Pickle[/green]")

    print("\n=== Original Object ===")
    print(repr(obj))
    print(vars(obj))

    print("\n=== Attempting to pickle object ===")
    data = pickle.dumps(obj)
    print("Pickled OK")

    try:
        unpickled_obj = pickle.loads(data)
        print("\n=== Unpickled Object ===")
        print(repr(unpickled_obj))
        print(vars(unpickled_obj))
    except Exception as e:
        print("Unpickling failed:", e)

exc = MyBadRequestError("Something went wrong", "gpt-3.5", "openai")
test_pickle(exc)

class NormalClass:
    def __init__(self, message, model, llm_provider):
        self.message = message
        self.model = model
        self.llm_provider = llm_provider

normal_obj = NormalClass("All good here", "gpt-4", "openai")
test_pickle(normal_obj)



# this would fix the error
import copyreg
def _reduce_no_init(exc: Exception) -> tuple:
    cls = exc.__class__
    return (cls.__new__, (cls,), exc.__dict__)

# suppose you want to apply this to MyError
copyreg.pickle(MyBadRequestError, _reduce_no_init)

exc = MyBadRequestError("Something went wrong", "gpt-3.5", "openai")
test_pickle(exc)



# Python's exception is very special
oe = OSError(2, "error!!!")
print(f"It does not have {oe.__dict__=}, but it has {oe.errno=}")

