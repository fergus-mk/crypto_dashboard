# Overview

The cryptocurrency price dashboard displays details about cryptocurrencies. The following details are shown:

- Name - the name of the crytpocurrency
- Symbol - the symbol representing the cryptocurrency 
- Price - the current price of the cryptocurrency
- Total supply - the total number of coins of the cryptocurrency in circulation
- Max supply - the total number of coins of the cryptocurrency that can be made. Note most crypto's have no limit
- Market Cap - market cap is coin price * total supply

## Use 

The dashboard has simple functionality. To add a crypto to the dashboard click 'Add Crypto' and type its name. Note details of cryptos are retrieved using the Coin Market Cap API (https://coinmarketcap.com/api/). In order to use the dashboard you must create a developer account for the Coin MArket API (this is free) and save the key in the 'keys.py' file. If a crypto is not available in the API it is not added.

The dashbaord provides functioanlity for filtering, this is done either on:
- Price (only cryptos with a price over the input value are displayed)
- Market cap (only cryptos with a market cap over the input value are displayed)

## Notes

This is only a beta version. Increased functionality will be added so that:

A. The page automatically refreshes when new cryptos are added

B. It is possible to remove cryptos from the dashboard

## Insparation

Note this project has been inspired by: https://github.com/hackingthemarkets/stockscreener





