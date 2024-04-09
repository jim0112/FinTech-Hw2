liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def getAmountout(liquid, deltaX):
    x, y = liquid
    return 997 * deltaX * y / (1000 * x + 997 * deltaX)

def validate_path(path, init_value):
    init_token = "tokenB"
    for p in path:
        init_value = getAmountout(liquidity[(init_token, p)], init_value)
        print(f"{p}, balance: {init_value}")
        init_token = p
    return init_value

nodes = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]
max_path = []
max_profit = 5

def print_ans(path, profit):
    ans = "path: TokenB"
    for p in path:
        ans += f"->{p}"
    ans += f", tokenB balance={profit}."
    print(ans)

def dfs(node, used, profit):
    if len(used) > 0 and used[-1] == "tokenB":
        global max_profit
        if profit > max_profit:
            global max_path
            max_path = used
            max_profit = profit
        return
    for next_node in nodes:
        if next_node not in used:
            new_profit = getAmountout(liquidity[node, next_node], profit) if not (node == next_node == "tokenB") else profit
            dfs(next_node, used + [next_node], new_profit)

if __name__ == '__main__':
    init_amount = 5
    newLiquidity = {}
    for (a, b), (x, y) in liquidity.items():
        newLiquidity[a, b] = (x, y)
        newLiquidity[b, a] = (y, x)
    liquidity = newLiquidity
    # print(liquidity)
    dfs("tokenB", [], init_amount)
    print_ans(max_path, max_profit)

    # sample_result = ["tokenA", "tokenD", "tokenC", "tokenB"]
    # print(validate_path(sample_result, 5))


