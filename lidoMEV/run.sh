# To load the variables in the .env file
source .env

# forge test --contracts test/MEV.t.sol -vvv --rpc-url $PHALCON_FORK_RPC_URL

# To deploy and verify our contract
forge script script/MEV.s.sol:MEVScript --rpc-url $PHALCON_FORK_RPC_URL --broadcast --verify -vvvv