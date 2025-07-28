import time


def timer(fn: callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(args, kwargs)
        end = time.time()

        print(f"{fn.__name__}의 실행 시간: {end-start:.5f}")
        return result
    return wrapper