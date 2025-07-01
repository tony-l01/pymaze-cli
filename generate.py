import random
from param import *

class Maze:
    DIRECTIONS = [(0, 2), (2, 0), (0, -2), (-2, 0)] # up, right, down, left
    
    def __init__(self, grid):
        self.grid = grid
        self.cols, self.rows = len(grid), len(grid)
        # Calculate the size of each cell to fit within the window
        self.cell_size = min(WIDTH // self.cols, HEIGHT // self.rows)

    def draw(self, current=None):
        SCREEN.fill(WHITE)
        start = (0, 0)
        end = (self.cols - 2, self.rows - 2)
        
        for x in range(self.cols):
            for y in range(self.rows):
                color = BLACK if self.grid[x][y] == 0 else WHITE
                if (x, y) == start:
                    color = RED
                elif (x, y) == end:
                    color = GREEN

                pygame.draw.rect(SCREEN, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        if current is not None:
            x, y = current
            pygame.draw.rect(SCREEN, RED, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
        pygame.display.update()
        
    def get_neighbors(self, grid, current, visited):
        neighbors = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            # Check if the neighboring cell is a valid wall and has not been visited.
            if 0 <= nx < self.cols and 0 <= ny < self.rows and grid[nx][ny] == 0 and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        return neighbors

    def dfs(self):
        current = (0, 0)
        self.grid[current[0]][current[1]] = 1
        stack = [current]
        
        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # Get neighboring cells of the current cell.
            neighbors = self.get_neighbors(self.grid, current, stack)
            if neighbors:
                # Randomly select a neighboring cell and form a path between current and neighbor.
                next = random.choice(neighbors)
                self.grid[next[0]][next[1]] = 1
                self.grid[(current[0] + next[0]) // 2][(current[1] + next[1]) // 2] = 1
                stack.append(current)
                current = next
            
            elif stack:
                current = stack.pop()
            self.draw(current)
            CLOCK.tick(FPS)
            
        return self.grid
    
    def bfs(self):
        current = (0, 0)
        self.grid[current[0]][current[1]] = 1
        queue = [current]
        
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            neighbors = self.get_neighbors(self.grid, current, queue)
            if neighbors:
                next = random.choice(neighbors)
                self.grid[next[0]][next[1]] = 1
                self.grid[(current[0] + next[0]) // 2][(current[1] + next[1]) // 2] = 1
                queue.append(current)
                current = next
            
            elif queue:
                current = queue.pop(0)
            self.draw(current)
            CLOCK.tick(FPS)
        
        return self.grid
    
    def kruskal(self):
        edges = []
        # Initialize a dictionary to keep track of the parent cell for each cell.
        parent = {(x, y): (x, y) for x in range(0, self.cols, 2) for y in range(0, self.rows, 2)}
        
        def find(node):
            if parent[node] != node:
                # Perform path compression by setting the parent of the current node to its root.
                parent[node] = find(parent[node]) 
                
            return parent[node]
        
        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 == root2:
                # If both nodes have the same root they are already connected and no union is needed.
                return False
            parent[root2] = root1
            # Set the parent of the root of node2 to the root of node1 to merge the two sets.
            return True
        
        for x in range(0, self.cols, 2):
            for y in range(0, self.rows, 2):
                if x > 1 :
                    # Add the edge between the current cell and its left neighbor to the list of edges.
                    edges.append(((x, y), (x - 2, y)))
                if y > 1:
                    # Add the edge between the current cell and its top neighbor to the list of edges.
                    edges.append(((x, y), (x, y - 2)))
        # Shuffle the list of edges randomly to ensure randomness in the generation process.
        random.shuffle(edges)
        
        for edge in edges:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            node1, node2 = edge
            '''
            Perform a union operation on the two nodes. 
            If they are not already connected, this creates a new path between them.
            '''
            if union(node1, node2):
                x1, y1 = node1
                x2, y2 = node2
                self.grid[x1][y1] = 1
                self.grid[x2][y2] = 1
                self.grid[(x1 + x2) // 2][(y1 + y2) // 2] = 1
                self.draw((x1, y1))
                CLOCK.tick(FPS)
                
        return self.grid
    
    def prim(self):
        current = (random.randrange(0, self.cols - 2, 2), random.randrange(0, self.rows - 2, 2))
        self.grid[current[0]][current[1]] = 1
        edge = self.get_neighbors(self.grid, current, [])

        while edge:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            current = random.choice(edge)
            edge.remove(current)
            neighbors = []
            # Calculate the coordinates of the neighboring cell.
            for dx, dy in self.DIRECTIONS:
                    nx, ny = current[0] + dx, current[1] + dy
                    if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[nx][ny] == 1:
                        neighbors.append((nx, ny))
            
            if neighbors:
                next = random.choice(neighbors)
                self.grid[current[0]][current[1]] = 1
                self.grid[(current[0] + next[0]) // 2][(current[1] + next[1]) // 2] = 1
                edge.extend(self.get_neighbors(self.grid, current, edge))
                
            self.draw(current)
            CLOCK.tick(FPS)
            
        return self.grid