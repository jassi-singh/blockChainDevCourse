from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorge.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode
bytecode = compiled_sol['contracts']['SimpleStorge.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorge.sol']['SimpleStorage']['abi']

# connecting to the blockChain
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_NODE")))
chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADRESS")
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build  a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# 2. Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

# 3. send the signd txn
print("Deploying ..........")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(txn_hash)
print("DEPLOYED")

simple_storage = w3.eth.contract(address=tx_reciept.contractAddress,abi=abi)

print(simple_storage.functions.getFavNum().call())

# Creating and sending a transaction

store_transaction = simple_storage.functions.setFavNum(45).buildTransaction(
    {"chainId":chain_id,"from":my_address,"nonce":nonce+1}
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction,private_key=private_key)
print("Updating ..........")
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated")

print(simple_storage.functions.getFavNum().call())

