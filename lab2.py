import heapq

# =========================
# Heuristic (Manhattan)
# =========================
def h_cost(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# =========================
# Chi phí ô
# =========================
def cost(cell):
    return {
        0: 1,
        2: 3,
        3: 5
    }.get(cell, float('inf'))

# =========================
# Lấy hàng xóm (4 hướng)
# =========================
def neighbors(grid, pos):
    x, y = pos
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    result = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != 1:
                result.append((nx, ny))
    return result

# =========================
# Truy vết đường đi
# =========================
def build_path(parent, end):
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = parent.get(cur)
    return path[::-1]

# =========================
# A* chính
# =========================
def a_star(grid, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))

    g_score = {start: 0}
    parent = {start: None}

    visited = set()

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return build_path(parent, goal), g_score[goal]

        for nb in neighbors(grid, current):
            if nb in visited:
                continue

            new_cost = g_score[current] + cost(grid[nb[0]][nb[1]])

            if nb not in g_score or new_cost < g_score[nb]:
                g_score[nb] = new_cost
                priority = new_cost + h_cost(nb, goal)
                heapq.heappush(pq, (priority, nb))
                parent[nb] = current

    return [], 0

# =========================
# In kết quả
# =========================
def show(grid, path, start, goal):
    temp = [row[:] for row in grid]

    for x, y in path:
        if (x, y) != start and (x, y) != goal:
            temp[x][y] = '*'

    sx, sy = start
    gx, gy = goal

    temp[sx][sy] = 'S'
    temp[gx][gy] = 'G'

    print("\n=== GRID ===")
    for row in temp:
        print(' '.join(str(i) for i in row))

# =========================
# MAIN
# =========================
def main():
    grid = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,2,2,0,1,0],
        [0,0,0,1,0,2,0,0,1,0],
        [0,3,0,1,0,0,0,3,1,0],
        [0,3,0,0,0,1,1,0,0,0],
        [0,3,3,3,0,0,0,0,2,0],
        [0,0,0,3,1,1,1,0,2,0],
        [1,1,0,0,0,2,0,0,2,0],
        [0,0,0,1,0,2,0,3,3,0],
        [0,1,0,0,0,0,0,0,0,0]
    ]

    start = (0, 0)
    goal = (9, 9)

    path, total = a_star(grid, start, goal)

    if path:
        print("✔ Path found")
        print("Steps:", len(path)-1)
        print("Cost:", total)
        print("Path:", path)
        show(grid, path, start, goal)
    else:
        print("✘ No path")

if __name__ == "__main__":
    main()