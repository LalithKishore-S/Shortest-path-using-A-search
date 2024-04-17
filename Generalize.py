import heapq
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import time

global grid

class robot:
	def __init__(self,p,src,dest):
		self.priority=p
		self.src=src
		self.dest=dest
		self.curr=0
		self.path=a_star_search(src, dest)
	
	def source_block(self):
		global grid
		'''
		if grid[self.src[0]][self.src[1]] == 0:
			print('Two robots cannot have same source')
			exit(0)
		else:
			grid[self.src[0]][self.src[1]] = 0
		'''

	def move(self):
		if self.curr == len(self.path) - 1:
			return
		next = self.path[self.curr+1]
		if is_unblocked(next[1], next[0]):
			print('P: ', self.priority)
			global grid
			pos = self.path[self.curr]
			grid[pos[1]][pos[0]] = 1
			print('Old pos: ', pos)
			self.curr += 1
			pos = self.path[self.curr]
			grid[pos[1]][pos[0]] = 0
			print('New pos: ', pos)

class Cell:
	def __init__(self):
		self.parent_i = 0 # Parent cell's row index
		self.parent_j = 0 # Parent cell's column index
		self.f = float('inf') # Total cost of the cell (g + h)
		self.g = float('inf') # Cost from start to this cell
		self.h = 0 # Heuristic cost from this cell to destination

# Define the size of the grid
ROW = 10
COL = 10

# Check if a cell is valid (within the grid)
def is_valid(row, col):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(row, col):
	global grid
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
def a_star_search(src, dest):
	global grid
	# Check if the source and destination are valid
	if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
		print("Source or destination is invalid")
		return

	# Check if the source and destination are unblocked
	if not is_unblocked(src[0], src[1]) or not is_unblocked(dest[0], dest[1]):
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
			if is_valid(new_i, new_j) and is_unblocked(new_i, new_j) and not closed_list[new_i][new_j]:
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

def main():
	import numpy as np

	# Define the grid (1 for unblocked, 0 for blocked)
	global grid
	m, n = 10, 10
	grid = np.ones((m, n))
	robots = []
	rn = int(input('Enter number of robots: (1 to 10): '))
	if rn < 1 or rn > 10:
		exit(0)
	for i in range(rn):
		print('Enter source of robot 1')
		x1 = int(input('x = '))
		y1 = int(input('y = '))
		print('Enter destination of robot 1')
		x2 = int(input('x = '))
		y2 = int(input('y = '))
		p = int(input('Enter priority of robot 1: '))
		robots.append(robot(p, (x1, y1), (x2, y2)))
		robots[-1].source_block()
	
	robots.sort(key=lambda x: x.priority, reverse=True)

	d1 = {r: [[r.src[0], r.src[1], 0]] for r in robots}
	for i in range(1, 10):
		for j in robots:
			j.move()
			if j.path[j.curr][0] == j.dest[0] and j.path[j.curr][1] == j.dest[1]:
				continue
			t = [j.path[j.curr][0], j.path[j.curr][1], i]
			d1[j].append(t)

	for i in robots:
		d1[i].append([i.dest[0], i.dest[1], d1[i][-1][-1] + 1])

	for i in d1.keys():
		print('P: ', i.priority)
		print(d1[i])
	visualize_grid_with_robots(d1)

def visualize_grid_with_robots(d1):
	global grid
	m, n = grid.shape

	t = 0
	for i in d1.values():
		for j in i:
			if j[2] > t:
				t = j[2]

	plt.ion()  # Turn on interactive mode

	for t in range(t):
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
		for i in d1.keys():
			plt.text(i.src[0], i.src[1], 'FROM', ha='center', va='center', color='red')
			plt.text(i.dest[0], i.dest[1], 'TO', ha='center', va='center', color='red')

		colors = plt.cm.tab10(np.linspace(0, 1, len(d1.keys())))

		tt = 0
        # Plot the robots
		for i in d1.keys():
			pri = i.priority
			temp = d1[i]
			for j in temp:
				if j[2] == 0:
					plt.scatter(j[0], j[1], color=colors[tt], label=f'P: {pri}')
				elif j[2] <= t:
					plt.scatter(j[0], j[1], color=colors[tt])
			tt += 1

			plt.legend()
			plt.pause(1.5)  # Pause for a short time to show the plot

	plt.ioff()  # Turn off interactive mode after the loop
	plt.show()

main()
