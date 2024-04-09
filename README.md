# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> tokenB, balance: 5 <br>
tokenA, balance: 5.655321988655322 <br>
tokenD, balance: 2.4587813170979333 <br>
tokenC, balance: 5.0889272933015155 <br>
tokenB, balance: 20.129888944077443

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Slippage refers to the difference between the expected price of a trade and the actual executed price. It occurs because the price of an asset in an AMM is determined by the ratio of the asset balances in the liquidity pool. When a trade is executed, especially for a large amount, it can cause the price to move due to the imbalance in the pool. Slippage can result in traders receiving a less favorable price than they anticipated.
 ```=solidity
function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline
) external virtual override ensure(deadline) returns (uint[] memory amounts) {
    amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
    // this assertion helps identifying slippage and prevent the execution of trade
    require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
    TransferHelper.safeTransferFrom(
        path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]
    );
    _swap(amounts, path, to);
}
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> MINIMUM_LIQUIDITY (usually set to 1000, cuz this won't hurt the first provider too much) is used to prevent attackers from trying to make a large discrepancy in quantities between a trading pair.
> To be more precise, an initial liquidity provider can easily initialize a new liquidity pair (with small amount). By accumulating trading fees or through “donations” to the liquidity pool, the value of the minimum quantity of liquidity pool shares can worth so much that it becomes infeasible for small liquidity providers to provide any liquidity. In Uniswap V2, to mitigate this problem, the MINIMUN_LIQUIDITY amount is first transfered to address(0) which can never be burned. To increase the value of pool shares, the attacker then has to donate 1000x more of the amount to perform the above attack. To sum up, this MINIMUM_LIQUIDITY serves as a protection against this issue.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?
```=solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```
> Intuitively, the liquidity (LP-tokens) should 1. be propotional to the deposited amount (ex. amount0, amount1) 2. be propotional to the total amount of LP-tokens. Therefore, the above formula is created. Additionally, the min() is yet another trick to punish those who deposit unbalanced liquidity into the pool (since the provider will only get the smaller one). It would be more benefitial for Uniswap to issue the smaller number of LP-tokens.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap? <br>
> The sandwich attack works as follows: <br>
> 1. Monitoring Transactions: The attacker monitors the pending transactions on the blockchain, looking for transactions that involve significant trades or movements of assets on the DEX. <br>
> 2. Front-Running: The attacker quickly places their own transaction in front of the target transaction (submitted by user). This transaction usually involves buying or selling the same asset that the target transaction is attempting to trade. <br>
> 3. Benefit: The attackers swap is completed at a low price, whereas, the user’s transaction is completed at a high price, which means they receive less tokens than expected. <br>

> To sum up, the attacker profits from the increase in price from the previous transactions. This results in a gain for the attacker, and a loss for the user.


### Bonus
The Arbitrage.py already outputs the most profitable path among all possible swap paths (the path in problem 1). Therefore, I am not going to provide another python script. (I assume that one cannot swap to the same token twice except tokenB)
