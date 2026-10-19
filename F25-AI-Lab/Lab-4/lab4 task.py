"""
Lab 4: Informed Search — Heuristics & A*
Course: Artificial Intelligence Lab
Scenario: Campus navigation using weighted travel-time edges.

Run:
    python lab4_astar_audit.py

No third-party packages are required.
"""

import heapq

GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": [],
}

HEURISTIC = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}
START = "S"
GOAL = "G"


def reconstruct_cost(graph, path):
    """Independently sum edge weights along a returned path."""
    total = 0
    for u, v in zip(path, path[1:]):
        for nxt, weight in graph[u]:
            if nxt == v:
                total += weight
                break
        else:
            raise ValueError(f"No edge found from {u} to {v}")
    return total


def true_remaining_costs(graph, goal):
    """Compute exact remaining costs using a simple repeated relaxation."""
    nodes = list(graph)
    dist = {node: float("inf") for node in nodes}
    dist[goal] = 0
    changed = True
    while changed:
        changed = False
        for u in nodes:
            for v, weight in graph[u]:
                if dist[v] != float("inf") and weight + dist[v] < dist[u]:
                    dist[u] = weight + dist[v]
                    changed = True
    return dist


def audit_heuristic(graph, heuristic, goal):
    true_costs = true_remaining_costs(graph, goal)
    print("\nHEURISTIC AUDIT")
    print("Node | h(n) | true remaining | admissible?")
    for node in graph:
        admissible = heuristic[node] <= true_costs[node]
        print(f"{node:>4} | {heuristic[node]:>4} | {true_costs[node]:>14} | {admissible}")
    consistent = True
    print("\nConsistency checks: h(u) <= cost(u,v) + h(v)")
    for u, edges in graph.items():
        for v, weight in edges:
            ok = heuristic[u] <= weight + heuristic[v]
            consistent = consistent and ok
            print(f"{u}->{v}: {heuristic[u]} <= {weight} + {heuristic[v]} "
                  f"({weight + heuristic[v]}) -> {ok}")
    print(f"Admissible overall: {all(heuristic[n] <= true_costs[n] for n in graph)}")
    print(f"Consistent overall: {consistent}")


def best_first_search(graph, heuristic, start, goal, algorithm_name="A*"):
    """
    Priority-queue graph search.
    A*: priority is g+h. UCS: pass a zero heuristic.
    A node is counted as expanded only when its successors are examined.
    Goal is logged as processed but excluded from expansion count.
    Stale queue entries are ignored.
    """
    counter = 0  # stable tie-breaking: insertion order
    pq = [(heuristic[start], counter, 0, start, [start])]
    best = {start: 0}
    processed = []
    expanded = []
    stale_skipped = 0

    while pq:
        priority, _, g_cost, node, path = heapq.heappop(pq)

        if g_cost != best.get(node, float("inf")):
            stale_skipped += 1
            continue

        processed.append((node, g_cost, heuristic[node], g_cost + heuristic[node]))
        if node == goal:
            return {
                "algorithm": algorithm_name,
                "path": path,
                "cost": g_cost,
                "processed": processed,
                "expanded": expanded,
                "expansion_count": len(expanded),
                "stale_skipped": stale_skipped,
            }

        expanded.append(node)
        for nxt, weight in graph.get(node, []):
            new_cost = g_cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                counter += 1
                heapq.heappush(
                    pq,
                    (new_cost + heuristic[nxt], counter, new_cost, nxt, path + [nxt]),
                )

    return {
        "algorithm": algorithm_name,
        "path": None,
        "cost": float("inf"),
        "processed": processed,
        "expanded": expanded,
        "expansion_count": len(expanded),
        "stale_skipped": stale_skipped,
    }


def show_result(result, graph):
    print(f"\n{result['algorithm']} RESULT")
    print("Path:", " -> ".join(result["path"]) if result["path"] else "No path")
    print("Returned cost:", result["cost"])
    if result["path"]:
        print("Independently summed path cost:", reconstruct_cost(graph, result["path"]))
    print("Processed trace (node, g, h, f):")
    for item in result["processed"]:
        print(" ", item)
    print("Expanded nodes (successors examined):", result["expanded"])
    print("Expansion count (goal excluded):", result["expansion_count"])
    print("Stale queue entries skipped:", result["stale_skipped"])


def main():
    print("=" * 60)
    print("LAB 4: INFORMED SEARCH — HEURISTICS & A*")
    print("=" * 60)
    print("Graph:", GRAPH)
    print("Heuristic:", HEURISTIC)

    audit_heuristic(GRAPH, HEURISTIC, GOAL)

    astar_result = best_first_search(GRAPH, HEURISTIC, START, GOAL, "A*")
    ucs_result = best_first_search(
        GRAPH, {node: 0 for node in GRAPH}, START, GOAL, "UCS (zero heuristic)"
    )
    show_result(astar_result, GRAPH)
    show_result(ucs_result, GRAPH)

    print("\nCONTROLLED COMPARISON")
    print("Algorithm | Path | Cost | Expanded nodes | Count")
    for result in (astar_result, ucs_result):
        path = " -> ".join(result["path"]) if result["path"] else "No path"
        print(f"{result['algorithm']} | {path} | {result['cost']} | "
              f"{result['expanded']} | {result['expansion_count']}")

    print("\nOVERESTIMATE EXPERIMENT: change only h(C) from 2 to 10")
    bad_h = dict(HEURISTIC)
    bad_h["C"] = 10
    print("Modified heuristic:", bad_h)
    audit_heuristic(GRAPH, bad_h, GOAL)
    overestimate_result = best_first_search(GRAPH, bad_h, START, GOAL, "A* with h(C)=10")
    show_result(overestimate_result, GRAPH)

    print("\nINTERPRETATION")
    print("The supplied heuristic is admissible and consistent on this graph.")
    print("A* finds S -> A -> C -> G at cost 6.")
    print("UCS uses h(n)=0 and returns an optimal path; its expansion count may differ.")
    print("With h(C)=10, the heuristic overestimates C's true remaining cost of 3.")
    print("The algorithm can choose the cost-9 route through B before exploring C,")
    print("so this inadmissible heuristic can cause a suboptimal result.")


if __name__ == "__main__":
    main()
