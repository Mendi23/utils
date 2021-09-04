from typing import Callable, Iterable, List, Set, Tuple, Union

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
