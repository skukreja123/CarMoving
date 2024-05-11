import tkinter as tk

def visualize_environment(env):
    root = tk.Tk()
    root.title("Grid Environment")
    
    colors = {
        'S': 'green',  # Start position
        'G': 'blue',   # Goals
        'C': 'gold',   # Coins
        'O': 'red',    # Potholes
        'X': 'black'   # Barriers
    }
    
    # Define colors for different goals
    goal_colors = {}
    goals = set()
    for i in range(env.m):
        for j in range(env.n):
            cell_content = env.grid[i][j]
            if cell_content and cell_content.startswith('G'):
                goals.add(cell_content)
    goals = list(goals)
    num_goals = len(goals)
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'yellow']  # Add more colors as needed
    for i in range(num_goals):
        goal_colors[goals[i]] = colors[i % len(colors)]

    # Display the grid environment with colors for goals
    for i in range(env.m):
        for j in range(env.n):
            cell_content = env.grid[i][j]
            bg_color = 'white'
            if cell_content:
                if cell_content.startswith('G'):
                    bg_color = goal_colors[cell_content]
            label = tk.Label(root, text=str(cell_content), width=6, height=3, borderwidth=1, relief="solid", bg=bg_color)
            label.grid(row=i, column=j)

    root.mainloop()


import time

def visualize_path(env, path):
    root = tk.Tk()
    root.title("Path Visualization")

    colors = {
        'S': 'green',  # Start position
        'G': 'blue',   # Goals
        'C': 'gold',   # Coins
        'O': 'red',    # Potholes
        'X': 'black',  # Barriers
        'Agent': 'purple',  # Agent
    }

    # Color gradient for the path
    color_gradient = ['#ff0000', '#ff3300', '#ff6600', '#ff9900', '#ffcc00', '#ffff00', '#ccff00', '#99ff00', '#66ff00', '#33ff00', '#00ff00']

    for i in range(env.m):
        for j in range(env.n):
            cell_content = env.grid[i][j]
            if (i, j) in path:
                idx = min(len(path) - 1, path.index((i, j)))
                color_idx = min(idx, len(color_gradient) - 1)
                label = tk.Label(root, text=str(cell_content), width=6, height=3, borderwidth=1, relief="solid", bg=color_gradient[color_idx])
            elif cell_content.startswith('A'):
                label = tk.Label(root, text=str(cell_content), width=6, height=3, borderwidth=1, relief="solid", bg=colors['Agent'])
            else:
                label = tk.Label(root, text=str(cell_content), width=6, height=3, borderwidth=1, relief="solid", bg=colors.get(cell_content, 'white'))
            label.grid(row=i, column=j)

            root.update()  # Update the GUI to show changes
            time.sleep(0.1)  # Add a delay to visualize the movement

    root.mainloop()

