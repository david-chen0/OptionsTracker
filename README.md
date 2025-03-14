Dependencies used:
Pip dependencies listed in requirements.txt
axios(npm)
tailwind(npm)
postcss(npm)
autoprefixer(npm)

Change the project to fit this structure:
OptionsTracker/
├── backend/                  # Flask backend files (Python)
│   ├── src/                  # Your Flask app folder
│   │   ├── __init__.py       # Initialize Flask app and routing
│   │   ├── routes.py         # API routes for the Flask app
│   │   ├── models.py         # Database models and backend logic
│   │   └── service_logic     # Folders and files for service logic
│   ├── test/                 # Tests for backend code
│   │   ├── __init__.py
│   │   ├── test_routes.py    # Tests for the Flask routes
│   │   ├── test_services.py  # Tests for the backend services
│   │   └── test_models.py    # Tests for backend models
|   └── run.py                # Script to run the Flask backend
│   ├── requirements.txt      # List of backend dependencies
│   └── config.py             # Configuration settings for Flask
├── frontend/                 # React frontend files
│   ├── public/               # Public static files (e.g., index.html, images)
│   ├── src/                  # React app source code
│   │   ├── components/       # Reusable React components
│   │   ├── pages/            # React pages (views)
│   │   ├── services/         # API calls to Flask backend
│   │   ├── App.js            # Main React app component
│   │   └── index.js          # React entry point
│   ├── package.json          # Frontend dependencies and scripts
│   └── .env                  # Frontend environment variables
├── data/                     # Local data files (e.g. JSON files, CSVs)
├── .gitignore                # Ignore unnecessary files in Git
├── README.md                 # Project overview and setup instructions


To start webpage/server(for now):
On one terminal, first launch the virtual env using
.\venv\Scripts\Activate

Then do
python backend/run.py

On another, go into frontend directory then do
npm start

Webpage will be at http://localhost:3000/, running npm start should autostart it though

PSQL:
Use \l to see databases
Use \c <DB> to go into a DB
Use \d to list all the tables in a DB
Use \d <table_name> to describe a table/sequence


AFTER BUSINESS LOGIC IS MORE COMPLETE, UPDATE THIS
Specific implementation ideas:
THERE WILL BE TWO JSON FILES FOR STORING LOCAL DATA. JSON files will be list of dicts. The files will be for active contracts(active_contracts.json) and inactive contracts(inactive_contracts.json).
These files will be sorted by expiry data with the earliest expiry date being at the front and the latest expiry date being at the end.

On startup, first parse inactive_contracts and store them locally. The JSON object should still be kept so that we can easily make changes.

Next, look through active_contracts. For all the inactive contracts(do a current date check) in active_contracts, check the underlying asset's price and update the contract to be either OTM or ITM.
Then, delete this from active_contracts and then add this to inactive_contracts.

Finally, just parse the rest of the active contracts as normal.

On the webpage, we will have an "active option positions" section and an "inactive option positions" section

APIs:
addContract: Adds an option contract in
closeContract: Closes a currently open option contract
getContract: Gets an option contract corresponding to the contractId we've assigned it
deleteContract: Deletes a contract. This is different from closeContract, as we want to get rid of all records corresponding to this contract.

Table schema:
ticker (str): The ticker symbol(ex: AAPL) for the underlying security
contract_type (ContractType): The type of contract
quantity (int): The number of contracts opened
strike_price (float): The strike price of the contracts
expiration_date (str): The expiration date of the contracts, represented as YYYY-MM-DD
premium (float): The premium per security for each of the contracts
open_price (float): The price of the underlying security when the contract was opened
open_date (str): The date that the contract was opened, represented as YYYY-MM-DD
contract_status (PositionStatus): The status of the options position. NOT SETTABLE BY USER, THIS WILL DEFAULT TO OPEN AND WILL BE HANDLED IN THE BACKEND

Possible table addons:
current_price (float): The current price of a contract. Float for open contracts, 0.0 for closed contracts



TODOs:
Change the current code to accept a serial number as the unique id, that way we can easily connect it once psql is setup
rn i think i have everything setup in the backend for it, but we need to pass this value to the frontend so that it can also keep track of it without displaying it
this is needed for operations like delete, get, etc

Change to a better DB system using PostgreSQL.

Add a delete button for the contracts. It should be like a red X next to the contract in the table and when it's clicked, it first gives a warning then it deletes if user hits yes

Figure out how the website should be arranged(where to put the tables, where to put the add contract form, etc)

Add a "newly expired" section for contracts that expired since last time you opened app and also signs for "about to expire", etc

Add sorting, grouping, and searching by custom fields(ex: sort/group/search by ticker NVDA)

Make different fields per table, for example inactive contracts should have profit and close price while active table shouldn't

Add a profit section for both active and inactive positions. Inactive positions profit will be set using the premium, strike, and close price while active
positions profit will require adding a query for the option's current price and then subtracting from the initial premium.

Look into making the operations async. Separation between frontend and backend, we can show things frontend and async do things in the backend, like delete from frontend then async delete from backend DB

Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date
