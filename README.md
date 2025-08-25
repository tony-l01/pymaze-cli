# pymaze-cli
Generate and solve mazes using various algorithms

## Getting Started

### Installation

1. Clone the repo
   ```
   git clone https://github.com/tony-l01/pymaze-cli
   ```

2. Install the requirements
   ```
   pip install -r requirements.txt
   ```
## Running the code
There are three flags to run the program: `-g`, `-l`, `-p`. 

For more help
```
python main.py -h
```

### Generating a maze

Enter the command in the console to generate a new maze
```
python main.py -g dfs
```

### Loading a maze
Enter the command in the console to load a saved maze
```
python main.py -l Maze/YOUR_MAZE.csv
```

### Solving a maze
Enter the command in the console to solve a new maze
```
python main.py -g dfs -p bfs
```
For loaded maze
```
python main.py -l Maze/YOUR_MAZE.csv -p bfs
```

## List of algorithms
### Generation
```
dfs, bfs, kruskal, prim
```

### Pathfinding
```
dfs, bfs, dijkstra, astar
```
