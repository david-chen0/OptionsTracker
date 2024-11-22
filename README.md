Dependencies used:
Python/pip
yfinance
Flask
pandas
numpy
aiofiles
pytest
pytest-asynchio

The purpose of this project is meant to track all my options(past, current, and planned). Also want to get this hooked up with my broker and get a UI/webpage for this

General plans:
Will be using Python for the backend logic and JavaScript for the webpage stuff

Use Python yfinance library to query data from Yahoo finance

Store the data on options I've held and are holding locally using CSVs, JSON, SQLite, or something else. pandas is good for this

UI/webpage should be handled using JavaScript with a framework like React or Vue.js. Python can act as the backend server using Flask or FastAPI


Specific implementation ideas:
THERE WILL BE TWO JSON FILES FOR STORING LOCAL DATA. JSON files will be list of dicts. The files will be for active contracts(active_contracts.json) and inactive contracts(inactive_contracts.json).
These files will be sorted by expiry data with the earliest expiry date being at the front and the latest expiry date being at the end.

On startup, first parse inactive_contracts and store them locally. The JSON object should still be kept so that we can easily make changes.

Next, look through active_contracts. For all the inactive contracts(do a current date check) in active_contracts, check the underlying asset's price and update the contract to be either OTM or ITM.
Then, delete this from active_contracts and then add this to inactive_contracts. Then add them to a list, which we will display under "newly expired contracts" section

Finally, just parse the rest of the active contracts as normal

APIs:
addContract: Adds an option contract in
closeContract: Closes a currently open option contract
getContract: Gets an option contract corresponding to the contractId we've assigned it
deleteContract: Deletes a contract. This is different from closeContract, as we want to get rid of all records corresponding to this contract.


Files and folders inside src/:
main.py: This will be where the main logic is implemented
data folder: This folder will contain all the logic for editing and accessing the locally stored data, along with where the locally stored data will be located
util folder: This will be for util methods and classes
web folder: This will be for all the web stuff(flask routes and endpoints, html templates, static files for things like css, JS, and images). this could look like web/, where
inside there is routes.py for flask routes and endpoints, templates/ for html templates, and static/ for the static files


TODOs that won't be implemented yet but should be done:
Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date

The JSON local stores should be done async. This means that when we receive a request to edit a contract(let's say we close it before expiry), we'll first process that request and show them the results of our updated memory(ex: if we use a dict or something like that), and then we run a thread or something async to update our locally stored json

