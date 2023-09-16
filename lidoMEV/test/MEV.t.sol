// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console2} from "forge-std/Test.sol";
import "forge-std/console.sol";
import {MEVExample} from "../src/MEV.sol";

contract MEVTest is Test {
    MEVExample public mevExample;

    function setUp() public {
        console.log("token0 is stETH token: [0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84]");
        console.log("token1 is WETH  token: [0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2]");
        mevExample = new MEVExample();
    }

    function testTrigger() public {
        mevExample.trigger();
    }
}
