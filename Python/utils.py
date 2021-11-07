from itertools import tee
from typing import Iterable
def split_on_condition(seq, condition):
    l1, l2 = tee((condition(item), item) for item in seq)
    return (i for p, i in l1 if p), (i for p, i in l2 if not p)

from itertools import cycle
class XorLike:
    def __init__(self, first_key, values):
        self.cur_key = first_key
        self.cur_val = next(iter(values))
        self.vals_iter = cycle(values)
    
    def get(self, key):
        if key != self.cur_key:
            self.cur_key = key
            return next(self.vals_iter)

from ast import literal_eval
def str_to_obj(s, t):
    """transform str of a given object (created usually via print(obj)) into this object

    Args:
        s (str):
        t (type): python type

    Returns:
        [t]: object of type `t`  if literal_eval didn't fail, else None
    """
    try:
        d = literal_eval(s.strip())
    except (ValueError, SyntaxError):
        pass
    else:
        if isinstance(d, t):
            return d
    return None

import json
# returns list of all unique dicts (checks both key and value)
# TODO: check time against simple check
unique_dicts = lambda *dicts: [json.loads(x) for x in {json.dumps(d) for d in dicts}]

# returns the first element in l where f(element) is not false
first_true = lambda l, fun: next((v for v in l if fun(v)), False)

# transform string of HTML headers to dict
parse_headers = lambda st: dict((line.split(': ', 1) for line in st.split('\n') if line))

# Make a class a Singleton class (only one instance)
def singleton(cls):
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

def phone_format(s, country_code='972'):
    """transform string into a phone number in global format

    Args:
        s (str): string containing phone number
        country_code (str, optional): country code (prefix). Defaults to '972'.

    Returns:
        [str]: phone number in global format
    """
    s = ''.join(c for c in s if c.isdigit())
    if s.startswith('0'):
        s = country_code + s[1:]
    return s

import datetime, pytz
# transform datetime.datetime object to localtime
localize_time = lambda date, tz='Asia/Jerusalem': pytz.timezone(tz).localize(date)

def pretty_print_dict(d, indent=0):
    """pretty print (nested) dictionary

    Args:
        d (dict): 
        indent (int, optional): ignore, for recursion perposes. Defaults to 0.
    """
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print_dict(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

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

def _dict_merge(dct, merge_dct, add_keys=True, dct_values = False):
    """
    Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.

    slightly updated version for the implementation of @DomWeldon and @angstwad
    from this thread: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

    This version will return a (deep) copy of the dictionary and leave the original
    arguments untouched.

    The optional argument ``add_keys``, determines whether keys which are
    present in ``merge_dict`` but not ``dct`` should be included in the
    new dict.

    The optional argument ``dct_values``, determines whether keys which are
    present in both dicts will reserve the value assosiated with them
    in ``dict`` (True) or ``merge_dct`` (False).

    Args:
        dct (dict) onto which the merge is executed
        merge_dct (dict): dct merged into dct
        add_keys (bool): whether to add new keys
        dct_values (bool): which values to overwrite

    Returns:
        dict: updated dict
    """
    if not add_keys:
            merge_dct = {
                k: merge_dct[k]
                for k in set(dct).intersection(set(merge_dct))
            }

    for k, v in merge_dct.items():
        if isinstance(dct.get(k), dict) and isinstance(v, collections.Mapping):
            dct[k] = _dict_merge(dct[k], v, add_keys=add_keys, dct_values=dct_values)
        else:
            dct[k] = v
    return dct

from functools import wraps
from time import time
from datetime import datetime
def measure(method):
    """wrapper for measuring execution time
    stolen from the great Uriel Hai
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        mname = method.__name__
        s = time()
        print(f"Start  {mname} at: {datetime.now()}")
        res = method(*args, **kwargs)
        e = time()
        mins, secs = divmod(e - s, 60)
        print(f"Finish {mname} at: {datetime.now()}")
        print(f"Total time of {mname}: {mins:02.0f}:{secs:05.2f}s")

        return res

    return wrapper

from functools import wraps
from time import time
def timeit(method):
    @wraps(method)
    def wrapper(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result 
    return wrapper

from threading import Thread
from multiprocessing import Queue
import time
def run_with_limited_time(func, args, kwargs, time_limit):
    """Runs a function with time limit
    :param func: The function to run.
    :param args: The functions args, given as tuple.
    :param kwargs: The functions keywords, given as dict.
    :param time_limit: The time limit in seconds (can be float).
    :return: A tuple: The function's return value unchanged, and the running time for the function.
    :raises PlayerExceededTimeError: If player exceeded its given time.
    """
    def run_measure_time(func, args, kwargs, result_queue):
        """Runs the given function and measures its runtime.
        :param func: The function to run.
        :param args: The function arguments as tuple.
        :param kwargs: The function kwargs as dict.
        :param result_queue: The inter-process queue to communicate with the parent.
        :return: A tuple: The function return value, and its runtime.
        """
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except MemoryError as e:
            result_queue.put(e)
            return

        runtime = time.time() - start
        result_queue.put((result, runtime))

    q = Queue()
    t = Thread(target = run_measure_time, args = (func, args, kwargs, q))
    t.start()

    # This is just for limiting the runtime of the other thread, so we stop eventually.
    # It doesn't really measure the runtime.
    t.join(time_limit)

    if t.is_alive():
        raise ExceededTimeError

    q_get = q.get()
    if isinstance(q_get, MemoryError):
        raise q_get
    return q_get

import os, zipfile
def create_zipdir(path, archive_name=None):
    """
    Zips an entire directory tree.
    The archive will be placed beside the directory. For example, given a
    path of `foo/bar/baz/`, this function will create `foo/bar/baz.zip`.
    :param path: Path of the directory to zip.
    :param archive_name: The name of the archive to create. By default it's
        None, which means use the name of the zipped folder.
    :return: Path of the created archive.
    """
    path_dirname = os.path.dirname(path)
    path_basename = os.path.basename(path)

    if archive_name is None:
        archive_name = path_basename

    archive_path = f'{os.path.join(path_dirname, archive_name)}.zip'

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(path):
            arch_root = os.path.relpath(root, path_dirname)

            for file in files:
                file_path = os.path.join(root, file)
                arch_path = os.path.join(arch_root, file)

                ziph.write(file_path, arch_path)

    return archive_path

class AvgrageMeter(object):
    def __init__(self, name = ''):
        self.reset()
        self._name = name

    def reset(self):
        self.avg = 0
        self.sum = 0
        self.cnt = 0

    def update(self, val, n = 1):
        self.sum += val * n
        self.cnt += n
        self.avg = self.sum / self.cnt

    def __str__(self):
        return "%s: %.5f" % (self._name, self.avg)

    def __repr__(self):
        return self.__str__()


from flask import Flask
import logging
def create_flask_app():
    app = Flask(__name__, instance_relative_config=False)

    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    app.logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(app.config["LOG_FILE"])
    file_handler.setFormatter(log_formatter)
    app.logger.addHandler(file_handler)

    from views import views_bp
    app.register_blueprint(views_bp)
    app.logger.info("app created!")
    return app

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
def run_flask_with_sched():

    sched = BackgroundScheduler()
    sched.add_job(lambda: print('test'),'cron',second='*')
    sched.start()

    def OnExitApp(user):
        sched.shutdown()
        print("exit Flask application")
    atexit.register(OnExitApp, user='user')
    
    app = create_flask_app()
    app.run(host="0.0.0.0")#, debug=True)

import functools, pickle, os
def check_local(func=None, *, filename=None):
    def wrapper(func):
        nonlocal filename
        if filename is None:
            filename = func.__name__+'.pkl'
        
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if os.path.exists(filename):
                try:
                    with open(filename, 'rb') as f:
                        return pickle.load(f)
                except:
                    pass
            res = func(*args, **kwargs)
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(res, f)
            except pickle.PicklingError:
                os.remove(filename)
            return res
        return inner
    return wrapper if func is None else wrapper(func)

import requests, shutil
def download_image(image_url):
    filename = image_url.rsplit("/")[-1]
    r = requests.get(image_url, stream = True) # stream = True to guarantee no interruptions
    r.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero.  
    with open(filename,'wb') as f:  
        shutil.copyfileobj(r.raw, f)
    
from tqdm import tqdm
import requests
def download_with_progress_bar(url, out_file):
    url = "http://www.ovh.net/files/10Mb.dat"
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(out_file, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR")

import pandas as pd
def all_csvs_to_dataframe(path):
    return pd.contact(pd.read_csv(f) for f in path.glob("*.csv"))

import pandas as pd
class CsvPandas:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self._df = pd.read_csv(filepath)
    
    def __call__(self):
        return self._df
    
    def __del__(self):
        self._df.to


from collections import Counter, OrderedDict
class OrderedCounter(Counter, OrderedDict):
    pass


from apscheduler.schedulers.background import BackgroundScheduler
def set_apscheduler():
    sched = BackgroundScheduler(daemon=True)
    #---\set scheduler job#
    

    #----/end#
    sched.start()

    sched.shutdown()

import sys
def sound_alarm(seconds=1, hz_freq=440):
    if sys.platform.startswith('win32'):
        import winsound
        winsound.Beep(hz_freq, seconds*1000)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # linux - sudo apt install sox
        # mac - sudo port install sox
        import os
        os.system(f'play -nq -t alsa synth {seconds} sine {hz_freq}')

import os
def say_someting(s: str):
    if sys.platform.startswith('darwin'):
        os.system('say '+s)
    elif sys.platform.startswith('linux'):
        # sudo apt install speech-dispatcher
        os.system('spd-say '+s)

get_attrs = lambda o: list(('Method' if callable(getattr(o, a)) else 'Attribute', a) for a in dir(o) if not a.startswith('__'))

def remove_prefix(dir_name):
    import os
    for filename in os.listdir(dir_name):
        pre, suf = filename.split(' ',1) 
        new_name = f'{pre:0>3}' + ' ' + suf
        os.rename(os.path.join(dir_name, filename), os.path.join(dir_name, new_name))


def breadth_first_search(start, is_goal, get_neighbors):
    """BFS for a graph. credit: https://johnlekberg.com/blog/2020-01-01-cabbage-goat-wolf.html"""
    parent = dict()
    to_visit = [start]
    discovered = set([start])

    while to_visit:
        vertex = to_visit.pop(0)

        if is_goal(vertex):
            path = []
            while vertex is not None:
                path.insert(0, vertex)
                vertex = parent.get(vertex)
            return path

        for neighbor in get_neighbors(vertex):
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = vertex
                to_visit.append(neighbor)

from typing import Iterable
def pprint_iterable(d: Iterable, indent=0):
  print(' - ' * indent)
  for i in d:
    if isinstance(i, Iterable):
       pprint_iterable(i, indent+1)
    else:
     print(' - ' * (indent+1) + str(i))

from typing import Iterable, Union
def test_regex(pattern: str, s: str) -> Union[None, str]:
    import re
    res = re.search(pattern, s)
    return res[0] if res is not None else None

from typing import Callable, Sequence, Generator
split_chuncks: Callable[[Sequence, int], Generator[Sequence, None, None]] = \
    lambda l, n: (l[i: i+n] for i in range(0, len(l), n))


import enum
# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4
def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes


from itertools import islice, takewhile, repeat
split_every = (lambda n, it:
    takewhile(bool, (list(islice(it, n)) for _ in repeat(None))))

from typing import List
import glob, os

def get_all_paths(root: str) -> List[str]:
    pattern = os.path.join(root, "**", "*")
    return [name for name in glob.glob(pattern, recursive=True)] 