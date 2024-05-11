import random


class GridEnvironment:
    def __init__(self, m, n, start_pos, num_goals, num_agents):
        self.m = m
        self.n = n
        self.start_pos = start_pos
        self.num_goals = num_goals
        self.num_agents = num_agents
        self.goals_found = set()
        # Initialize positions for all agents
        self.agent_positions = [start_pos] * num_agents
        self.grid = [[None for _ in range(n)] for _ in range(m)]
        self.generate_environment()

    def generate_environment(self):
        # Place start position
        p1, p2 = self.start_pos

        # Place goals
        goal_positions = []
        for k in range(self.num_goals):
            goal_pos = (random.randint(0, self.m-1),
                        random.randint(0, self.n-1))
            while self.grid[goal_pos[0]][goal_pos[1]] is not None:
                goal_pos = (random.randint(0, self.m-1),
                            random.randint(0, self.n-1))
            goal_positions.append(goal_pos)
            self.grid[goal_pos[0]][goal_pos[1]] = f'G({k})'

        # Randomly populate with coins, potholes, and barriers
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] is None:
                    rand_num = random.random()
                    if rand_num < 0.1:  # 10% chance of pothole
                        self.grid[i][j] = f'O({random.randint(-50, -10)})'
                    elif rand_num < 0.3:  # 20% chance of coin
                        self.grid[i][j] = f'C({random.randint(1, 20)})'
                    elif rand_num < 0.35:  # 5% chance of barrier
                        self.grid[i][j] = 'X'
                    else:
                        self.grid[i][j] = ' '  # Empty space
        # Randomly place agents, making sure they're not on goal positions
        for agent_id in range(self.num_agents):
            agent_pos = (random.randint(0, self.m-1),
                         random.randint(0, self.n-1))
            while agent_pos in goal_positions or self.grid[agent_pos[0]][agent_pos[1]] == 'A':
                agent_pos = (random.randint(0, self.m-1),
                             random.randint(0, self.n-1))
            self.agent_positions[agent_id] = agent_pos
            self.grid[agent_pos[0]][agent_pos[1]] = 'A'

    def print_grid(self):
        for i in range(self.m):
            for j in range(self.n):
                cell_content = self.grid[i][j]
                if cell_content:
                    print(cell_content, end=' ')
                else:
                    print(' ', end=' ')
            print()

    def is_valid_move(self, i, j):
        return (
            0 <= i < self.m and 
            0 <= j < self.n and 
            self.grid[i][j] != 'X' and 
            self.grid[i][j] != 'A'
        )


    def get_neighbors(self, i, j):
        neighbors = []
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if self.is_valid_move(ni, nj):
                neighbors.append((ni, nj))
        return neighbors

    def heuristic(self, current_pos, goal_pos):
        return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

    def get_goal_position(self, goal_id):
        for i in range(self.m):
            for j in range(self.n):
                cell_content = self.grid[i][j]
                if cell_content and cell_content.startswith('G') and int(cell_content.split('(')[1][:-1]) == goal_id:
                    return (i, j)
        return None
