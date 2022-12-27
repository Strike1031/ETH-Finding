from codecs import backslashreplace_errors
from functools import cache
from json import JSONDecodeError
from platform import java_ver
from progressbar import ProgressBar, Percentage, Bar, ETA
from pprint import pprint
import blocksmith, time, sys, os, uuid, datetime
from dotenv import load_dotenv
from etherscan import Etherscan
from pathlib import Path
import random

load_dotenv()
eth = Etherscan(os.environ.get("ETHERSCAN_API_KEY"))
searchAddresses = os.environ.get('SEARCH_ADDRESSES')
intoFile = bool(os.environ.get('OUTPUT_TO_FILE'))


amountToGen=int(os.environ.get("AMOUNT_TO_GENERATE"))
basic_startPrivateKey=hex(int(os.environ.get("START_PRIVATE_KEY"),0))
basic_startPrivateKey = int(basic_startPrivateKey, 0)
#Start private address  example:0x3f3493044924290290290902492... (64byte)
#basic_startPrivateKey = 0xbfd1054b382a415fa4e52efd9d21657f9382c9d89f9933f46457a1a225852535

# Define global (non .env) variables
pbar = ProgressBar()
savedAddresses = []
savedKeys = []


##############################################
#     Functions from Blocksmith Library      #
##############################################
def generatePrivateKey():
    # Generate Private Key
    kg = blocksmith.KeyGenerator()
    kg.seed_input('since rule enact rally actress weasel chapter ivory ensure entire flock exchange')
    key = kg.generate_key()
    return key

def privateKeyToBitcoinWallet(key):
    # Create Bitcoin wallet from private key
    address = blocksmith.BitcoinWallet.generate_address(key)
    return address
    

def privateKeyToEthereumWallet(key):
    # Create Ethereum wallet from private key
    address = blocksmith.EthereumWallet.generate_address(key)
    checksum_address = blocksmith.EthereumWallet.checksum_address(address)
    return checksum_address


##############################################
#   Finging Valueable Wallets   #
##############################################
def finding(amount=amountToGen, startPrivateKey = basic_startPrivateKey, unique_filename="data.txt", printVals=False, saveAll=False):
    try:    
        with open(unique_filename, 'w') as outFile:
            print("Finding...")
            # for i in pbar(range(amount)):
            for i in range(amount):
                # privateKey = generatePrivateKey()
                time.sleep(random.uniform(0, 1.0)) #after random seconds between a range
                print(i)
                privateKey = startPrivateKey + i
                privateKey = hex(privateKey)[2:]
                privateKey = privateKey.zfill(32 * 2)
                #print("Prviate key: ", privateKey)
                walletAddress = privateKeyToEthereumWallet(privateKey)
                #print('public key: ', walletAddress)
                if printVals == True:
                    print(f"{walletAddress}\t:\t{privateKey}")
                if saveAll == True:
                    savedAddresses.append(walletAddress)
                    savedKeys.append(privateKey)
                # If you want to check individual balances as you generate them, use the following block of code
                try:
                    balance = eth.get_eth_balance(walletAddress)
                    #print(balance)
                    if balance != '0':
                        print("Ether detected!", i)
                        print("Wallet: ", walletAddress)
                        print("Private Key: ", privateKey)
                        print("Balance: ", balance)
                        savedAddresses.append(walletAddress)
                        savedKeys.append(privateKey)
                        outFile.write("\nWALLET FOUND")
                        outFile.write(f"\nWallet Address: {walletAddress}")
                        outFile.write(f"\nPrivate Key: {privateKey}")
                except JSONDecodeError:
                    # If you would like to track how many API calls fail (due to your limit being exceeded or some other issue) you can put your logic here
                    #balanceCheckFailCount = balanceCheckFailCount + 1
                    pass
    except:
        global basic_startPrivateKey
        basic_startPrivateKey = basic_startPrivateKey + 0x100000
        currentDT = datetime.datetime.now()
        filename = str(currentDT.year)+"_"+str(currentDT.month)+"_"+str(currentDT.day)+"_"+str(currentDT.hour)+"_"+str(currentDT.minute)+"_"+str(currentDT.second)
        filename = "collection\\" + filename + ".txt"
        finding(amount=amountToGen,startPrivateKey = basic_startPrivateKey, unique_filename=filename)


if __name__ == '__main__':
    currentDT = datetime.datetime.now()
    filename = str(currentDT.year)+"_"+str(currentDT.month)+"_"+str(currentDT.day)+"_"+str(currentDT.hour)+"_"+str(currentDT.minute)+"_"+str(currentDT.second)
    filename = "collection\\" + filename + ".txt"
    finding(amountToGen, basic_startPrivateKey, filename)