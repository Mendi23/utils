## Better commands
```python
a = b or c # a = b if b else c
iter(v, sentinel) # for i in v(): if i != v...
''.join(['he', 'llo w', 'orld!']) # better than += on every iteration
collections.ChainMap(dict1, dict2) # dict1.copy().update(dict2)
x, y = y, x+y # t = x+y; x = y; y = t
for i in islice(items, 10) # for j,i in enumerate(items):; if i == 10: break
yield from func(...) # for i in func(...): yield i
l[::i] # every i'th value of l
a = l[:] # a = l.copy()
a = l[::-1] # a = reversed(l)
head, *tail = co # head, tail = co[1], co[1:]
(a, b)[int(f(x))].append(y) # if f(x): a.append(y); else: b.append(y)
[j for i in iter1 for j in fun_iter(i)] # res=[]; for i in iter1: for j in fun_iter(i); res.append(j) 
s.rsplitp(sep)[-1] # s.splitp(sep)[-1]
a == b == c != d > e # can have multiple comparisons
['yes' if v is True else 'no' if v is False else 'unknown' for v in values] # multiple if's
if any((v:=f(n)) is False for n in l): print(f"{v} is not good") # retrieve the "witness" to the failure of the condition
g: typing.Annotaed[int, "meters"] # add metadata to types
```

## New commands
```python
next((v for v in l if fun(v)), False) # first_true = [v for v in l if fun(v)][0]
next((i for i,v in enumerate(l) if fun(v)), False) # index_first_true = [v for v in l if fun(v)][0]
accumulate(repeat(x), lambda fx,_: f(fx)) # iterate[3] = f(f(f(x))))
zip(*l) # transpose(l)
```
[cheasheet](https://jyoti05iitd.medium.com/python-pandas-cheat-sheet-30-functions-methods-b1176f2e37da)

## Good to know
```python
dir(obj) # shows all attributes of obj
help(mod) # shows help string for mod
func(/, ...) # only allow positional arguments after /
func(*, ...) # only allow keyword arguments after *
key, val = dict.popitem() # atomic operation! remove and return last inserted
getattr, hasattr, setattr # allows dynamic attributes
compile(source, filename, mode) # compile a string to code (in order to execute it)
divmod(a,b) # returns both quotient and remainder
chr, ord # map integer and unicode characters
# str functions
str.partition(sub_string) # better than using str.split when splitting in two
str.count(sub_string) # count occurrences in string
str.zfill(length) # left-pad with zeroes
str.title() # capitalize first letter of each word
def f(): pass; f.x = 5 # function attributes can be used for internal states
```

## itertools
```python
cycle(iterable) # cyclic iterable
islice(...) # lazy slice from a sequence
count([start[, step]]) # infinite count
tee(iterable, n) # n copies of iterable
repeat(i[, n]) # like [i,]*n, iterable
accumulate(iterable[, func]) # res[i] = func(iterable[i], res[i-1])
product(*iterables[, repeat])
zip_longest(*itreables, fillvalue=None)
```

## more_itertools
```python
consecutive_groups(iter) # splits into group of consucetive values
pairwise(iter) # returns pairs of elements
```

## functools
```python
partial(func, *args, **kwargs) # pre determined arguments
reduce(func, iterable[, init]) # for i in iterable: res = func(res, i)
```

## pandas
```python
## assignments
df1=df2 # pointer! use df2.copy()
df.query(cond: str) # condition on rows
df[['value','group']].groupby('group').cumsum() # cumulative sum of 'value' separated by group
df['col'].where(df['col']>0, 0) # replace instances of condition with value
df.memory_usage() # memory for each column
df.merge() # basically, all kinds of `join`
df.sort_values(by=col, ascending=True) # sorted

## change data
df.infer_objects() # infer datatypes for columns
df.replace() # either *(value, replacement), or dict of replacements
df.applymap(fun) # perform `fun` element wise, Note: always prefer vectorized operation if possible

## use data
df.sample(n=3, frac=0.5) # randomly sample n rows or frac
df.unique() # unique values
df.nunique(axis=0) # num of unique values in each column/row
df.value_counts() # params: normalize(bool), bin(int)
df.pct_change() # calculate changes column-wise (only if all columns are numeric!)
df.rank() # rank values column-wise
df.melt() # all kind of 'self join' operations, transforming column to values in rows
df.explode(c, ignore_index=False) # for each row: [a:1, b:2, c:[3,4]] creates rows [1,2,3],[1,2,4]
df.describe() # statistical summary for each column. all kind of statistics
df.select_dtypes() # use `include` or  `exlude` parameters to select dtypes to returns 
df.isna().sum() # count of nulls per column

## addressing
df['col'] # select COLUMN `col`
df.col # select COLUMN `col`
df[['col1', 'col2']] # select COLUMNS `col1`, `col2` 
df[df.col.isin(l)] # select ROWS, condition on `col`
df.loc[r0:r1:r2, cols] # select ROWS & COLUMNS in index range [r0:r1] with step of r2. only work if r0,r1 is unique! cols is indexing for columns
df.loc[['row1', 'row2'], cols] # select ROWS & COLUMNS row1, row2. cols is indexing for columns
df.iloc[r0:r1:r2, c0:c1:c2] # select ROWS & COLUMNS in range [r0, r1) * [c0, c1) with step of r2,c2. 
df.lookup(row_seq, col_seq) # like: df.loc[i,j] for i,j in row_seq,col_seq

df.columns.tolist() # column names
```

## numpy
```python
linspace(start, stop, num)
arrange(start, stop, step)
setdiff1d(arr1, arr2) # values in arr1, not arr2
intersect1d(arr1, arr2) # values in both arr1
np.where(cond, true_val, false_val) # set values according to condition
```

## other libraries - tips
```python
matplotlib.animation.FuncAnimation(...) # animation of iterative process
timeit.timeit(stmt, setup, ..., number) # execute `stmnt` `number` times with `setup` code, and return timing
```

## Development
* [refurb](https://medium.com/@fareedkhandev/make-your-python-code-more-elegant-readable-or-modern-with-one-command-eb910cefded3) for code imporvements tips
* Write regex with **RegEx**
* [Numba](https://towardsdatascience.com/this-decorator-will-make-python-30-times-faster-715ca5a66d5f) for speeding up Python execution by compiling it


## General Tips
* return `namedtuple` when returning multiple items instead of a tuple
* no mutations! don't assign a variable a new value, create new one (when possible)!
* update all states variables in one line: `count, end = count+1, False`
* raise exceptions freely for anything which is not output=f(input)
* document your code in doc-strings (top of function/module) so it'll be captured in python's built-in `__doc__` attribute 
* `from module import *` doesn't import objects which starts with underscore (`_`) unless otherwise specified.

## Library Tips
* use `requests.Session()` to re-use the TCP connection and increase performance
* use `Pathlib` instead of `os.path`, `glob`, etc.