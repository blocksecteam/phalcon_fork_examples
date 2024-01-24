import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "@openzeppelin/hardhat-upgrades";
import { vars } from "hardhat/config";

const config: HardhatUserConfig = {
  defaultNetwork: "phalcon",
  networks: {
    phalcon: {
      url: vars.get("PHALCON_RPC", ""), 
      chainId: Number(vars.get("PHALCON_CHAIN_ID", "1")),
      //testing account -- DONOT USE IN PRODUCTION. 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC
      accounts: ["0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"]
    }
  },
  etherscan: {
    apiKey: {
      phalcon: vars.get("PHALCON_API_KEY", ""),
    },
    customChains: [
      {
        network: "phalcon",
        chainId: 1,
        urls: {
          apiURL: vars.get("PHALCON_API_URL", ""),
          browserURL: vars.get("PHALCON_BROWSER_URL", ""),
        }
      }
    ]
  },
  solidity: {
    compilers: [{ version: "0.8.18" }],
    overrides: {
      // indicate the exact settings used by OZ for compiling the contracts you're using
      "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol": {
        version: "0.8.9",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
      "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol":
        {
          version: "0.8.9",
          settings: {
            optimizer: {
              enabled: true,
              runs: 200,
            },
          },
        },

      "@openzeppelin/contracts/proxy/beacon/UpgradeableBeacon.sol": {
        version: "0.8.9",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
      "@openzeppelin/contracts/proxy/beacon/BeaconProxy.sol": {
        version: "0.8.9",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    },
  },
  mocha: {
    timeout: 4 * 60 * 1000,
  },
};

export default config;
