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

class ContextManager():
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

