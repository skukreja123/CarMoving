import heapq
import queue
from environment import GridEnvironment
from collections import deque


def bfs_search(env, start, goal):
    frontier = deque([(start, [])])
    explored = set()

    while frontier:
        current, path = frontier.popleft()
        if current == goal:
            return path + [current]
        if current in explored:
            continue
        for neighbor in env.get_neighbors(*current):
            if neighbor not in explored and env.grid[neighbor[0]][neighbor[1]] != 'A':  # Check if neighbor is not an agent position
                frontier.append((neighbor, path + [current]))
        explored.add(current)
    return None

def dfs_search(env, start, goal):
    frontier = [(start, [])]
    explored = set()

    while frontier:
        current, path = frontier.pop()
        if current == goal:
            return path + [current]
        if current in explored:
            continue
        for neighbor in env.get_neighbors(*current):
            if neighbor not in explored and env.grid[neighbor[0]][neighbor[1]] != 'A':  # Check if neighbor is not an agent position
                frontier.append((neighbor, path + [current]))
        explored.add(current)
    return None

def a_star_search(env, start, goal, heuristic):
    frontier = queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for next in env.get_neighbors(*current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                if env.grid[next[0]][next[1]] != 'A':  # Check if next position is not an agent position
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
    return None
