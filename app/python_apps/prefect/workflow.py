#!/usr/bin/env -S uv run --no-project --with prefect python
from prefect import flow, task

@task
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

@flow
def my_flow():
    result = say_hello("Prefect")
    print("Flow result:", result)

if __name__ == "__main__":
    my_flow()
