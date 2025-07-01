import heapq
from param import *
from generate import Maze

class Pathfinder(Maze):
    def __init__(self, grid):
        super().__init__(grid)
        self.grid = grid
        self.cols, self.rows = len(grid), len(grid)
        self.cell_size = min(WIDTH // self.cols, HEIGHT // self.rows)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def draw(self, current, shortest=False):
        color = RED if shortest else BLUE
        pygame.draw.rect(SCREEN, color, (current[0] * self.cell_size, current[1] * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()

    def get_neighbors(self, grid, x, y):
        neighbors = []
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.cols and 0 <= ny < self.rows and grid[nx][ny] == 1):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def reconstruct_path(self, came_from, end):
        # reconstruct and draw the shortest path from start to end.
        current = end
        while current in came_from:
            current = came_from[current]
            self.draw(current, True)

    def dfs(self):
        current = (0, 0)
        end = (self.cols - 2, self.rows - 2)
        stack = [current]
        came_from = {}
        visited = [current]
        
        while stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = stack.pop()
            if current == end:
                while current in came_from:
                    self.reconstruct_path(came_from, end)
                    break
                break
        
            for neighbors in self.get_neighbors(self.grid, *current):
                if neighbors not in visited and self.grid[neighbors[0]][neighbors[1]] == 1:
                    visited.append(neighbors)
                    came_from[neighbors] = current
                    stack.append(neighbors)
            
            self.draw(current)
            CLOCK.tick(FPS)   
            
    def bfs(self):
        current = (0, 0)
        end = (self.cols - 2, self.rows - 2)
        
        queue = [current]
        came_from = {}
        visited = [current]
        
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = queue.pop(0)            
            if current == end:
                while current in came_from:
                    self.reconstruct_path(came_from, end)
                    break
                break
        
            
            for neighbors in self.get_neighbors(self.grid, *current):
                if neighbors not in visited and self.grid[neighbors[0]][neighbors[1]] == 1:
                    visited.append(neighbors)
                    came_from[neighbors] = current
                    queue.append(neighbors)
                    
            self.draw(current)
            CLOCK.tick(FPS)

    def dijkstra(self):
        current = (0, 0)
        end = (self.cols - 2, self.rows - 2)
        queue = []
        came_from = {}
        # Store the distance from the start point to each cell.
        distance = {row: {col: float('inf') for col in range(self.cols)} for row in range(self.rows)}
        distance[current[0]][current[1]] = 0
        heapq.heappush(queue, (0, current))

        visited = [current]
        
        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Pop the cell with the smallest distance from the start point from the priority queue.
            current = heapq.heappop(queue)[1]
            visited.remove(current)
            if current == end:
                while current in came_from:
                    self.reconstruct_path(came_from, end)
                    break
                break
            
            for neighbor in self.get_neighbors(self.grid, *current):
                if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] == 1:
                    # Calculate the distance from the start point to the neighbor through the current cell.
                    updated_distance = distance[current[0]][current[1]] + 1
                    # If a shorter path to the neighbor has been found, update the parent cell and the distance in the dictionary.
                    if updated_distance < distance[neighbor[0]][neighbor[1]]:
                        came_from[neighbor] = current
                        distance[neighbor[0]][neighbor[1]] = updated_distance
                        if neighbor not in queue:
                            # Add the neighbor to the priority queue with its updated distance as the priority key.
                            heapq.heappush(queue, (distance[neighbor[0]][neighbor[1]], neighbor))
                            visited.append(neighbor)
                            
            self.draw(current)
            CLOCK.tick(FPS)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self):
        current = (0, 0)
        end = self.cols - 2, self.rows - 2
        open_set = []
        heapq.heappush(open_set, (0, current))
        came_from = {}
        
        # Store the cost from the start point ot each cell.
        g_score = {row: {col: float('inf') for col in range(self.cols)} for row in range(self.rows)}
        g_score[current[0]][current[1]] = 0
        # Store the estimated total cost from each cell to the end point.
        f_score = {row: {col: float('inf') for col in range(self.cols)} for row in range(self.rows)}
        f_score[current[0]][current[1]] = self.heuristic(current, end)
        
        visited = [current]
        
        while open_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current = heapq.heappop(open_set)[1]
            visited.remove(current)
            if current == end:
                while current in came_from:
                    self.reconstruct_path(came_from, end)
                    break
                break
            
            for neighbor in self.get_neighbors(self.grid, *current):
                if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] == 1:
                    # Calculate the cost from the neighbor through the current cell.
                    updated_g_score = g_score[current[0]][current[1]] + 1
                    if updated_g_score < g_score[neighbor[0]][neighbor[1]]:
                        came_from[neighbor] = current
                        # Update the cost from the start point to the neighbor.
                        g_score[neighbor[0]][neighbor[1]] = updated_g_score
                        # Update the estimated total cost from the neighbor to the end point.
                        f_score[neighbor[0]][neighbor[1]] = updated_g_score + self.heuristic(neighbor, end)
                        if neighbor not in open_set:
                            heapq.heappush(open_set, (f_score[neighbor[0]][neighbor[1]], neighbor))
                            visited.append(neighbor)
                               
            self.draw(current)
            CLOCK.tick(FPS)