import queue

G = {0: [1, 2, 3, 4, 5, 6, 7], 1: [4, 6], 2: [1, 3, 4, 5, 6], 3: [1, 4, 6, 7], 5: [1, 3, 4, 6], 6: [4], 7: [1, 2, 4, 6]}

visited = []
queue = []

def bfs(visited, g, node):
    visited.append(node)
    queue.append(node)
    

print(level) 