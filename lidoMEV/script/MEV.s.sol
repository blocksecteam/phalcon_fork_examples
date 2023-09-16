// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import {MEVExample} from "../src/MEV.sol";

contract MEVScript is Script {
    MEVExample public mevExample;

    function setUp() public {

    }

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        mevExample = new MEVExample();
        mevExample.trigger();
        
        vm.stopBroadcast();
    }
}
