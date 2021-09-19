import config, time, ccxt, datetime
from etherscan import Etherscan
from flask import Flask, render_template, request, flash, redirect
from web3 import Web3
from ens import ENS

eth = Etherscan('Your Etherscan.io API key here') 

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = 'somerandomstring'

w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
ns = ENS.fromWeb3(w3)

def get_ethereum_price():
    binance = ccxt.binance()
    ethereum_price = binance.fetch_ticker('ETH/USDT')

    return ethereum_price

# custom filter for currency format
@app.template_filter()
def format_currency(value):
    return "${:,.2f}".format(value)

# homepage, creating a list of latest blocks and transaction on the Ethereum network.
@app.get("/")
def index():
    ethereum_price = get_ethereum_price()
    current_time = int(time.time())
    newest_block = int(eth.get_block_number_by_timestamp(current_time, 'before'))
    latest_blocks = []
    for newest_block in range(newest_block, newest_block-7, -1):
        block = w3.eth.getBlock(newest_block)
        latest_blocks.append(block)
    
    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-3:]:
        transaction = w3.eth.getTransaction(tx)
        latest_transactions.append(transaction)

    ether = w3.eth

    return render_template('index.html', 
        miners=config.MINERS,
        current_time=current_time, 
        ether=ether, 
        ethereum_price=ethereum_price,
        latest_blocks=latest_blocks,
        latest_transactions=latest_transactions)

# address page(using the Etherscan api to form a table of the transaction history)
@app.get("/address")
def address():
    address = request.args.get('address')
    ethereum_price = get_ethereum_price()

    try:
        address = w3.toChecksumAddress(address)  

    except:
        try:
            eth_address = ns.address(address)
            if eth_address != None and eth_address != "0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85":
                address = eth_address
            else:
                raise ValueError
                
        except ValueError as e:
            try:
                tx = w3.eth.get_transaction(address)
                return redirect(('/transaction/{}').format(address))

            except:
                flash('Invalid address', 'danger')
                return redirect('/')

    balance = w3.eth.get_balance(address)
    balance = w3.fromWei(balance, 'ether')
    tx_history = []
    try:
        tx_history = eth.get_normal_txs_by_address(address=address, startblock=0, endblock=999999999, sort='asc')
    except:
        flash('The wallet has no Transaction History', 'danger')
        return redirect('/')

    tx_dates = []
    for transaction in tx_history:
        timestamp = int(transaction['timeStamp'])
        current_time = datetime.datetime.fromtimestamp(timestamp)
        tx_dates.append(current_time)

    return render_template('address.html', ethereum_price=ethereum_price, address=address, balance=balance, tx_information=zip(tx_history, tx_dates))

# single block page
@app.get("/block/<block_number>")
def block(block_number):
    block = w3.eth.get_block(int(block_number))
    
    return render_template('block.html', block=block)

# single transaction page
@app.get('/transaction/<hash>')
def transaction(hash):
    tx = w3.eth.get_transaction(hash)
    value = w3.fromWei(tx.value, 'ether')
    receipt = w3.eth.get_transaction_receipt(hash)
    ethereum_price = get_ethereum_price()

    gas_price = w3.fromWei(tx.gasPrice, 'ether')
    return render_template('transaction.html', tx=tx, value=value, receipt=receipt, gas_price=gas_price, ethereum_price=ethereum_price)

if __name__ == "__main__":
    app.run()

