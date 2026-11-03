import heapq

def dijkstra(graph, source):
    if source not in graph:
        raise ValueError("Source router not found in graph")

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(f"Unknown neighbor: {neighbor}")
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                raise ValueError(f"Invalid link cost: {weight}")
            if not 0 <= weight < float('inf'):
                raise ValueError(f"Invalid link cost: {weight}")
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    previous = {node: None for node in graph}
    priorityQueue = [(0, source)]
    while priorityQueue:
        currentDistance, currentNode = heapq.heappop(priorityQueue)

        if currentDistance > distances[currentNode]:
            continue

        for neighbor, weight in graph[currentNode].items():
            newDistance = currentDistance + weight

            if newDistance < distances[neighbor]:
                distances[neighbor] = newDistance
                previous[neighbor] = currentNode
                heapq.heappush(priorityQueue, (newDistance, neighbor))

    return distances, previous

def get_next_hops(previous, source):
    nextHops = {}

    for destination in previous:
        if destination == source:
            continue

        current = destination

        while previous[current] is not None and previous[current] != source:
            current = previous[current]

        if previous[current] == source:
            nextHops[destination] = current
        else:
            nextHops[destination] = None

    return nextHops

if __name__ == "__main__":
    graph = {
        "routerA": {"routerB": 2, "routerC": 5},
        "routerB": {"routerA": 2, "routerD": 1},
        "routerC": {"routerA": 5, "routerD": 2},
        "routerD": {"routerB": 1, "routerC": 2},
        "routerD": {"routerB": 1, "routerC": 2},
        "routerE": {}
    }

    distances, previous = dijkstra(graph, "routerA")

    print("Distances:", distances)
    print("Previous:", previous)
    nextHops = get_next_hops(previous, "routerA")
    print("Next hops:", nextHops)