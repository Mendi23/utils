
## Graph search

### Topological sorting
Ordering of the vertices such that for every directed edge `uv` from vertex `u` to vertex `v`, `u` comes before `v` in the ordering. possible iff it's DAG 
Complexity: `O(|V|+|E|)`

### Dijkstra's algorithm
Finding the shortest paths between nodes in a graph. building the "shortest path" tree
Complexity: `O((|V|+|E|)log(|V|))` using queue, `O(|V^2|)` using array, `O(|E|+|V|log(|V|))` using Fibonacci heap

### Bellman–Ford algorithm
Finding the shortest path from a single node in a `weighted directed graph` without a negative-value cycle.
Complexity: `O(|V|*|E|)`
finding the shortest path with length `i` can be done in `O(|V|*i)`

### Johnson's algorithm
Find the shortest paths between all pairs of vertices in an edge-weighted directed graph without negative-weight cycles