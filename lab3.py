
# lab3.py – Lab Assignment 3
import heapq
from collections import deque

def suggest_friends(adj, user):
    visited=set([user]); q=deque([user]); level={user:0}
    while q:
        u=q.popleft()
        for v in adj.get(u,[]):
            if v not in visited:
                visited.add(v); level[v]=level[u]+1; q.append(v)
    return {n for n,d in level.items() if d==2 and n not in adj.get(user,[])}

def bellman_ford(vertices, edges, source):
    dist={v:float('inf') for v in vertices}; dist[source]=0
    for _ in range(len(vertices)-1):
        for (u,v,w) in edges:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
    for u,v,w in edges:
        if dist[u]+w<dist[v]: return "NEGATIVE CYCLE"
    return dist

def dijkstra_graph(adj, source):
    dist={v:float('inf') for v in adj}; dist[source]=0
    pq=[(0,source)]; visited=set()
    while pq:
        d,u=heapq.heappop(pq)
        if u in visited: continue
        visited.add(u)
        for v,w in adj[u]:
            if dist[v]>d+w:
                dist[v]=d+w; heapq.heappush(pq,(dist[v],v))
    return dist

def prim_heap(adj, start):
    visited=set(); pq=[(0,start,None)]; edges=[]; total=0
    while pq and len(visited)<len(adj):
        w,u,p=heapq.heappop(pq)
        if u in visited: continue
        visited.add(u)
        if p is not None:
            edges.append((p,u,w)); total+=w
        for v,wt in adj[u]:
            if v not in visited: heapq.heappush(pq,(wt,v,u))
    return edges,total
