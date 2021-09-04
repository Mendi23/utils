import numpy as np

def alpha_beta_minmax(
    state,
    alpha: int = -np.inf,
    beta: int = np.inf,
    max_depth: int = None,
    maximizing: bool = True
    ):

    successors = list(state.get_possible_moves())

    if not successors or max_depth == 0:
        return state.score

    current, action = (-np.inf, max) if maximizing else (np.inf, min)
    max_depth = max_depth-1 if max_depth is not None else max_depth
    for c in successors:

        current = action(current, alpha_beta_minmax(c, alpha, beta, max_depth, not maximizing))

        if maximizing:
            alpha = max(alpha, current)
            if current >= beta:
                return np.inf
        else:
            beta = min(beta, current)
            if current <= alpha:
                return -np.inf

    return current