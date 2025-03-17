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
Use ALTER SEQUENCE <sequence_name> RESTART WITH 1; to restart a sequence


TODO: Flush out the code's logic of how everything works in the backend here once it's all been decided


Frontend idea:
The page will sorta be split into two parts, one part(on the left) contains the tables, we'll call this TableSection, and the other part(on the right) contains the input boxes, we'll call this InputSection

TableSection:
This will take up most of the screen width(let's say around 75%). When the InputSection is hidden(see that section for it), it should take up all of the width

Top will be newly expired section(once we implement it, skip for now) followed by active, then expired positions


InputSection:
This will take up just about 25% of the screen width

There'll be an option to hide this, in which the InputSection just slides into to right and disappears with a tiny tab/bar that can be clicked to pull it back out

The inputs will be at the bottom, while the top will contain other stuff

One main thing to have at the top is a jump-to section, which will let you jump to newly expired, active, or inactive table


TODOs:
Figure out how the website should be arranged(where to put the tables, where to put the add contract form, etc)

Switch all "inactive" terminology to "expired"

Add a "newly expired" section for contracts that expired since last time you opened app and also signs for "about to expire", etc

Add sorting, grouping, and searching by custom fields(ex: sort/group/search by ticker NVDA)

Add a profit section for both active and inactive positions. Inactive positions profit will be set using the premium, strike, and close price while active
positions profit will require adding a query for the option's current price and then subtracting from the initial premium.

Look into making the operations async. Separation between frontend and backend, we can show things frontend and async do things in the backend, like delete from frontend then async delete from backend DB

Make sessions sync their data, ex: people can have multiple tabs open

Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date
