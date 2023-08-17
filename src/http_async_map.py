import asyncio 
import aiohttp
import uuid
import time
from enum import Enum

class FailureState(Enum):
    SUCCESS = 0
    NONFATAL = 1
    FATAL = 2

class Memory:
    def __init__(self, ) -> None:
        self.generator_done = False
        self.generated = 0
        self.history = []
        self.guessed_capacity = asyncio.Semaphore(100)
        self.aborted = []
        self.processed = []
        

class Attempt:
    def __init__(self, request) -> None:
        self.request = request
        self.attempt = 1
        self.create_time = time.time()
        

async def make_request(memory, session, request, attempt, validate_response_fn):
    print("Sleeping")
    start_time = time.time()
    await asyncio.sleep(1.0)
    response = 200
    failure_state = validate_response_fn(response)
    if failure_state == FailureState.NONFATAL:
        memory.aborted.append((request, attempt, start_time))
    else:
        memory.processed.append((attempt.request, attempt.response, attempt.attempt))
    memory.guessed_capacity.release()
    print("Slept")
    return

def check_if_done(memory):
    return len(memory.in_flight) == 0 and memory.generator_done


async def requester_with_session(memory, session, request_generator, validate_response_fn):
    while True:
        await memory.guessed_capacity.acquire()
        try:
            next_request = next(iter(request_generator))
            task = asyncio.create_task(make_request(memory, session, next_request, 1, validate_response_fn))
        except StopIteration:
            memory.generator_done = True


async def requester(memory, request_generator, validate_response_fn):
    async with aiohttp.ClientSession() as session:
        return await requester_with_session(memory, session, request_generator, validate_response_fn)

async def printer():
    await asyncio.sleep(1)

# async def guesser(memory):
#     memory.history = []

async def main(memory, request_generator, validate_response_fn):
    requester_coroutine = requester(memory, request_generator, validate_response_fn)
    asyncio.create_task(printer())
    # all_coroutines = asyncio.gather(scheduler_coroutine, printer())
    return await requester_coroutine

def map(request_generator, validate_response_fn):
    memory = Memory()
    main_coroutine = main(memory, request_generator, validate_response_fn)
    asyncio.run(main_coroutine)
