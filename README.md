# Binance Smart Chain TradingBot

## About The Project
BSCTradingBot consists of 3 Bots Automated, Buy and Sell. 

Requirements:
  - Bot only works for bsc tokens on pancakeswap 
  - Your need to have some wbnb in your wallet to use this bot
  
## Getting Started
When you download the BSCTradingBot, you will find a config.json file. This is where you need to add the following data.
  - Wallet Address: your BSC wallet address (e.g., Metamask)
  - Private Key: your private key of your wallet address in hex, not the mnemonic phrase 
  - Gas amount: amount of max gas to use per transaction. Recommended to leave at default.
  - Gasprice: max price of gas to use per transaction. Recommended to leave at default.

To start BSCTradingBot double-click on main.exe file. 


### Automated Bot: 
Functionality: It listens to a telegram channel to get new tokens published on coinmarketcap.
              Buys a token and monitors the price. 
              After setted conditions are reached it sells the token.

inputs:
  - Token to buy address: The contract address of the token you want to snipe
  - Quantity: Amount of BNB you want to use for the trade (example: 0.02 means you want to buy the token for 0.02 BNB)
  - Take profit: Value must be greater than 1. It's a win limit, at which you want to sell the Token (example: 2 means sell token after you made 2x) 
  - Stop loss: Value must be between [0, 1[. It's a loss limit, at which you want to sell the token (example: 0.2 means sell token after value 
    goes down by 20 %)
  - Sell Quantity: value must be between [0, 1] example: 0.2 means sell 20 % of token if limit( take profit, stop loss) reached 
  

### Buy Bot:
Functionality: This Bot only buys once and does not sell.

inputs:
  - Token to buy address: The contract address of the token you want to buy
  - Quantity: Amount of BNB you want to use for the trade (example: 0.02 means you want to buy the token for 0.02 BNB)


### Sell Bot:
Functionality: This Bot only sell once.

inputs:
  - Token to sell address: The contract address of the token you want to sell
  - Quantity of token in %: Percentage of the total balance you want to sell (example: 0.2 means you want to sell 20% of total balance)

## Common errors and how to fix them
  - ValueError: {'code': -32000, 'message': '(replacement) transaction underpriced'}: You are using too low gas. Increase gas price / limit and restart. 
  - ValueError: {'code': -32000, 'message': 'insufficient funds for gas * price + value'}:
You do not have enough BNB in your wallet to snipe/buy with, or you do not have enough of the token you want to sell. Make sure your wallet has enough BNB / token to sell and try again.
   
  You may wonder why this issue happens even if you have enough BNB in your wallet. 
  Usually the reason is how the gas is calculated: even though you are very unlikely to use the full gas limit (eg. 2.5 mil) the bot still needs to make sure that you could technically afford it and enough BNB to pay for the snipe. 
  1 gwei is 0.000000001, so 5 gwei is 0.000000005. When you multiply 0.000000005 by 2.5 million you get 0.0125 BNB, so for these settings you would need at least this amount + snipe amount in your wallet. 
  You can reduce the amount needed in your wallet by reducing the gas limit.

  ### !!! Always check transaction Hash on https://bscscan.com/ for more information !!!
  Do not hesitate to report (write me a msg on telegram) any error that are not listed here.  

## Risks

Investing in BSC tokens / shitcoins is risky and you should be aware you could lose all your money. For this reason, NEVER invest more money than you can afford to lose.
This Bot do not check tokens of scam.

Crypto scams are on the rise and it seems the vast majority of tokens are either straight up scams or are too risky eg. unlocked liquidity).

So be aware and make sure the token you are buying is safe.


