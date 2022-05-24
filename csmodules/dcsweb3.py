#%%
import os
import requests
import json
from web3 import Web3
from web3.auto import w3
from decimal import *
from termcolor import colored as cl

def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)

def create_wallet(amount,export_path):
    try:
        for i in range(amount):
            account = w3.eth.account.create('KEYSMASH FDHGDFGFDFVSDFGHUTY 1999')
            append_new_line(export_path,account.address+'|'+account.privateKey.hex())
        print('Create wallet done!')
        return True
    except:
        return False

class ContractABI:
    def __init__(self,contract_address,network):
        self.contract_address = contract_address
        self.cur_dir = os.path.dirname(__file__)
        self.abi_folder = os.path.join(self.cur_dir,'abi_data')
        if not os.path.exists(self.abi_folder):
            os.makedirs(self.abi_folder)

        if network == 'polygon':
            self.path_abi = os.path.join(self.cur_dir,'abi_data\\polygon_'+self.contract_address+'.abi')  
            self.scan_network = 'https://api.polygonscan.com'
            self.scan_key = 'YBXYH8U4QE4CVFB6RHFEGASP5VWNS566YZ'
        elif network == 'bsc':
            self.path_abi = os.path.join(self.cur_dir,'abi_data\\bsc_'+self.contract_address+'.abi')
            self.scan_network = 'https://api.bscscan.com'
            self.scan_key = 'XBWYHWDK1WUN12MUJE78F2DIU89U9ZYDWR'
        else:
            return False

    def get(self):
        try:
            if os.path.exists(self.path_abi):
                # Get ABI from file
                f = open(self.path_abi)
                return json.load(f)
            else:
                try:
                    # Get ABI from scan network
                    res = requests.get(self.scan_network+'/api?module=contract&action=getabi&address='+self.contract_address+'&apikey='+self.scan_key)
                    if res.status_code == 200:
                        res_json = res.json()
                        abi = json.loads(res_json['result'])
                        # Write abi to file
                        f = open(self.path_abi, "a+")
                        f.write(json.dumps(abi))
                        f.close()
                        return abi
                except:
                    return False
        except:
            return False

class DCSCHAIN:
    def __init__(self,network,rpc = 'default'):
        self.cur_dir = os.path.dirname(__file__)
        self.contract_address = False
        self.network = network
        if network == 'bsc':
            self.chainId = 56
            if rpc == 'default':
                self.rpc = 'https://bsc-dataseed1.defibit.io'
            else:
                self.rpc = rpc
            self.scan_network = 'https://api.bscscan.com'
            self.scan_key = 'XBWYHWDK1WUN12MUJE78F2DIU89U9ZYDWR'
        elif network == 'polygon':
            self.chainId = 137
            if rpc == 'default':
                self.rpc = 'https://rpc-mainnet.maticvigil.com'
            else:
                self.rpc = rpc
            self.scan_network = 'https://api.polygonscan.com'
            self.scan_key = 'YBXYH8U4QE4CVFB6RHFEGASP5VWNS566YZ'
        else:
            print('This network is not supported')
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        if self.web3.isConnected() == False:
            print('ERROR: Can not connect to rpc network!')
 
    def set_contract(self,contract_address):
        self.contract_address = contract_address
    def get_token_balance(self,wallet_address):
        if self.contract_address == False:
            print('ERROR: You have to set token contract. ')
            return {'status':'error','message':'You have to set token contract. (Using function .set_contract() to set contract!)'}
        try:
            wallet_address = Web3.toChecksumAddress(wallet_address)
            ct_address = Web3.toChecksumAddress(self.contract_address)
            abi = ContractABI(self.contract_address,self.network).get()
            contract = self.web3.eth.contract(ct_address, abi=abi) 
            token_balance = contract.functions.balanceOf(wallet_address).call()
            return self.web3.fromWei(token_balance,'ether')
        except:
            res = requests.get(self.scan_network+'/api?module=account&action=tokenbalance&contractaddress='+self.contract_address+'&address='+wallet_address+'&tag=latest&apikey='+self.scan_key)
            if res.status_code == 200:
                res_json = res.json()
                token_balance = json.loads(res_json['result'])
                print('Balance from scan network: '+str(self.web3.fromWei(token_balance,'ether')))
                return self.web3.fromWei(token_balance,'ether')
            else:
                return False
    def get_native_balance(self,wallet_address):
        try:
            if self.web3.isConnected():
                balance = self.web3.eth.getBalance(wallet_address)
                return self.web3.fromWei(balance,'ether')
            else:
                return False
        except:
            return False
    def send_token(self,sender_wallet,receive_wallet,sender_wallet_key,value = -1,gwei = 5,gas = -1,timeout=20):
        if self.contract_address == False:
            print('ERROR: You have to set token contract. ')
            return {'status':'error','message':'You have to set token contract. (Using function .set_contract() to set contract!)'}
        balance_fee = self.get_native_balance(sender_wallet)
        print('..Native token: '+str(balance_fee))
        balance_token = self.get_token_balance(sender_wallet)
        if balance_fee > 0 and balance_token > 0:
            nonce = self.web3.eth.getTransactionCount(sender_wallet)
            sender_wallet = Web3.toChecksumAddress(sender_wallet)
            ct_address = Web3.toChecksumAddress(self.contract_address)
            abi = ContractABI(self.contract_address,self.network).get()
            contract = self.web3.eth.contract(ct_address, abi=abi) 
            if gas == -1:
                egas = contract.functions.transfer(receive_wallet,6).estimateGas({'from':sender_wallet})
                gas = int(egas*1.5)
            # print('gas: '+str(gas)) #show
            val = value if value != -1 else balance_token
            token_tx = contract.functions.transfer(receive_wallet, self.web3.toWei(val,'ether')).buildTransaction({
                'chainId':self.chainId,
                'gas': gas,
                'gasPrice': self.web3.toWei(gwei,'gwei'),
                'nonce':nonce
            })
            signed_tx = self.web3.eth.account.signTransaction(token_tx,sender_wallet_key)

            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print('Transaction pending hash:: '+str(tx_hash.hex()))
            check_transaction = self.web3.eth.waitForTransactionReceipt(tx_hash,timeout=timeout)
            if check_transaction.status ==1:
                return {'status':'success','message':'Transaction successfully','tx':tx_hash.hex()}
            else:
                return {'status':'error','message':'Transaction failed!','tx':tx_hash.hex()}
        else:
            if balance_fee <= 0:
                return {'status':'error','message':'Balance fee not enough'}
            elif balance_token <=0:
                return {'status':'error','message':'Balance token not enough'}
            else:
                return {'status':'error','message':'Unknown error'}
    def send_native_token(self,sender_wallet,receive_wallet,sender_wallet_key,value=-1,gwei = 5,timeout=20):
        balance_fee = self.get_native_balance(sender_wallet)
        print('Native token: '+str(balance_fee))
        if balance_fee > 0.000105 and value == -1:
            value = balance_fee - Decimal(0.000105)
        if balance_fee > 0 and balance_fee>value:
            nonce = self.web3.eth.getTransactionCount(sender_wallet)
            sender_wallet = Web3.toChecksumAddress(sender_wallet)
            tx = {
                'nonce':nonce,
                'to':receive_wallet,
                'value':self.web3.toWei(value,'ether'),
                'gas':21000,
                'gasPrice': self.web3.toWei(gwei, 'gwei'),
                'chainId':self.chainId
            }
            signed_tx = self.web3.eth.account.signTransaction(tx,sender_wallet_key)
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print('Transaction pending hash:: '+str(tx_hash.hex()))
            check_transaction = self.web3.eth.waitForTransactionReceipt(tx_hash,timeout=timeout)
            if check_transaction.status ==1:
                return {'status':'success','message':'Transaction successfully','tx':tx_hash.hex()}
            else:
                return {'status':'error','message':'Transaction failed!','tx':tx_hash.hex()}
        else:
            if balance_fee <= 0:
                return {'status':'error','message':'Balance fee not enough'}
            else:
                return {'status':'error','message':'Unknown error|Not enough token to send!'}


dcs = DCSCHAIN('bsc')
# dcs.set_contract('0x3b78458981eb7260d1f781cb8be2caac7027dbe2')
# print(dcs.get_token_balance('0x74D17aB9c31b14d36D84E22Cc31969cbe0ae5b4a'))

# sender_wallet = '0x6A92e664FD1Dc35A22BDcC4c9D7992352c4456b9'
# receive_wallet = '0x5E4A490fFE7eBAC03b22dbaffb5f5a5d0292CFA3'
# sender_wallet_key = '024b62126357f95eb207e3f390c8bfbd73bdb05eae94b852564db2f217c34980'
# print(dcs.send_token(sender_wallet,receive_wallet,sender_wallet_key,value=0.001,gas=160000))

# 0x04c747b40be4d535fc83d09939fb0f626f32800b
# 0x3b78458981eb7260d1f781cb8be2caac7027dbe2

# dcs = DCSCHAIN('polygon')
# dcs.set_contract('0x7e4c577ca35913af564ee2a24d882a4946ec492b')
# print(dcs.get_token_balance('0x4EaC0Fc56d427262a041e79D714d9d8aA4639D32'))
