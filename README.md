The purpose of this project is meant to track all my options(past, current, and planned). Also want to get this hooked up with my broker and get a UI/webpage for this

General plans:
Will be using Python for the backend logic and JavaScript for the webpage stuff

Use Python yfinance library to query data from Yahoo finance

Store the data on options I've held and are holding locally using CSVs, JSON, SQLite, or something else. pandas is good for this

UI/webpage should be handled using JavaScript with a framework like React or Vue.js. Python can act as the backend server using Flask or FastAPI


Specific implementation ideas:
On startup, parse all the data stored locally. Then, for all the options that have not been closed yet, go from closest to expiry to furthest to expiry date.
If any of the contracts have already expired, update them dynamically by fetching the underlying stock's price and then determining whether they were ITM or OTM.

APIs:
addContract: Adds an option contract in
closeContract: Closes a currently open option contract
getContract: Gets an option contract corresponding to the contractId we've assigned it
deleteContract: Deletes a contract. This is different from closeContract, as we want to get rid of all records corresponding to this contract.

OptionsPosition class:
positionId: This will be a unique increasing number(starting from 1) which maps to a contract
ticker
contractType: Put or call
quantity: The number of contracts opened. Positive = long, negative = short
strikePrice
expiryDate
premium: The price of the contract per underlying asset
openPrice: The price of the underlying asset when we opened this contract
openDate: The date when we opened this contract
profit: The total profit generated from these contracts. This takes into account opportunity cost too. For instance, for covered calls,
if strike was at 95, price was 1 per asset, and closeprice was 100, then profit is 95+1-100=-4.

