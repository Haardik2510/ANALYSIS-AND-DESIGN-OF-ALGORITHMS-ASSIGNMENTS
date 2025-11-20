
# lab2.py – Lab Assignment 2
import itertools

def schedule_ads(ads):
    ads_sorted = sorted(ads, key=lambda x: x[2], reverse=True)
    max_deadline = max(d for _,d,_ in ads)
    slots = [None] * (max_deadline+1)
    total_profit = 0
    scheduled = []
    for ad in ads_sorted:
        ad_id, dead, profit = ad
        for t in range(dead, 0, -1):
            if slots[t] is None:
                slots[t] = ad_id
                total_profit += profit
                scheduled.append((ad_id, t, profit))
                break
    return scheduled, total_profit

def knapsack(items, capacity):
    n = len(items)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        wt, val = items[i-1]
        for w in range(capacity+1):
            dp[i][w] = dp[i-1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-wt] + val)
    res = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            res.append(i-1)
            w -= items[i-1][0]
    res.reverse()
    return dp[n][capacity], res

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, r, c, val):
    if any(board[r][j] == val for j in range(9)): return False
    if any(board[i][c] == val for i in range(9)): return False
    br, bc = 3*(r//3), 3*(c//3)
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            if board[i][j] == val: return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    for val in range(1, 10):
        if is_valid(board, r, c, val):
            board[r][c] = val
            if solve_sudoku(board): return True
            board[r][c] = 0
    return False

def brute_force_password(target, charset):
    length = 1
    attempts = 0
    while True:
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            candidate = ''.join(combo)
            if candidate == target:
                return candidate, attempts
        length += 1
