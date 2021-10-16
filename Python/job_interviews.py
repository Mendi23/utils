from typing import Callable, Generator, Iterable, Iterator, List, Set, Tuple, Union, Sequence

def reverse_integer(i):
    """
    Given an integer, return the integer with reversed digits.
    Note: The integer could be either positive or negative.
    """
    return str(i)[::-1] if i >= 0 else '-' + str(-1 * i)[::-1]

def average_words_length(s):
    """
    For a given sentence, return the average word length. 
    Note: Remember to remove punctuation first.
    """
    seq = s.split()
    return sum(len(list(filter(str.isalpha, w))) for w in seq) / len(seq)

def add_strings(s1, s2):
    """
    Given two non-negative integers num1 and num2 represented as string, return the sum of num1 and num2.
    You must not use any built-in BigInteger library or convert the inputs to integer directly.

    Notes:
    Both num1 and num2 contains only digits 0-9.
    Both num1 and num2 does not contain any leading zero.
    """

    from itertools import zip_longest

    conv_int = lambda e: ord(e) - ord('0')
    final, carry = [], 0

    for i, j in zip_longest(s1[::-1], s2[::-1], fillvalue='0'):
        carry, res = divmod(conv_int(i) + conv_int(j) + carry, 10)
        final.append(str(res))

    if carry > 0:
        final.append(str(carry))

    return ''.join(reversed(final))

def first_unique_character(s):
    """
    Given a string, find the first non-repeating character in it and return its index. 
    If it doesn't exist, return -1.
    Note: all the input strings are already lowercase.
    """
    from collections import OrderedDict
    res = OrderedDict()
    for i, letter in enumerate(s):
        if letter in res:
            res[letter][1] += 1
        else:
            res[letter] = [i, 1]

    return next((v[0] for v in res.values() if v[1] == 1), -1)

def valid_palindrome(s):
    """
    Given a non-empty string s, you may delete at most one character. Judge whether you can make it a palindrome.
    The string will only contain lowercase characters a-z.
    """

    for i in range(len(s)):
        t = s[:i] + s[i + 1:]
        if t == t[::-1]: return True
    return s == s[::-1]

def alignment_problen(s1, s2):
    """paper: https://upload.wikimedia.org/wikipedia/en/c/c4/ParallelNeedlemanAlgorithm.pdf"""

    # parameters
    GAP_SCORE = -1
    MISMATCH_SCORE = -2
    MATCH_SCORE = 1

    # initialization
    score = [[None] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    for i in range(len(s2) + 1):
        score[0][i] = i * GAP_SCORE

    for i in range(len(s1) + 1):
        score[i][0] = i * GAP_SCORE

    # dynamic programing
    directions = []
    for i in range(1, len(s1) + 1):
        directions.append([])
        for j in range(1, len(s2) + 1):
            d, max_score = (
                max(((0, -1), score[i][j - 1] + GAP_SCORE),
                    ((-1, 0), score[i - 1][j] + GAP_SCORE),
                    ((-1, -1), score[i - 1][j - 1] +
                     (MATCH_SCORE if s1[i - 1] == s2[j - 1] else MISMATCH_SCORE)),
                    key=lambda x: x[1])
                )
            score[i][j] = max_score
            directions[i - 1].append(d)

    # getting best sequence from direction
    seq = []
    i, j = len(s1), len(s2)
    while any((i, j)):
        d = directions[i - 1][j - 1]
        i, j = i + d[0], j + d[1]
        seq.append((s1[i] if d[0] else None, s2[j] if d[1] else None))

    return seq[::-1]

def check_canonical_forms(matrix_a, matrix_b):
    from collections import Counter
    get_rows_sets_counter = lambda matrix: Counter(
        frozenset(Counter(r).items()) for r in matrix
        )
    return get_rows_sets_counter(matrix_a) == get_rows_sets_counter(matrix_b) and \
        get_rows_sets_counter(zip(*matrix_a)) == get_rows_sets_counter(zip(*matrix_b))

def maximun_sum_decent(tree):
    """https://johnlekberg.com/blog/2020-02-12-maximum-sum-descent.html"""

    max_sum = [[] for _ in range(len(tree) - 1)]
    max_sum.append(tree[-1])
    for i in range(len(tree) - 2, -1, -1):
        for j in range(len(tree[i])):
            max_sum[i].append(+tree[i][j] + max(max_sum[i + 1][j], max_sum[i + 1][j + 1]))
    return max_sum[0][0]

def permutation_rank_problem(s: str):
    """https://johnlekberg.com/blog/2020-03-04-permutation-rank.html"""
    from math import factorial
    assert len(set(s)) == len(s)   # no repeating charecters!

    char_order = sorted(s)
    res = 0
    for i, char in enumerate(s, 1):
        char_pos = char_order.index(char)
        char_order.pop(char_pos)
        res += char_pos * factorial(len(s) - i)

    return res + 1

def caesar_cipher_1(s: str, n: int) -> str:
    hashed = lambda c: chr((ord(c) + n - ord('a')) % 26 + ord('a'))
    return ''.join(hashed(c) if c.islower() else c for c in s)

def sudoko_solver(board: str) -> str:
    from itertools import chain, product
    Board = List[List[int]]

    def sdm_to_lists(s: str) -> Board:
        return [list(int(i) for i in s[i * 9:(i*9) + 9]) for i in range(9)]


    def get_square_indexes(i: int, j: int) -> Iterable[Tuple[int, int]]:
        sq_row, sq_col = (i//3) * 3, (j//3) * 3
        return product(range(sq_row, sq_row + 3), range(sq_col, sq_col + 3))

    def available_digits(board: Board, i: int, j: int) -> Set[int]:
        taken = set(
            chain(
                board[i], (row[j] for row in board),
                (board[x][y] for x, y in get_square_indexes(i, j))
                )
            )
        return set(range(1,10)) - taken

    def solve_board(board: Board, i: int, j: int) -> Union[Board, None]:
        new_i, new_j = (i+1, j) if j == 8 else (i, j+1)
        if board[i][j] != 0:
            return board if i == 8 and j == 8 else solve_board(board, new_i, new_j)
        
        options = available_digits(board, i, j)
        if not options:
            return None
        
        if i == 8 and j == 8:
            board[i][j] = options.pop()
            return board
    
        for num in options:
            board[i][j] = num
            res = solve_board(board, new_i, new_j)
            if res is None:
                board[i][j] = 0
            else:
                return res
        return None

def SED(X, Y):
    """Compute the squared Euclidean distance between X and Y."""
    return sum((i-j)**2 for i, j in zip(X, Y))


def longest_substring_no_repetition(s: str) -> str:
    """Length of the longest substring without repeating characters"""
    
    from collections import defaultdict
    
    last_index, max_len, start_idx, max_start = defaultdict(0), 0, 0, 0

    for i, l in enumerate(s):

        start_idx = max(start_idx, last_index[l])
        curr_len = i-start_idx+1
        if curr_len > max_len:
            max_len, max_start = curr_len, start_idx
        last_index[l] = i

    end_idx = next((i for i,v in enumerate(l) if v==s[max_start]), len(s))
    return s[max_start:end_idx]

def print_prev_smaller(l: List) -> List:
    from collections import deque
    d = deque()
    res = {}

    for i in l:
        while 0 < len(d):
            curr = d.pop()
            if curr < i:
                res[i] = curr
                d.append(curr)
                break
        d.append(i)
        
    return [res.get(i, None) for i in range(len(l))]

def convert_integer_to_words(i: int) -> str:

    assert 0 <= i <= 999999999, 'illegal integer value' 

    def convert_triplet(triplet) -> str:
        teens_dict = {
            '0': 'ten', '1': 'eleven', '2': 'twelve', '3': 'thirteen', '4': 'fourteen', '5': 'fifteen',
            '6': 'sixteen', '7': 'seventeen', '8': 'eighteen', '9': 'nineteen'
        }
        digit_dict = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
            '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
            }
        tenth_dict = {
            '2': 'twenty', '3': 'thirty', '4': 'forty', '5': 'fifty',
            '6': 'sixty', '7': 'seventy', '8': 'eighty', '9': 'ninety'
            }

        if len(triplet) == 1:
            return digit_dict[triplet[0]]

        res = []

        if len(triplet) == 3 and triplet[-3] != '0':
            res.extend((digit_dict[triplet[-3]], 'hundred'))

        if triplet[-2] != '0':
            if triplet[-2] == '1':
                res.append(teens_dict[triplet[-1]])
            elif triplet[-1] == '0':
                res.append(tenth_dict[triplet[-2]])
            else:
                res.extend((tenth_dict[triplet[-2]], digit_dict[triplet[-1]]))
        elif triplet[-1] != '0':
            res.append(digit_dict[triplet[-1]])

        return ' '.join(res)
            
    num_str = list(str(i))
    ret_list = []

    if i > 999999:
        ret_list.extend((convert_triplet(num_str[:-6]), 'million'))
    if i > 999:
        second = convert_triplet(num_str[-6:-3])
        if second:
            ret_list.extend((second, 'thousand'))
    ret_list.append(convert_triplet(num_str[-3:]))
    return ' '.join(ret_list)

def schedule_meeting_rooms(intervals: List[Tuple[int, int]]) -> dict:
    import heapq as hq
    from collections import defaultdict

    rooms = []
    sched = {}
    _end_times = defaultdict(list)
    for i, (s, e) in enumerate(intervals):
        if rooms[0] > s:
            hq.heappush(rooms, e)
            new_room = len(rooms)
            _end_times[e].append(new_room)
            sched[new_room] = [i,]
        else:
            curr_end = hq.heappushpop(rooms, e)
            room = _end_times[curr_end].pop()
            
            if not _end_times[curr_end]:
                del _end_times[curr_end]
            
            sched[room].append(i)
            _end_times[e].append(room)
    
    return sched

def min_val_with_min_operations(arr: Sequence[int]) -> int:
    """3/2 comperations"""
    if len(arr) == 0:
        raise ValueError("empty array")
    curr_min, curr_max = arr[0], arr[0]
    if len(arr) % 2 != 0:
        arr = arr[1:]
    for x, y in (arr[i: i+2] for i in range(0, len(arr), 2)):
        smaller, larger = (x, y) if x < y else (y, x)
        curr_min = smaller if smaller < curr_min else curr_min
        curr_max = larger if larger > curr_max else curr_max
    return curr_min, curr_max

def sum_of_halfs(arr: list) ->int:
    left, right = 0, sum(arr)
    for i, val in enumerate(arr):
        left += val
        right -= val
        if left == right:
            return i
    return -1

def is_pow(i):
    bin_rep = bin(i)
    return '1' in bin_rep and bin_rep.index('1') == bin_rep.rindex('1')

def max_render_elements(D, C, P):
    """Microsoft 1

    Args:
        D ([type]): [description]
        C ([type]): [description]
        P ([type]): [description]

    Returns:
        [type]: [description]
    """
    max_sum = 0
    for i, (_, cost) in enumerate(sorted(zip(D,C))):
        max_sum += cost
        if max_sum > P:
            return i
    return len(D)

def drop_five(N):
    """Microsoft 2

    Args:
        N ([type]): [description]

    Returns:
        [type]: [description]
    """
    digit = str(5)
    s_n = str(N)
    indices = (i for i, x in enumerate(s_n) if x == digit)
    return max(int(s_n[:i]+s_n[i+1:]) for i in indices)


        