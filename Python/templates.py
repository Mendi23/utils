# simple singleton class to be inherited
class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class Iterable:
    def __iter__(self):
        pass
    def __next__(self):
        pass

    # you can also implement __getitem__ instead

class Subscribable:
    def __getitem__(self, index):
        pass
    def __setitem__(self, index, data):
        pass

# metaclass template
class Meta(type):
    def __new__(cls, what, bases=None, dct=None):  
        return type.__new__(cls, what, bases, dct)

from contextlib import ContextDecorator
class ContextManager(ContextDecorator):
    def __init__(self):
        print('init method called')
          
    def __enter__(self):
        print('enter method called')
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exit method called')

from contextlib import contextmanager
@contextmanager
def get_scope():
    """Provide a transactional scope around a series of operations."""
    item = get_items()
    try:
        yield item
        item.commit()
    except:
        item.rollback()
        raise
    finally:
        item.close()

class scope:
    def __init__(self):
        self.item = get_items()

    def __enter__(self):
        return self.item

    def __exit__(self, type, value, traceback):
        pass

import time
from typing import Callable
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
def partial_router_fastapi():
    class TimedRoute(APIRoute):
        def get_route_handler(self) -> Callable:
            original_route_handler = super().get_route_handler()

            async def custom_route_handler(request: Request) -> Response:
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                print(f"route duration: {duration}")
                print(f"route response: {response}")
                print(f"route response headers: {response.headers}")
                return response

            return custom_route_handler

    app = FastAPI()
    router = APIRouter(route_class=TimedRoute)

    @app.get("/")
    async def not_timed():
        return {"message": "Not timed"}

    @router.get("/timed")
    async def timed():
        return {"message": "It's the time of my life"}

    app.include_router(router)