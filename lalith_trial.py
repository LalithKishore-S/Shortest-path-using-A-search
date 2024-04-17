import math
import heapq
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

class robot:
    def __init__(self,p,src,dest):
        self.priority=p
        self.src=src
        self.dest=dest
        self.path=[]
        self.path_time=[]
        
class Cell:
	def __init__(self):
		self.parent_i = 0 # Parent cell's row index
		self.parent_j = 0 # Parent cell's column index
		self.f = float('inf') # Total cost of the cell (g + h)
		self.g = float('inf') # Cost from start to this cell
		self.h = 0 # Heuristic cost from this cell to destination

# Define the size of the grid
ROW = 9
COL = 10

# Check if a cell is valid (within the grid)
def is_valid(row, col):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
	return grid[row][col] == 1

# Check if a cell is the destination
def is_destination(row, col, dest):
	return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
	return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
	print("The Path is ")
	path = []
	row = dest[0]
	col = dest[1]

	# Trace the path from destination to source using parent cells
	while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
		path.append((row, col))
		temp_row = cell_details[row][col].parent_i
		temp_col = cell_details[row][col].parent_j
		row = temp_row
		col = temp_col

	# Add the source cell to the path
	path.append((row, col))
	# Reverse the path to get the path from source to destination
	path.reverse()

	# Print the path
	for i in path:
		print("->", i, end=" ")
	print()
	return path

# Implement the A* search algorithm
def a_star_search(grid, src, dest):
	# Check if the source and destination are valid
	if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
		print("Source or destination is invalid")
		return

	# Check if the source and destination are unblocked
	if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
		print("Source or the destination is blocked")
		return

	# Check if we are already at the destination
	if is_destination(src[0], src[1], dest):
		print("We are already at the destination")
		return

	# Initialize the closed list (visited cells)
	closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
	# Initialize the details of each cell
	cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

	# Initialize the start cell details
	i = src[0]
	j = src[1]
	cell_details[i][j].f = 0
	cell_details[i][j].g = 0
	cell_details[i][j].h = 0
	cell_details[i][j].parent_i = i
	cell_details[i][j].parent_j = j

	# Initialize the open list (cells to be visited) with the start cell
	open_list = []
	heapq.heappush(open_list, (0.0, i, j))

	# Initialize the flag for whether destination is found
	found_dest = False

	# Main loop of A* search algorithm
	while len(open_list) > 0:
		# Pop the cell with the smallest f value from the open list
		p = heapq.heappop(open_list)

		# Mark the cell as visited
		i = p[1]
		j = p[2]
		closed_list[i][j] = True

		# For each direction, check the successors
		directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
		for dir in directions:
			new_i = i + dir[0]
			new_j = j + dir[1]

			# If the successor is valid, unblocked, and not visited
			if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
				# If the successor is the destination
				if is_destination(new_i, new_j, dest):
					# Set the parent of the destination cell
					cell_details[new_i][new_j].parent_i = i
					cell_details[new_i][new_j].parent_j = j
					print("The destination cell is found")
					# Trace and print the path from source to destination
					path = trace_path(cell_details, dest)
					found_dest = True
					return path
				else:
					# Calculate the new f, g, and h values
					g_new = cell_details[i][j].g + 1.0
					h_new = calculate_h_value(new_i, new_j, dest)
					f_new = g_new + h_new

					# If the cell is not in the open list or the new f value is smaller
					if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
						# Add the cell to the open list
						heapq.heappush(open_list, (f_new, new_i, new_j))
						# Update the cell details
						cell_details[new_i][new_j].f = f_new
						cell_details[new_i][new_j].g = g_new
						cell_details[new_i][new_j].h = h_new
						cell_details[new_i][new_j].parent_i = i
						cell_details[new_i][new_j].parent_j = j

	# If the destination is not found after visiting all cells
	if not found_dest:
		print("Failed to find the destination cell")

def visualize_grid_with_robots(grid,robot1, robot2):
    m, n = grid.shape
    temp=0
    src1=robot1.src
    src2=robot2.src
    dest1=robot1.dest
    dest2=robot2.dest
    robot1_positions=robot1.path
    robot2_positions=robot2.path
    plt.ion()  # Turn on interactive mode

    for t in range(max(len(robot1_positions),len(robot2_positions))):
        plt.clf()  # Clear the previous plot
        plt.imshow(grid, cmap='viridis', interpolation='nearest')
        plt.colorbar()

        # Customize x-axis scale for labels
        x_labels = [i for i in range(n)]
        plt.xticks(np.arange(n), x_labels)

        # Customize y-axis scale for labels
        y_labels = [i for i in range(m)]
        plt.yticks(np.arange(m), y_labels)

        # Draw grid lines
        ax = plt.gca()
        ax.set_xticks(np.arange(-0.5, n), minor=True)
        ax.set_yticks(np.arange(-0.5, m), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

        # Create legend patches
        colors = plt.cm.viridis
        legend_patches = [mpatches.Patch(color=colors(0), label='blocked'),
                          mpatches.Patch(color=colors(255), label='free')]  # Corrected colormap index
        plt.legend(handles=legend_patches, title='Legend', loc='upper right')

        # Add text for source and destination
        plt.text(src1[1], src1[0], 'FROM', ha='center', va='center', color='red')
        plt.text(dest1[1], dest1[0], 'TO', ha='center', va='center', color='red')
        plt.text(src2[1], src2[0], 'FROM', ha='center', va='center', color='red')
        plt.text(dest2[1], dest2[0], 'TO', ha='center', va='center', color='red')

        # Plot the robots
        if t<len(robot1_positions):
            plt.scatter(robot1_positions[t][1], robot1_positions[t][0], color='blue', label='Robot 1')
        else:
            temp=len(robot1_positions)-1
            plt.scatter(robot1_positions[temp][1], robot1_positions[temp][0], color='blue', label='Robot 1')
        if t<len(robot2_positions):
            plt.scatter(robot2_positions[t][1], robot2_positions[t][0], color='green', label='Robot 2')
        else:
            temp=len(robot1_positions)-1
            plt.scatter(robot2_positions[temp][1], robot2_positions[temp][0], color='green', label='Robot 2')
        plt.legend()

        plt.pause(0.5)  # Pause for a short time to show the plot

    plt.ioff()  # Turn off interactive mode after the loop
    plt.show()
    
    
def main():
   import numpy as np

	# Define the grid (1 for unblocked, 0 for blocked)
   grid = np.array([
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
   robots=[]
   for i in range(2):
       s_x=int(input("Enter the source x for robot %d :"%(i+1)))
       s_y=int(input("Enter the source y for robot %d :"%(i+1)))
       d_x=int(input("Enter the destination x for robot %d :"%(i+1)))
       d_y=int(input("Enter the destination y for robot %d :"%(i+1)))
       p=int(input("Enter the priority of the robot:"))
       robots.append(robot(p,(s_x,s_y),(d_x,d_y)))
       robots[i].path=a_star_search(grid,robots[i].src,robots[i].dest)
       #print(robots[i].path) 
   count=[1,1] #position for each robot
   time=[0,0] # time in each cell for each robot
   while(True):
       if robots[0].path[count[0]]!=robots[1].path[count[1]]:
           robots[0].path_time.append((robots[0].path[count[0]-1][0],robots[0].path[count[0]-1][1],time[0]))
           robots[1].path_time.append((robots[1].path[count[1]-1][0],robots[1].path[count[1]-1][1],time[1]))
           time=[0,0]
           for i in range(len(count)):
               count[i]+=1
       else:
           if robots[0].priority>robots[1].priority:
               robots[0].path_time.append((robots[0].path[count[0]-1][0],robots[0].path[count[0]-1][1],time[0]))
               time[1]+=1
               count[0]+=1
           else:
               robots[1].path_time.append((robots[1].path[count[1]-1][0],robots[1].path[count[1]-1][1],time[1]))
               time[0]+=1
               count[1]+=1
       if count[0]==len(robots[0].path) or count[1]==len(robots[1].path):
           break
   time=[0,0]
   while(count[0]==len(robots[0].path) and count[1]<len(robots[1].path)):
       robots[1].path_time.append((robots[1].path[count[1]-1][0],robots[1].path[count[1]-1][1],time[1]))
       count[1]+=1
   robots[1].path_time.append((robots[1].dest[0],robots[1].dest[1],0))
   while(count[0]<len(robots[0].path) and count[1]==len(robots[1].path)):
       robots[0].path_time.append((robots[0].path[count[0]-1][0],robots[0].path[count[0]-1][1],time[0]))
       count[0]+=1
   robots[0].path_time.append((robots[0].dest[0],robots[0].dest[1],0))
   print(robots[0].path_time)
   print(robots[1].path_time)  
   
   for i in range(len(robots[0].path_time)):
       if robots[0].path_time[i][2]==1:
           robots[0].path.insert(i+1,robots[0].path[i])
   for i in range(len(robots[1].path_time)):
       if robots[1].path_time[i][2]==1:
           robots[1].path.insert(i+1,robots[1].path[i])
   print(robots[0].path)
   print(robots[1].path) 
   visualize_grid_with_robots(grid,robots[0], robots[1])
       
if __name__=="__main__":
    main()
