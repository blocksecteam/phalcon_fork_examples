import subprocess
import re,os,sys,json
from pathlib2 import Path
import hashlib

DEPLOYED_ADDRESSES_FILE_POSTFIX = 'addresses.json'
WETH_ADDRESS = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

class ShellInteractor:
    def __init__(self):
        pass

    def execute(self, command):
        print ('\t-->' + command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        
        return process.returncode, output.decode('utf-8'), error.decode('utf-8')

    def search_output(self, regex, command_output):
        matches = re.findall(regex, command_output)
        return matches

    def check_tool_installed(self, tool):
        ret, output, error = self.execute(f'which {tool}')
        if output:
            return True
        else:
            return False

shell = ShellInteractor()
ENVIRON = {}


############################## check ###################################

def check_envir():
    print ('[*] Checking environ ...', end=' ')
    ENVIRON['PRIVATE_KEY'] = os.environ.get('PRIVATE_KEY')
    ENVIRON['PHALCON_API_ACCESS_KEY'] = os.environ.get('PHALCON_API_ACCESS_KEY')
    ENVIRON['PHALCON_RPC'] = os.environ.get('PHALCON_RPC')

    if ENVIRON['PRIVATE_KEY']  is None:
        print ('\n[x] Please set up environ [PRIVATE_KEY]')
        sys.exit(-1)
    
    if ENVIRON['PHALCON_API_ACCESS_KEY'] is None:
        print ('\n[x] Please set up environ [PHALCON_API_ACCESS_KEY]')
        sys.exit(-1)
    
    if ENVIRON['PHALCON_RPC']  is None:
        print ('\n[x] Please set up environ [PHALCON_RPC]')
        sys.exit(-1)
    
    if ENVIRON['PHALCON_RPC'][-1] == '/':
        ENVIRON['PHALCON_RPC'] = ENVIRON['PHALCON_RPC'][:-1]
    
    rpc_id = ENVIRON['PHALCON_RPC'].split('/')[-1]
    ENVIRON['VERIFIER_URL'] = 'https://api.phalcon.xyz/api/' + rpc_id
    ENVIRON['DEPLOYED_ADDRESSES_FILE'] = hashlib.md5(rpc_id.encode('utf-8')).hexdigest()  + '.' + DEPLOYED_ADDRESSES_FILE_POSTFIX


    print ('[Pass]')
    

def check_foundry():
    print ('[*] Checking foundry installation ...')
    if shell.check_tool_installed('forge'):
        return True
    else:
        print ('[x] Please install foundry first')
        sys.exit(-1)

############################### utility #########################
def get_address():
    print ('[*] Getting deployer address ...')
    cmd = 'cast wallet address --private-key ' + ENVIRON['PRIVATE_KEY']
    ret, output, error = shell.execute(cmd)

    if (ret == 0):
        return (output.strip())
    else:
        print ('[x] ' + error)
        sys.exit(-1)


def get_balance(address):
    cmd = 'cast balance --rpc-url ' + ENVIRON['PHALCON_RPC'] + '  ' + address
    ret, output, error = shell.execute(cmd)
    if (ret != 0):
        sys.exit(-1)
    
    balance = int(output.strip())

    return balance

def become_rich(address):
    RICH_MAN = '0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8'
    balance = get_balance(address)

    if (balance == -1):
        sys.exit(-1)
    
    cmd = 'cast send --unlocked --value 200ether ' + ' --rpc-url ' + ENVIRON['PHALCON_RPC'] + ' -f ' + (RICH_MAN) + ' ' + address 
    ret, output, error = shell.execute(cmd)
    if (ret != 0):
        print ('[x] ' + error)
        sys.exit(-1)


########################## compile ###############################
def compile_source_code():
    print ('[*] Building smart contracts ...')
    cmd = 'forge build'
    ret, output, error = shell.execute(cmd)

    if (ret != 0):
        print ('[x] ' + error)
        sys.exit(-1)

######################### deploy ###################################
# def get_deployed_code(contract_file, contract_name):
#     path = 'out/' + contract_file + '/' + contract_name + '.json'
#     if os.path.exists(path):
#         with open(path, 'r') as f:
#             data = json.load(f)
#             return (data['deployedBytecode']['object'])
#     return None

def get_deployed_address(contract_name):
    with open(ENVIRON['DEPLOYED_ADDRESSES_FILE'], 'r') as f:
        data = json.load(f)
    
        if contract_name in data.keys():
            return data[contract_name]
        else:
            return None

def set_deployed_address(contract_name, address):
    with open(ENVIRON['DEPLOYED_ADDRESSES_FILE'], 'r') as f:
        data = json.load(f)
    
    data[contract_name] = address

    with open(ENVIRON['DEPLOYED_ADDRESSES_FILE'], 'w') as f:
        json.dump(data, f, indent=4)

def check_deployed(contract_name):
    contract_address = get_deployed_address(contract_name)
    if contract_address is None:
        return None
    return contract_address


def __parse_deploy_output(output):
    for o in output.split('\n'):
        if o.startswith('Deployed to'):
            contract_address = o.split(':')[-1].strip()
            return contract_address
    return None


def deploy_UniswapV2Factory(deployer_address, verify = False):
    UniswapV2Factory_address = check_deployed('UniswapV2Factory')
    if (UniswapV2Factory_address is not None):
        print ('[*] UniswapV2Factory is already deployed to ' + UniswapV2Factory_address)
        return UniswapV2Factory_address

    print ('[*] Deploying UniswapV2Factory ...')
    cmd = 'forge create  --rpc-url ' + ENVIRON['PHALCON_RPC'] + ' --private-key ' + ENVIRON['PRIVATE_KEY']  + ' contracts/v2-core/contracts/UniswapV2Factory.sol:UniswapV2Factory' + '     --constructor-args  ' + deployer_address + '  '

    if (verify):
        cmd += ' --verify  --verifier-url ' + ENVIRON['VERIFIER_URL'] + ' --etherscan-api-key ' + ENVIRON['PHALCON_API_ACCESS_KEY']
    ret, output, error = shell.execute(cmd)

    if (ret != 0):
        print ('[x] ' + error)
        sys.exit(-1)

    address = __parse_deploy_output(output.strip())
    print ('[*] UniswapV2Factory is deployed to ' + address)
    set_deployed_address('UniswapV2Factory', address)
    return address


def deploy_UniswapV2Router02(factory_address, verify = False):
    UniswapV2Router02_address = check_deployed('UniswapV2Router02')
    if (UniswapV2Router02_address is not None):
        print ('[*] UniswapV2Router02 is already deployed to ' + UniswapV2Router02_address)
        return UniswapV2Router02_address

    print ('[*] Deploying UniswapV2Router02 ...')
    cmd = 'forge create  --rpc-url ' + ENVIRON['PHALCON_RPC'] + ' --private-key ' + ENVIRON['PRIVATE_KEY']  + ' contracts/v2-periphery/contracts/UniswapV2Router02.sol:UniswapV2Router02' + '     --constructor-args  ' + factory_address + ' '+ WETH_ADDRESS + ' '

    if (verify):
        cmd += ' --verify --verifier-url ' + ENVIRON['VERIFIER_URL'] + ' --etherscan-api-key ' + ENVIRON['PHALCON_API_ACCESS_KEY']
    ret, output, error = shell.execute(cmd)

    if (ret != 0):
        print ('[x] ' + error)
        sys.exit(-1)

    address = __parse_deploy_output(output.strip())
    print ('[*] UniswapV2Router02 is deployed to ' + address)
    set_deployed_address('UniswapV2Router02', address)
    return address


def get_init_code_hash(UniswapV2Factory_address):
    cmd = 'cast call --rpc-url '  + ENVIRON['PHALCON_RPC'] +  ' ' + UniswapV2Factory_address + '  "INIT_CODE_HASH()"'

    ret, output, error = shell.execute(cmd)

    if (ret != 0):
        print ('[x] ' + error)
        sys.exit(-1)

    return output.strip()


def update_init_code_hash_in_periphery(init_code_hash):
    path = 'contracts/v2-periphery/contracts/libraries/UniswapV2Library.sol'
    file = Path(path)

    data = file.read_text()

    if (init_code_hash[0] == '0' and init_code_hash[1] == 'x'):
        init_code_hash = init_code_hash[2:]

    data = data.replace('96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f', init_code_hash)

    file.write_text(data)


if __name__ == "__main__":

    check_foundry()

    check_envir()

    # create the file
    if (not os.path.exists(ENVIRON['DEPLOYED_ADDRESSES_FILE'])):
        with open(ENVIRON['DEPLOYED_ADDRESSES_FILE'], 'w+') as f:
            json.dump({}, f, indent=4)
    
    deployer_address = get_address()
    print ('[*] Using deployer address ' + deployer_address)

    balance = get_balance(deployer_address)
    print ('[*] Balance of deployer is ' + str(balance/(1e18) ) + ' Ether')

    if (balance < 1e18):
        print ('[*] Deployer is not rich, get some Ether')
        become_rich(deployer_address)

    # compile the contracts
    compile_source_code()

    # deploy UniswapV2Factory
    UniswapV2Factory_address = deploy_UniswapV2Factory(deployer_address, True)
    
    # get the INIT_CODE_HASH
    init_code_hash = get_init_code_hash(UniswapV2Factory_address)

    print ('[*] INIT_CODE_HASH is ' + init_code_hash)

    # update INIT_CODE_HASH IN libraries/UniswapV2Library.sol
    update_init_code_hash_in_periphery(init_code_hash)

    # build again
    compile_source_code()

    # deploy UniswapV2Router02
    UniswapV2Router02_address = deploy_UniswapV2Router02(UniswapV2Factory_address, True)

    # create a pool of WETH/USDC