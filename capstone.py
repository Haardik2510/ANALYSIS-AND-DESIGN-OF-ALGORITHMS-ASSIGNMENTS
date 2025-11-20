# capstone.py
# Full Capstone Assignment Implementation

import itertools, heapq
from functools import lru_cache

locations=['Warehouse','C1','C2','C3']
distance_matrix=[[0,4,8,6],[4,0,5,7],[8,5,0,3],[6,7,3,0]]
parcels={'C1':{'value':50,'time':(9,12),'weight':10},
         'C2':{'value':60,'time':(10,13),'weight':20},
         'C3':{'value':40,'time':(11,14),'weight':15}}
vehicle_capacity=30

def delivery_cost_recursive(idx=0,visited=None):
    if visited is None: visited={0}
    if len(visited)==len(distance_matrix): return distance_matrix[idx][0]
    best=float('inf')
    for nxt in range(len(distance_matrix)):
        if nxt not in visited:
            c=distance_matrix[idx][nxt]+delivery_cost_recursive(nxt,visited|{nxt})
            best=min(best,c)
    return best

def greedy_parcel_selection(parcels,cap):
    items=[(k,v['value'],v['weight'],v['value']/v['weight']) for k,v in parcels.items()]
    items.sort(key=lambda x:x[3],reverse=True)
    sel=[];tw=0;tv=0
    for n,val,w,ratio in items:
        if tw+w<=cap:
            sel.append(n);tw+=w;tv+=val
    return sel,tv,tw

def knapsack_dp(parcels,cap):
    items=list(parcels.items());n=len(items)
    dp=[[0]*(cap+1) for _ in range(n+1)]
    for i in range(1,n+1):
        name,inf=items[i-1];w=inf['weight'];val=inf['value']
        for W in range(cap+1):
            dp[i][W]=dp[i-1][W]
            if w<=W: dp[i][W]=max(dp[i][W],dp[i-1][W-w]+val)
    res=[];W=cap
    for i in range(n,0,-1):
        if dp[i][W]!=dp[i-1][W]:
            res.append(items[i-1][0]);W-=items[i-1][1]['weight']
    return list(reversed(res)),dp[n][cap]

def check_delivery_with_time_windows(route,start=9):
    t=start;delivered=[]
    for i in range(1,len(route)):
        prev,cur=route[i-1],route[i];t+=distance_matrix[prev][cur]
        name=locations[cur]
        if name=='Warehouse':continue
        tw=parcels[name]['time']
        if t<tw[0]:t=tw[0]
        if t>tw[1]:return False,t,delivered
        delivered.append((name,t))
    return True,t,delivered

def find_routes_respecting_time_windows():
    idx=list(range(1,len(locations)));best=None;bc=float('inf')
    for p in itertools.permutations(idx):
        r=[0]+list(p)+[0]
        cost=sum(distance_matrix[r[i]][r[i+1]] for i in range(len(r)-1))
        ok,_,_=check_delivery_with_time_windows(r)
        if ok and cost<bc:best=r;bc=cost
    return best,bc

def dijkstra(start=0):
    n=len(distance_matrix);dist=[float('inf')]*n;dist[start]=0
    pq=[(0,start)];vis=[False]*n
    while pq:
        d,u=heapq.heappop(pq)
        if vis[u]:continue
        vis[u]=True
        for v in range(n):
            w=distance_matrix[u][v]
            if w>0 and dist[v]>d+w:
                dist[v]=d+w;heapq.heappush(pq,(dist[v],v))
    return dist

def prim_mst():
    n=len(distance_matrix);sel=[False]*n;key=[10**9]*n;par=[-1]*n;key[0]=0
    for _ in range(n):
        u=min((i for i in range(n) if not sel[i]),key=lambda x:key[x])
        sel[u]=True
        for v in range(n):
            w=distance_matrix[u][v]
            if w>0 and not sel[v] and w<key[v]:key[v]=w;par[v]=u
    edges=[];t=0
    for v in range(1,n):edges.append((par[v],v,distance_matrix[par[v]][v]));t+=distance_matrix[par[v]][v]
    return edges,t

def tsp_bruteforce():
    n=len(locations);idx=list(range(1,n))
    best=None;bc=float('inf')
    for p in itertools.permutations(idx):
        r=[0]+list(p)+[0]
        cost=sum(distance_matrix[r[i]][r[i+1]] for i in range(len(r)-1))
        if cost<bc:bc=cost;best=r
    return best,bc
