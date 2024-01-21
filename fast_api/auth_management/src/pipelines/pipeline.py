from inspect import isclass, iscoroutine
from typing import List, Callable, Union
from functools import reduce

### source : https://github.com/henningway/python-pipeline

class Pipe:
    def handle(self, content, next):
        pass

CallablePipe = Callable
PipeType = Union[CallablePipe, Pipe]

class Pipeline:
    def __init__(self, passable=None):
        self.pipes = []
        self.passable = passable

    def through(self, pipes: List[PipeType]):
        self.pipes.extend(pipes)
        return self

    def prepare(self):
        def resolve_handler(pipe: PipeType):
            if isclass(pipe):
                pipe = pipe()

            if hasattr(pipe, 'handle'):
                return pipe.handle

            return pipe

        pipeline = [resolve_handler(pipe) for pipe in self.pipes]

        # serves as initial "next" function
        def identity(x):
            return x

        def pack_next(stack, pipe):
            def next(carry):
                return pipe(carry, stack)

            return next

        pipeline = reduce(pack_next, pipeline[::-1], identity)

        return pipeline

    def run(self):
        pipeline = self.prepare()
        return pipeline(self.passable)

    async def run_async(self):
        pipeline = self.prepare()
        result = pipeline(self.passable)

        while iscoroutine(result):
            result = await result

        return result