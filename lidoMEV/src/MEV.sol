// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./Interface.sol";
// import "forge-std/console.sol";

// Be cautious!! This is an example contract. DO NOT use it in a production environment.

contract MEVExample {

    IUniswapV2Pair stETH_WETH_pair = IUniswapV2Pair(0x4028DAAC072e492d34a3Afdbef0ba7e35D8b55C4);

    address owner;

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function trigger() external onlyOwner {

        //query the balance and reserve of the pool
        address token0 = stETH_WETH_pair.token0();
        address token1 = stETH_WETH_pair.token1();

        (uint112 reserve0, uint112 reserve1, ) = stETH_WETH_pair.getReserves();

        uint256 balance0 = IERC20(token0).balanceOf(address(stETH_WETH_pair));
        uint256 balance1 = IERC20(token1).balanceOf(address(stETH_WETH_pair));

        // console.log("[stETH] reserve : balance", reserve0, balance0);
        // console.log("[WETH]  reserve : balance", reserve1, balance1);

        require (balance0 > reserve0, "Balance should be bigger than Reserve!");

        // calculate how many tokens can be swapped out 
        // this is the amount0In
        uint amount0In = balance0 - reserve0;

        uint amount1Out = balance1 - (uint(reserve0)*(reserve1)*(1000**2) / ((balance0 * 1000 - 3 * amount0In)))/1000;

        // console.log("[stETH] out ", amount1Out);

        // perform the swap
        stETH_WETH_pair.swap(0, amount1Out - 1, msg.sender, "");

    }
}
