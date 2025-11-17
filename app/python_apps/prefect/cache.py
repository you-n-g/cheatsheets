import time
from prefect import task
from prefect.cache_policies import TASK_SOURCE, INPUTS


@task(cache_policy=TASK_SOURCE + INPUTS)
def foo(x: int):
    # changing this function will not affect the cache of my_cached_task
    return x + 3


# NOTE: changing the script will not affect the cache.
# But changing the code in the function will invalidate the cache.
@task(cache_policy=TASK_SOURCE + INPUTS)
def my_cached_task(x: int):
    return x + foo(x)

@task(cache_policy=TASK_SOURCE + INPUTS)
def my_cache_with_exception(x: int):
    time.sleep(5)
    raise ValueError("error")


if __name__ == "__main__":
    # even hitting the cache, it will take a while.
    # import time
    # start = time.time()
    # for i in range(10):
    #     print(my_cached_task(2))
    # end = time.time()
    my_cached_task(2)

    t = time.time()
    try:
        my_cache_with_exception(2)
    except ValueError as e:
        print(f"time: {time.time() - t}")

    try:
        print("exception will not be cached")
        my_cache_with_exception(2)
    except ValueError as e:
        print(f"time: {time.time() - t}")
