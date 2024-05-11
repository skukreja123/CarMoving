import random
from agent import Agent
from environment import GridEnvironment
import search
from visualization import visualize_environment
from visualization import visualize_path
from search import bfs_search, dfs_search, a_star_search


# Define agent strategy function
def agent_strategy(agent, grid, env, goals_found):
    # Placeholder for agent strategy
    # For now, let's move the agent randomly
    valid_moves = env.get_neighbors(*agent.position)
    return random.choice(valid_moves) if valid_moves else agent.position

# Define alpha-beta search function
def alpha_beta_search(agent, depth, alpha, beta, grid, env, goals_found):
    # Check if depth limit reached or if the game is over
    if depth == 0 or env.is_game_over():
        return calculate_utility(agent, grid, env.start_pos)

    if agent.strategy == 'max':
        v = -float('inf')
        for action in env.get_valid_actions(agent):
            v = max(v, alpha_beta_search(action, depth - 1, alpha, beta, grid, env, goals_found))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float('inf')
        for action in env.get_valid_actions(agent):
            v = min(v, alpha_beta_search(action, depth - 1, alpha, beta, grid, env, goals_found))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

# Define utility function
def calculate_utility(agent, grid, start_pos):
    utility = 0
    for row in grid:
        for cell_content in row:
            if cell_content:
                if cell_content.startswith('C'):
                    coin_value = int(cell_content.split('(')[1].split(')')[0])
                    utility += coin_value
                elif cell_content.startswith('O'):
                    pothole_value = int(cell_content.split('(')[1].split(')')[0])
                    utility -= pothole_value
    return utility

# Define main function
import random

def main():
    # User input for grid size, starting position, number of goals, and number of agents
    m = int(input("Enter number of rows: "))
    n = int(input("Enter number of columns: "))
    start_pos = tuple(map(int, input("Enter starting position (row, col): ").split()))
    num_agents = int(input("Enter number of agents: "))
    num_goals = int(input("Enter number of goals: "))

    # Initialize the grid environment
    env = GridEnvironment(m, n, start_pos, num_goals, num_agents)
    print("Generated Environment:")
    env.print_grid()
    
    # Visualize the initial environment
    visualize_environment(env)

    prev_goal_positions = set()
    for i in range(m):
        for j in range(n):
            if env.grid[i][j] is not None and env.grid[i][j].startswith('G'):
                prev_goal_positions.add((i, j))

    for goal_id in range(num_goals):
        goal_pos = (random.randint(0, m - 1), random.randint(0, n - 1))
        while goal_pos in prev_goal_positions:
            goal_pos = (random.randint(0, m - 1), random.randint(0, n - 1))
        # env.grid[goal_pos[0]][goal_pos[1]] = f'G({goal_id})'

    agent_paths = {}
    agent_steps = {}
    for agent_id in range(num_agents):
        agent = Agent(agent_id, env.agent_positions[agent_id], 'max') 
        agent_paths[agent_id] = {}
        agent_steps[agent_id] = {}
        for goal_id in range(num_goals):
            goal_pos = env.get_goal_position(goal_id)
            for search_algorithm in [bfs_search, dfs_search, a_star_search]:
                if search_algorithm == a_star_search:
                    path = search_algorithm(env, agent.position, goal_pos, env.heuristic)  
                else:
                    path = search_algorithm(env, agent.position, goal_pos)  
                
                if path:
                    print(f"Path found by {search_algorithm.__name__} for Agent {agent_id} to Goal {goal_id}: {path}")
                    visualize_path(env, path)
                    agent_paths[agent_id][(search_algorithm.__name__, goal_id)] = path
                    agent_steps[agent_id][(search_algorithm.__name__, goal_id)] = [] 
                else:
                    print(f"No path found by {search_algorithm.__name__} for Agent {agent_id} to Goal {goal_id}")

    # Find the correct search algorithm path
    correct_path = None
    for agent_id in agent_paths:
        if 'a_star_search' in agent_paths[agent_id]:
            correct_path = agent_paths[agent_id]['a_star_search']
            break

    if correct_path:
        print(f"Correct path found by A* Search: {correct_path}")
        visualize_path(env, correct_path)

    # Calculate utility for each agent
    for agent_id in range(num_agents):
        agent = Agent(agent_id, env.agent_positions[agent_id], 'max')
        utility = calculate_utility(agent, env.grid, start_pos)
        print(f"Utility for Agent {agent_id}: {utility}")
        
    print("\nComparison of Search Algorithms:")
    print("-------------------------------")
    print("The A* search algorithm tends to find the optimal path,")
    print("especially when there are obstacles (like potholes) in the grid.")
    print("BFS and DFS may find suboptimal paths and can get stuck in certain scenarios.")
    print("However, BFS guarantees the shortest path in terms of number of steps.")
    print("DFS may take longer but could find a different path.")
    print("A* search combines the benefits of both, ensuring optimality while")
    print("also considering heuristic information to guide the search process.")

# Call main function
if __name__ == "__main__":
    main()

