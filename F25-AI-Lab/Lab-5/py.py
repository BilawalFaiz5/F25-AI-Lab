
import math


def minimax(depth, index, is_max, scores, target_depth,
            counter, reverse=False):
    # Count each terminal node that is evaluated
    if depth == target_depth:
        counter[0] += 1
        return scores[index]

    best = float("-inf") if is_max else float("inf")
    branches = [1, 0] if reverse else [0, 1]

    for branch in branches:
        child_index = index * 2 + branch

        value = minimax(
            depth + 1,
            child_index,
            not is_max,
            scores,
            target_depth,
            counter,
            reverse
        )

        if is_max:
            best = max(best, value)
        else:
            best = min(best, value)

    return best


def alphabeta(depth, index, is_max, scores, target_depth,
              alpha, beta, counter, reverse=False):
    # Count each terminal node that is evaluated
    if depth == target_depth:
        counter[0] += 1
        return scores[index]

    branches = [1, 0] if reverse else [0, 1]

    if is_max:
        value = float("-inf")

        for branch in branches:
            child_index = index * 2 + branch

            child_value = alphabeta(
                depth + 1, child_index, False, scores,
                target_depth, alpha, beta, counter, reverse
            )

            value = max(value, child_value)
            alpha = max(alpha, value)

            # Prune when MAX's bound reaches MIN's bound
            if alpha >= beta:
                break

        return value

    else:
        value = float("inf")

        for branch in branches:
            child_index = index * 2 + branch

            child_value = alphabeta(
                depth + 1, child_index, True, scores,
                target_depth, alpha, beta, counter, reverse
            )

            value = min(value, child_value)
            beta = min(beta, value)

            if alpha >= beta:
                break

        return value


def run_test(scores, reverse=False):
    if len(scores) == 0:
        raise ValueError("Scores cannot be empty.")

    # A complete binary tree must have a power-of-two leaf count
    if len(scores) & (len(scores) - 1):
        raise ValueError("Use a complete tree with 2^n leaves.")

    depth = int(math.log2(len(scores)))

    mini_count = [0]
    alpha_count = [0]

    mini_value = minimax(
        0, 0, True, scores, depth, mini_count, reverse
    )

    alpha_value = alphabeta(
        0, 0, True, scores, depth,
        float("-inf"), float("inf"),
        alpha_count, reverse
    )

    print("Branch order:", "Reversed" if reverse else "Normal")
    print("Minimax value:", mini_value)
    print("Minimax leaves evaluated:", mini_count[0])
    print("Alpha-Beta value:", alpha_value)
    print("Alpha-Beta leaves evaluated:", alpha_count[0])
    print("Values match:", mini_value == alpha_value)
    print("-" * 35)

    return mini_value, alpha_value, mini_count[0], alpha_count[0]


# Main test: eight terminal scores
scores = [3, 5, 6, 9, 1, 2, 0, -1]

normal = run_test(scores, reverse=False)
reversed_order = run_test(scores, reverse=True)

# Edge case: a tree containing only one terminal node
print("Edge case: one terminal node")
edge = run_test([42])

# Verify that pruning never evaluates more leaves
assert normal[0] == normal[1] == 5
assert reversed_order[0] == reversed_order[1] == 5
assert normal[3] <= normal[2]
assert reversed_order[3] <= reversed_order[2]
assert edge[0] == edge[1] == 42

print("All tests passed.")
