import argparse
import pandas as pd
import re
import time
from param import *
from generate import Maze
from pathfinding import Pathfinder

def round_even(n):
    n = int(n)
    return n if n % 2 == 0 else n - 1

def handle_generation(args, maze):
    gen_algo = None
    
    if args.generate:
        if args.generate[0] == 'dfs':
            maze.dfs()
            gen_algo = 'dfs'
        elif args.generate[0] == 'bfs':
            maze.bfs()
            gen_algo = 'bfs'
        elif args.generate[0] == 'kruskal':
            maze.kruskal()
            gen_algo = 'kruskal'
        elif args.generate[0] == 'prim':
            maze.prim()
            gen_algo = 'prim'
        else:
            print(f'Invalid generation algorithm: {args.generate[0]}')
            return None
        
        # Save generated maze as a csv.
        size = round_even(args.generate[1])
        df = pd.DataFrame(maze.grid)
        df.to_csv(f'Maze/{size}-{gen_algo}.csv', index=False)
    
    return gen_algo

def handle_pathfinding(args, maze, gen_algo, size):
    path_algo = None
    
    if args.pathfinder:
        pf = Pathfinder(maze.grid)
        start = time.time()
        if args.pathfinder[0] == 'dfs':
            pf.dfs()
            path_algo = 'dfs'
        elif args.pathfinder[0] == 'bfs':
            pf.bfs()
            path_algo = 'bfs'
        elif args.pathfinder[0] == 'dijkstra':
            pf.dijkstra()
            path_algo = 'dijkstra'
        elif args.pathfinder[0] == 'astar':
            pf.astar()
            path_algo = 'astar'
        else:
            print(f'Invalid pathfinding algorithm: {args.pathfinder[0]}')
            return
            
        print(f'Time to solve using {path_algo}: {(time.time() - start):.4f} seconds')

        # Save the pathfinding as an upscaled (10x) image.
        picture = pygame.transform.scale(SCREEN, (maze.cols * 10, maze.rows * 10))
        pygame.image.save(picture, f'Image/Pathfinding/{size}-{gen_algo}-{path_algo}.png')

def main():
    parser = argparse.ArgumentParser(
        prog='pymaze-cli',
        description='Generate and solve mazes using various algorithms',
        add_help=True
    )
    
    parser.add_argument('-g', '--generate', nargs=2, metavar=('[algorithm]', '[size]'),
                        type=str, help='generate a maze using the specified algorithm and size')
    
    parser.add_argument('-p', '--pathfinder', nargs=1, metavar='[algorithm]', type=str,
                        help='solve a maze using the specified algorithm')
    
    parser.add_argument('-l', '--load', nargs='+', metavar='[file]', type=argparse.FileType('r'),
                        help='load a maze from the specified file')
    
    args = parser.parse_args()
        
    pygame.init()
    pygame.display.set_caption('pymaze-cli')
    
    gen_algo = None
    size = None
    running = True
    unsolved = True
    
    # Check if a maze file a provided for loading.
    if args.load:
        grid = pd.read_csv(args.load[0], delimiter=',').values.tolist()
        size = len(grid)
        maze = Maze(grid)
        gen_algo = re.search('[\\w]+?(?=\\.)', args.load[0].name).group()
    # Otherwise, generate a new maze based on provided arguments.
    else:
        size = round_even(args.generate[1]) if args.generate else 0
        grid = [[0 for x in range(size)] for y in range(size)]
        maze = Maze(grid)
        gen_algo = handle_generation(args, maze)
        if not gen_algo:
            return
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if unsolved:
                maze.draw()
                picture = pygame.transform.scale(SCREEN, (maze.cols * 10, maze.rows * 10))
                pygame.image.save(picture, f'Image/Generation/{size}-{gen_algo}.png')
                handle_pathfinding(args, maze, gen_algo, size)
                unsolved = False
            
            CLOCK.tick(FPS)
            
    pygame.quit()
    
if __name__ == "__main__":
    main()