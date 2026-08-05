import heapq
import copy

INF = float('inf')


def reduce_matrix(matrix):
    """Reduce the matrix and return reduced matrix with reduction cost."""
    m = copy.deepcopy(matrix)
    n = len(m)
    reduction_cost = 0

    # Row reduction
    for i in range(n):
        row = [x for x in m[i] if x != INF]
        if row:
            row_min = min(row)
            if row_min > 0:
                reduction_cost += row_min
                for j in range(n):
                    if m[i][j] != INF:
                        m[i][j] -= row_min

    # Column reduction
    for j in range(n):
        col = [m[i][j] for i in range(n) if m[i][j] != INF]
        if col:
            col_min = min(col)
            if col_min > 0:
                reduction_cost += col_min
                for i in range(n):
                    if m[i][j] != INF:
                        m[i][j] -= col_min

    return m, reduction_cost


class Node:
    def __init__(self, matrix, path, level, city, cost, bound):
        self.matrix = matrix
        self.path = path
        self.level = level
        self.city = city
        self.cost = cost
        self.bound = bound

    def __lt__(self, other):
        return self.bound < other.bound


def tsp_branch_and_bound(cost):
    n = len(cost)

    reduced_matrix, reduction_cost = reduce_matrix(cost)

    root = Node(
        reduced_matrix,
        [0],
        0,
        0,
        0,
        reduction_cost
    )

    pq = []
    heapq.heappush(pq, root)

    best_cost = INF
    best_path = []

    while pq:
        current = heapq.heappop(pq)

        if current.bound >= best_cost:
            continue

        if current.level == n - 1:
            total_cost = current.cost + cost[current.city][0]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = current.path + [0]
            continue

        for next_city in range(n):
            if next_city not in current.path:

                new_matrix = copy.deepcopy(current.matrix)

                # Make current row INF
                for j in range(n):
                    new_matrix[current.city][j] = INF

                # Make next column INF
                for i in range(n):
                    new_matrix[i][next_city] = INF

                # Prevent returning to start early
                new_matrix[next_city][0] = INF

                reduced, red_cost = reduce_matrix(new_matrix)

                new_cost = current.cost + cost[current.city][next_city]
                new_bound = new_cost + red_cost

                if new_bound < best_cost:
                    child = Node(
                        reduced,
                        current.path + [next_city],
                        current.level + 1,
                        next_city,
                        new_cost,
                        new_bound
                    )
                    heapq.heappush(pq, child)

    return best_path, best_cost


# ---------------- Driver Program ----------------

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

cities = ['A', 'B', 'C', 'D', 'E']

path, minimum_cost = tsp_branch_and_bound(cost)

print("5-City TSP - Cost Matrix:")
print(f'{"":>4}', ' '.join(f'{c:>5}' for c in cities))

for i, row in enumerate(cost):
    values = ['INF' if x == INF else str(x) for x in row]
    print(f'{cities[i]:>4}', ' '.join(f'{v:>5}' for v in values))

print("\nOptimal Tour:")
print(" -> ".join(cities[i] for i in path))

print("\nMinimum Cost:", minimum_cost)

print("\nPath Verification:")
for i in range(len(path) - 1):
    u, v = path[i], path[i + 1]
    print(f"{cities[u]} -> {cities[v]} : {cost[u][v]}")