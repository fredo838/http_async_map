import src.http_async_map as ham


def request_generator():
    for i in range(200):
        yield i

def validate_response_fn(response):
    if response == 200:
        return ham.FailureState.SUCCESS
    elif response in [429]:
        return ham.FailureState.NONFATAL
    else:
        return ham.FailureState.FATAL

if __name__ == "__main__":
    print("Start")
    result = ham.map(request_generator(), validate_response_fn)
    print(result)
    print("End")