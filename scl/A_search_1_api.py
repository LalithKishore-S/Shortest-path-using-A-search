
from pyvis.network import Network
import networkx as nx
import math
import heapq
 
# Define the Cell class
class Cell:
    def __init__(self,a):
        self.parent = -1  # Parent cell's  index
        self.latitude=a[0]
        self.longitude=a[1]
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
 
# Define the size of the grid
#ROW = 9
#COL = 10


def generate_adj_list(pyvis_graph):
    adj_list = {}
    VERTICES = pyvis_graph.get_nodes()
    EDGES = pyvis_graph.get_edges()

    for i in VERTICES:
        adj_list[i] = []

    for i in EDGES:
        adj_list[i['from']].append(i['to'])
        adj_list[i['to']].append(i['from'])
    #print(adj_list)
    return adj_list

def generate_adj_martix(pyvis_graph):
    VERTICES = pyvis_graph.get_nodes()
    n = len(VERTICES)
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    EDGES = pyvis_graph.get_edges()
    for i in EDGES:
        adj_matrix[i['from']-1][i['to']-1] = i['value']
        adj_matrix[i['to']-1][i['from']-1] = i['value']
    #print(adj_matrix)
    return adj_matrix

#def is_valid(row, col):
 #   return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)
 
# Check if a cell is unblocked
def is_unblocked(block,place):
    return place!=block
 
# Check if a cell is the destination
def is_destination(place, dest):
    return place==dest
 
# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(place, dest):
    r=6571
    return 2*r*math.asin(math.sqrt(math.sin(math.radians((dest.latitude-place.latitude)/2))**2+math.cos(math.radians(place.latitude))*math.cos(math.radians(dest.latitude))*math.sin(math.radians((dest.longitude-place.longitude)/2))**2))
 
# Trace the path from source to destination
def trace_path(cell_details, dest, locations):
    print("The Path is ")
    path = []
    place = dest
 
    # Trace the path from destination to source using parent cells
    while not (cell_details[place].parent == place):
        path.append(place+1)
        temp_place = cell_details[place].parent
        place = temp_place
 
    # Add the source cell to the path
    path.append(place+1)
    # Reverse the path to get the path from source to destination
    path.reverse()
 
    # Print the path
    for i in path:
        print("->", locations[i], end=" ")
    print()
 
# Implement the A* search algorithm
def a_star_search(adj_list,adj_matrix, src, dest, block, loc, places):
    # Check if the source and destination are valid
   # if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
    #    print("Source or destination is invalid")
    #    return
 
    # Check if the source and destination are unblocked
    if not is_unblocked(block, src) or not is_unblocked(block, dest):
        print("Source or the destination is blocked")
        return
 
    # Check if we are already at the destination
    if is_destination(src,dest):
        print("We are already at the destination")
        return
 
    # Initialize the closed list (visited cells)
    closed_list = [False for _ in range(1,10)]
    # Initialize the details of each cell
    # loc=[(10.956455,76.972296),(10.988052,76.961595),(10.964746,76.987609),(10.998326,76.985056),(10.996996,76.995915),(11.012854,76.986207),(11.002055,77.015386),(11.024660,77.010170),(11.024544,77.002729)]
    cell_details = [Cell(loc[k]) for k in range(9)]
 
    # Initialize the start cell details
    i = src
    cell_details[i].f = 0
    cell_details[i].g = 0
    cell_details[i].h = 0
    cell_details[i].parent = i
 
    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i))
 
    # Initialize the flag for whether destination is found
    found_dest = False
 
    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)
 
        # Mark the cell as visited
        i = p[1]
        closed_list[i] = True
 
        # For each direction, check the successors
        directions = adj_list[i+1]
        for dir in directions:
            new_i =dir -1
 
            # If the successor is valid, unblocked, and not visited
            if is_unblocked(block, new_i) and not closed_list[new_i]:
                # If the successor is the destination
                if is_destination(new_i, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i].parent = i
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest, places)                     
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i].g + adj_matrix[i][new_i]                 
                    h_new = calculate_h_value(cell_details[new_i],cell_details[dest])  
                    f_new = g_new + h_new
 
                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i].f == float('inf') or cell_details[new_i].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i))
                        # Update the cell details
                        cell_details[new_i].f = f_new
                        cell_details[new_i].g = g_new
                        cell_details[new_i].h = h_new
                        cell_details[new_i].parent = i
 
    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

def main():
   pyvis_graph = Network(directed=True)
   nx_graph = nx.MultiGraph()

   places = {
        1: 'Abinand Hospital',
        2: 'Ukkadam Bus Stand',
        3: 'Podanur Junction',
        4: 'Sungam Junction Coimbatore',
        5: 'Ramanathapuram Coimbatore',
        6: 'Lakshmi Mills Coimbatore',
        7: 'Perks Road Coimbatore',
        8: 'Fun Republic Mall Coimbatore',
        9: 'PSG College of Technology'
    }

   for i in places.keys():
        nx_graph.add_node(i, label=str(i))

   def lat_lon_api(place):
       import requests
       url = "https://api.geoapify.com/v1/geocode/search?text=" + place + "&format=json&apiKey=67f3b4876f964d49a0bfc8150d784964"
       response = requests.get(url)

       output = response.json()
       lat, lon = output['results'][0]['lat'], output['results'][0]['lon']

       return (lat, lon)

   def distance_api(p1, p2):
       import requests
       url1 = "https://api.geoapify.com/v1/geocode/search?text=" + p1 + "&format=json&apiKey=67f3b4876f964d49a0bfc8150d784964"
       url2 = "https://api.geoapify.com/v1/geocode/search?text=" + p2 + "&format=json&apiKey=67f3b4876f964d49a0bfc8150d784964"

       response1 = requests.get(url1)
       response2 = requests.get(url2)

       output1 = response1.json()
       output2 = response2.json()
       
       lat1, lon1 = output1['results'][0]['lat'], output1['results'][0]['lon']
       lat2, lon2 = output2['results'][0]['lat'], output2['results'][0]['lon']

       url = f"https://api.geoapify.com/v1/routing?waypoints={lat1},{lon1}|{lat2},{lon2}&mode=drive&apiKey=67f3b4876f964d49a0bfc8150d784964"
       response = requests.get(url)
       output = response.json()

       return output['features'][0]['properties']['distance']

   nx_graph.add_edges_from([(1,2,{'weight': distance_api(places[1], places[2])}),
                         (1,3,{'weight': distance_api(places[1], places[3])}),
                         (2,3,{'weight': distance_api(places[2], places[3])}),
                         (2,4,{'weight': distance_api(places[2], places[4])}),
                         (3,5,{'weight': distance_api(places[3], places[5])}),
                         (4,5,{'weight': distance_api(places[4], places[5])}),
                         (4,6,{'weight': distance_api(places[4], places[6])}),
                         (5,6,{'weight': distance_api(places[5], places[6])}),
                         (5,7,{'weight': distance_api(places[5], places[7])}),
                         (7,8,{'weight': distance_api(places[7], places[8])}),
                         (6,9,{'weight': distance_api(places[6], places[9])}),
                         (8,9,{'weight': distance_api(places[8], places[9])})])
   
   loc = []
   for i in places.keys():
       loc.append(lat_lon_api(places[i]))

   for i in places.keys():
        pyvis_graph.add_node(i, label=places[i])
   EDGES = pyvis_graph.get_edges()
   # Iterate through edges and aggregate weights
   for u, v, data in nx_graph.edges(data=True):
       # Check if the edge already exists in Pyvis
       #if {'value': data['weight'], 'from': u, 'to': v} not in EDGES:
       print(u,v,data)
        # If the edge doesn't exist, add it with weight as the aggregation
       pyvis_graph.add_edge(u, v, value=data['weight'], label=str(data['weight']), arrows = "hi", color = 'blue')
       EDGES = pyvis_graph.get_edges()
       #print(EDGES)
   adj_list = generate_adj_list(pyvis_graph)
   adj_matrix = generate_adj_martix(pyvis_graph)
   pyvis_graph.set_edge_smooth('dynamic')
   pyvis_graph.show_buttons()
   pyvis_graph.write_html("basic.html", open_browser=True)

   src = (1-1)  #from sundarapuram 1st location but index=0 in adj_matrix
   dest = (9-1) #to PSGTECH 9th location but index=8 in adj_matrix

   print(places)
   check_block=input("Is there any block in any of the given locations: ")
   blocked_place=-1
   if check_block=="yes":
       blocked_place=int(input("Enter the blocked place's corresponding number: "))

    # Run the A* search algorithm
   a_star_search(adj_list, adj_matrix, src, dest, blocked_place, loc, places)


if __name__=='__main__':
    main()
