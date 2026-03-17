
# ============================================================
#  A* MAZE SOLVER — Animated Version
#  Run:  python maze_solver.py
#  Requires matplotlib:  pip install matplotlib
# ============================================================

import heapq
import math
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.animation import FuncAnimation

# ── MAZE DEFINITION ──────────────────────────────────────────
# 0 = open cell   |   1 = wall
# Feel free to edit — just keep all rows the same length.

MAZE = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

START = (0, 0)    # (row, col)
GOAL  = (9, 9)    # (row, col)
ROWS  = len(MAZE)
COLS  = len(MAZE[0])

# ── SETTINGS ─────────────────────────────────────────────────
DIAGONAL          = False        # True = allow diagonal movement
ANIMATION_SPEED   = 80          # milliseconds per frame (lower = faster)
CHOSEN_HEURISTIC  = "manhattan"  # "manhattan", "euclidean", or "chebyshev"


# ── HEURISTIC FUNCTIONS ──────────────────────────────────────

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

HEURISTICS = {
    "manhattan" : manhattan,
    "euclidean" : euclidean,
    "chebyshev" : chebyshev,
}


# ── NODE CLASS ───────────────────────────────────────────────

class Node:
    def __init__(self, pos, g=0, h=0, parent=None):
        self.pos    = pos
        self.g      = g
        self.h      = h
        self.f      = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


# ── A* ALGORITHM ─────────────────────────────────────────────

def astar(maze, start, goal, heuristic=manhattan, diagonal=False):
    rows, cols = len(maze), len(maze[0])

    if diagonal:
        DIRS = [(-1,0),(1,0),(0,-1),(0,1),
                (-1,-1),(-1,1),(1,-1),(1,1)]
    else:
        DIRS = [(-1,0),(1,0),(0,-1),(0,1)]

    start_node = Node(start, g=0, h=heuristic(start, goal))
    open_list  = [start_node]
    closed_set = set()
    best_g     = {start: 0}
    explored   = []

    while open_list:
        current = heapq.heappop(open_list)

        if current.pos in closed_set:
            continue
        closed_set.add(current.pos)
        explored.append(current.pos)

        if current.pos == goal:
            path = []
            node = current
            while node is not None:
                path.append(node.pos)
                node = node.parent
            path.reverse()
            return path, explored, True

        r, c = current.pos
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols): continue
            if maze[nr][nc] == 1:                        continue
            if (nr, nc) in closed_set:                   continue

            step  = math.sqrt(2) if (dr != 0 and dc != 0) else 1
            new_g = current.g + step

            if new_g < best_g.get((nr, nc), float('inf')):
                best_g[(nr, nc)] = new_g
                h        = heuristic((nr, nc), goal)
                neighbor = Node((nr, nc), g=new_g, h=h, parent=current)
                heapq.heappush(open_list, neighbor)

    return [], explored, False


# ── BUILD BASE IMAGE ─────────────────────────────────────────

def build_base_image(maze):
    img = np.zeros((ROWS, COLS, 3))
    for r in range(ROWS):
        for c in range(COLS):
            img[r, c] = [0.16, 0.16, 0.22] if maze[r][c] == 1 \
                        else [0.07, 0.10, 0.16]
    sr, sc = START
    gr, gc = GOAL
    img[sr, sc] = [0.00, 0.90, 0.50]   # green = start
    img[gr, gc] = [1.00, 0.25, 0.35]   # red   = goal
    return img


# ── ANIMATED VISUALISER ──────────────────────────────────────

def animate(maze, explored, path, found, heuristic_name, elapsed_ms):
    base_img   = build_base_image(maze)
    canvas_img = base_img.copy()

    fig, ax = plt.subplots(figsize=(7, 7), facecolor="#0a0a0f")
    ax.set_facecolor("#0a0a0f")
    fig.canvas.manager.set_window_title("A* Maze Solver")

    im = ax.imshow(canvas_img, interpolation="nearest", vmin=0, vmax=1)

    # Grid lines
    ax.set_xticks([x - 0.5 for x in range(COLS + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(ROWS + 1)], minor=True)
    ax.grid(which="minor", color="#1a1a2e", linewidth=0.6)
    ax.tick_params(which="minor", size=0)
    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))
    ax.tick_params(colors="#555577", labelsize=7)

    title_text  = ax.set_title("A* Search — Exploring...",
                               color="white", fontsize=12, pad=12)
    status_text = ax.text(
        0.5, -0.04, "", transform=ax.transAxes,
        ha="center", va="top", color="#8888aa", fontsize=9
    )

    legend_items = [
        mpatches.Patch(color=[0.00, 0.90, 0.50], label=f"Start {START}"),
        mpatches.Patch(color=[1.00, 0.25, 0.35], label=f"Goal  {GOAL}"),
        mpatches.Patch(color=[0.20, 0.50, 0.80], label="Exploring (frontier)"),
        mpatches.Patch(color=[0.08, 0.25, 0.42], label="Explored"),
        mpatches.Patch(color=[1.00, 0.85, 0.25], label="Shortest path"),
        mpatches.Patch(color=[0.16, 0.16, 0.22], label="Wall"),
    ]
    ax.legend(
        handles=legend_items, loc="upper right",
        facecolor="#111118", edgecolor="#2a2a3a",
        labelcolor="white", fontsize=8, framealpha=0.9
    )

    state = {"phase": "explore", "index": 0, "done": False}
    total_frames = len(explored) + (len(path) if found else 0) + 1

    def update(frame):
        if state["done"]:
            return [im]

        img = canvas_img

        # Phase 1 — explore cell by cell
        if state["phase"] == "explore":
            i = state["index"]
            if i < len(explored):
                r, c = explored[i]
                if (r, c) != START and (r, c) != GOAL:
                    img[r, c] = [0.20, 0.50, 0.80]   # bright blue = current frontier
                    if i > 0:
                        pr, pc = explored[i - 1]
                        if (pr, pc) != START and (pr, pc) != GOAL:
                            img[pr, pc] = [0.08, 0.25, 0.42]  # dark blue = visited

                state["index"] += 1
                title_text.set_text(
                    f"A* Search — Exploring...  ({i+1}/{len(explored)} cells)"
                )
                status_text.set_text(
                    f"Heuristic: {heuristic_name}  |  "
                    f"Diagonal: {DIAGONAL}  |  Time: {elapsed_ms:.2f} ms"
                )
            else:
                state["phase"] = "path"
                state["index"] = 0

        # Phase 2 — draw path cell by cell
        elif state["phase"] == "path":
            i = state["index"]
            if found and i < len(path):
                r, c = path[i]
                if (r, c) != START and (r, c) != GOAL:
                    img[r, c] = [1.00, 0.85, 0.25]   # gold = path

                state["index"] += 1
                title_text.set_text(
                    f"Path found!  Tracing route...  ({i+1}/{len(path)} steps)"
                )
            else:
                state["phase"] = "done"
                state["done"]  = True
                if found:
                    title_text.set_text(
                        f"✅  Done!   Path: {len(path)} steps   |   "
                        f"Explored: {len(explored)} cells"
                    )
                    status_text.set_text(
                        f"Heuristic: {heuristic_name}  |  "
                        f"Diagonal: {DIAGONAL}  |  Time: {elapsed_ms:.2f} ms"
                    )
                else:
                    title_text.set_text(
                        f"❌  No path found!   "
                        f"Explored {len(explored)} cells — goal unreachable."
                    )
                    title_text.set_color("#ff4466")

        im.set_data(img)
        return [im]

    ani = FuncAnimation(
        fig, update,
        frames=total_frames,
        interval=ANIMATION_SPEED,
        blit=True,
        repeat=False
    )

    plt.tight_layout()
    plt.show()


# ── CONSOLE PRINT ────────────────────────────────────────────

def print_maze(maze, path, explored):
    path_set     = set(path)
    explored_set = set(explored)
    print("\n     " + "".join(f"{c:<2}" for c in range(COLS)))
    print("    " + "─" * (COLS * 2 + 1))
    for r, row in enumerate(maze):
        row_str = f"{r:>3} │"
        for c, cell in enumerate(row):
            pos = (r, c)
            if   pos == START:           row_str += " S"
            elif pos == GOAL:            row_str += " G"
            elif pos in path_set:        row_str += " *"
            elif pos in explored_set:    row_str += " o"
            elif cell == 1:              row_str += " #"
            else:                        row_str += " ."
        print(row_str)
    print()


# ── MAIN ─────────────────────────────────────────────────────

def main():
    heuristic_fn = HEURISTICS.get(CHOSEN_HEURISTIC, manhattan)

    print("=" * 52)
    print("  A* MAZE SOLVER — Animated")
    print(f"  Grid      : {ROWS} x {COLS}")
    print(f"  Start     : {START}   Goal : {GOAL}")
    print(f"  Heuristic : {CHOSEN_HEURISTIC}")
    print(f"  Diagonal  : {DIAGONAL}")
    print("=" * 52)

    # Validate positions
    for label, pos in [("Start", START), ("Goal", GOAL)]:
        r, c = pos
        if not (0 <= r < ROWS and 0 <= c < COLS):
            print(f"\n[ERROR] {label} {pos} is outside the grid.")
            return
        if MAZE[r][c] == 1:
            print(f"\n[ERROR] {label} {pos} is inside a wall.")
            return

    # Run A*
    t0 = time.perf_counter()
    path, explored, found = astar(
        MAZE, START, GOAL,
        heuristic=heuristic_fn,
        diagonal=DIAGONAL
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    # Console output
    if found:
        print(f"\n  ✅  Path found!")
        print(f"      Length   : {len(path)} steps")
        print(f"      Explored : {len(explored)} cells")
        print(f"      Time     : {elapsed_ms:.3f} ms")
    else:
        print(f"\n  ❌  No path found — goal is unreachable!")
        print(f"      Explored : {len(explored)} cells")

    print_maze(MAZE, path, explored)
    print("  Opening animation window...")

    # Launch animation
    animate(MAZE, explored, path, found, CHOSEN_HEURISTIC, elapsed_ms)


if __name__ == "__main__":
    main()
