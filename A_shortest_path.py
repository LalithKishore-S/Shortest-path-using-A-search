import numpy as np
import sympy as sp
import random as r

class node:
    x :int
    y :int
    fn :float
    def __init__(self):
        pass
    def __init__(self, x, y, fn):
        self.x = x
        self.y = y
        self.fn = fn

    def __str__(self):
        return f"Node(x={self.x}, y={self.y}, fn={self.fn})"


def create_obstacle_matrix(m,n,initial,final):
    A=np.zeros((m,n),dtype=bool)
    no_obstacles=2
    i=0
    while(i<no_obstacles):
        x=r.randint(0,m-1)
        y=r.randint(0,n-1)
        if (x==initial[0] and y==initial[1]) or (x==final[0] and y==final[1]):
            continue
        else:
            A[x][y]=True
            i+=1
    return A

def heuristic_function(x,y):
    return ((y[1]-x[1])**2+(y[0]-x[0])**2)**0.5

def compute_neighbours(current,obstacle_matrix,m,n):
    x=current[0]
    y=current[1]
    # max 8 neighbours for each node
    neighbour=[]
    for j in range(3):
       if (x-1)>=0:
           if (y-1+j>=0 and y-1+j<n):
              if obstacle_matrix[x-1][y-1+j]!=True:
                 node1=node(x-1,y-1+j,0)
                 node1.x=x-1
                 node1.y=y-1+j
                 neighbour.append(node1)
        
       if (x+1)<m:
           if (y-1+j>=0 and y-1+j<n):
               if obstacle_matrix[x+1][y-1+j]!=True:
                  node1=node(x+1,y-j+1,0)
                  node1.x=x+1
                  node1.y=y-1+j
                  neighbour.append(node1)

       if y-1+j!=y and y-1+j>=0 and y-1+j<n:
           if obstacle_matrix[x][y-1+j]!=True:
              node1=node(x,y-1+j,0)
              node1.x=x
              node1.y=y-1+j
              neighbour.append(node1)
    
    return neighbour
    

def main():
    Trail_tracker_matrix=np.zeros((4,4),dtype=bool)
 
    x_start=int(input("Enter the x coordinate of initial point:"))
    y_start=int(input("Enter the y coordinate of initial point:"))

    initial=(x_start,y_start)
    Trail_tracker_matrix[initial[0]][initial[1]]=True
    

    x_finish=int(input("Enter the x coordinate of final point:"))
    y_finish=int(input("Enter the y coordinate of final point:"))

    final=(x_finish,y_finish)

    obstacle_matrix=create_obstacle_matrix(4,4,initial,final)

    current=initial

    if initial==final:
        print("The initial and final points are same..")
        return
    
    path_length=1
    node_min=node(-1,-1,0)

    while(current != final):
        neighbour=compute_neighbours(current,obstacle_matrix,4,4)
        min=-float('inf')
        for neighbours in neighbour:
            sub_initial=(neighbours.x,neighbours.y)
            neighbours.fn=path_length+heuristic_function(sub_initial,final)
            if min > neighbours.fn:
                min=neighbours.fn
                node_min=neighbours
        current=(node_min.x,node_min.y)
        Trail_tracker_matrix[current[0]][current[1]]=True
    
    print(Trail_tracker_matrix)

#    print(Trail_tracker_matrix)
 #   print(obstacle_matrix)
#    print(initial)
 #   print(final)




main()
