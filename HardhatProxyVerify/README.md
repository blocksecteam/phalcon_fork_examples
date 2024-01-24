# Deploy and verify proxy contracts in Phalcon Fork

Part of the code is from this repo: https://github.com/fjun99/proxy-contract-example

Install the required libraries.
```
# npm install  
```

Create a new Fork in [Phalcon](https://phalcon.blocksec.com) and then setup the necessary IDs.


```
npx hardhat vars set PHALCON_RPC [RPC_URL]
npx hardhat vars set PHALCON_API_KEY [API KEY]
npx hardhat vars set PHALCON_API_URL https://api.phalcon.blocksec.com/api/[RPC_ID]
npx hardhat vars set PHALCON_BROWSER_URL https://phalcon.blocksec.com/fork/scan/[FORK_ID]
```

## How to deploy and verify proxy contracts (Transparent Proxy)

Use the following command to deploy and verify the contracts. Note that, we use [the transparent proxy type](https://docs.openzeppelin.com/upgrades-plugins/1.x/api-hardhat-upgrades) in the example.

```
# npx hardhat  --network phalcon run scripts/1.deploy_box.ts
Deploying Box...
0x9ae40d21177F53928da4dFF6389dEA33DF2E4558  box(proxy) address
0x121525a50836042846362fAAB126168b998D1cF2  getImplementationAddress
0x24b6a2190270Ee90116868e648A527E9FEd2ef70  getAdminAddress
# npx hardhat --network phalcon verify 0x9ae40d21177F53928da4dFF6389dEA33DF2E4558
Verifying implementation: 0x121525a50836042846362fAAB126168b998D1cF2
Nothing to compile
No need to generate any newer typings.
Successfully submitted source code for contract
contracts/Box.sol:Box at 0x121525a50836042846362fAAB126168b998D1cF2
for verification on the block explorer. Waiting for verification result...

Successfully verified contract Box on Etherscan.
https://phalcon.blocksec.com/fork/scan/fork_3e3f03e2a9404d36bf63ffdf8d4da7e7/address/0x121525a50836042846362fAAB126168b998D1cF2#code
Verifying proxy: 0x9ae40d21177F53928da4dFF6389dEA33DF2E4558
Successfully verified contract TransparentUpgradeableProxy at 0x9ae40d21177F53928da4dFF6389dEA33DF2E4558.
Linking proxy 0x9ae40d21177F53928da4dFF6389dEA33DF2E4558 with implementation
Successfully linked proxy to implementation.
Verifying proxy admin: 0x24b6a2190270Ee90116868e648A527E9FEd2ef70
Successfully verified contract ProxyAdmin at 0x24b6a2190270Ee90116868e648A527E9FEd2ef70.

Proxy fully verified.
```

Then we can upgrade and verify the new implementation contract.

```
# npx hardhat --network phalcon run scripts/2.upgradeV2.ts
0x9ae40d21177f53928da4dff6389dea33df2e4558  original Box(proxy) address
upgrade to BoxV2...
0x9ae40d21177f53928da4dff6389dea33df2e4558  BoxV2 address(should be the same)
0xBE95c3f554e9Fc85ec51bE69a3D807A0D55BCF2C  getImplementationAddress
0x24b6a2190270Ee90116868e648A527E9FEd2ef70  getAdminAddress

# npx hardhat --network phalcon verify 0xbe95c3f554e9fc85ec51be69a3d807a0d55bcf2c
Nothing to compile
No need to generate any newer typings.
Successfully submitted source code for contract
contracts/BoxV2.sol:BoxV2 at 0xbe95c3f554e9fc85ec51be69a3d807a0d55bcf2c
for verification on the block explorer. Waiting for verification result...

Successfully verified contract BoxV2 on Etherscan.
https://phalcon.blocksec.com/fork/scan/fork_3e3f03e2a9404d36bf63ffdf8d4da7e7/address/0xbe95c3f554e9fc85ec51be69a3d807a0d55bcf2c#code
```




The deployed contract can be viewed here: [https://phalcon.blocksec.com/fork/scan/fork_3e3f03e2a9404d36bf63ffdf8d4da7e7](https://phalcon.blocksec.com/fork/scan/fork_3e3f03e2a9404d36bf63ffdf8d4da7e7)

