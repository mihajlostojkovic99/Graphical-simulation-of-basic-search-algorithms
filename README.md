# Graphical-simulation-of-basic-search-algorithms

This is a University project for Intelligent Systems class showcasing the use of search algorithms to find a path on a map from a defined start to finish. The program is written in Python using PyCharm IDE and requires pygame package (v2.0.2). 

The map has tiles with a unique cost (road, grass, mud, dune, water and stone). Maps can be configured in txt files in folder maps. first a starting poind is defined and then the finish point as x and y coorinates. Afterwards, the map tile configuration is defined as a matrix of first letters of tile type. Map example:
```
1,1
2,3
wwgg
wrgg
grrr
gggg
```

The program has 4 players utilising different search strategies. Playes can move in 4 directions.
  - **ExampleAgent** - An example agent provided to showcase a basic version of a player.
  - **Aki** - Aki uses a depth first search strategy (DFS) and prefers tiles with the least cost and in case some tiles are the same, he prefers them according to sides of the                   world (North, East, South, West).
  - **Jocke** - Jocke uses a breath first search strategy (BFS) and prefers tiles which neigbors have the least cost and in case of more of such tiles he prefers them according to                 sides of the world (North, East, South, West).
  - **Draza** - Draza uses branch and bound strategy and in case of partial paths with same cost, he chooses the one with least nodes in the path or an arbitrary one in case of                    multiple same partial paths.
  - **Bole** - Bole uses A* search strategy with Manhattan distance heuristics with coefficient set to the lowest cost between adjacent squares on a given map.
  
The algorithms are defined in `get_agent_path` function (which returns a final path as list of `Tile` objects) in expanded `Agent` classes (in sprites.py file). The program is started from the terminal by specifying the following command `.\main.py map agent`, for example `.\main.py maps\map4.txt Bole`.
