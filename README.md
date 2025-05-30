# OptionsTracker
<p align="center">
    <img src="docs/options_tracker_landing.png" alt="drawing" width="50%">
</p>

## Description
My personal way of tracking all my current and expired option positions.

Currently this has to be run locally. The Github Pages page does show the frontend, but I haven't connected it to any server cuz I don't wanna pay for one :D. Instructions to run locally included below

I plan to containerize this sometime in the future so it's really easy for anyone to use

Make sure to set the env variables, otherwise this project won't work. Check out `.env.example` for an example

## Using the project
### Backend
To start webpage/server(for now):
On one terminal, first launch the virtual env using `.\venv\Scripts\Activate`

Then do `python backend/run.py`

### DB
PSQL:
Use \l to see databases
Use \c <DB> to go into a DB
Use \d to list all the tables in a DB
Use \d <table_name> to describe a table/sequence
Use ALTER SEQUENCE <sequence_name> RESTART WITH 1; to restart a sequence

### Frontend
On another, go into frontend directory(`cd frontend`) then run `npm start`
The above is for dev mode, to use a production build first build it with `npm run build` then run `serve -s build`

Webpage will be at http://localhost:3000/, running `npm start` should autostart it though

GITHUB PAGES:
Currently deployed to Github Pages using gh-pages dependency

Need to run `npm run deploy` from the frontend directory to directly deploy the static files to Github Pages

THE BACKEND DOES NOT WORK, GITHUB PAGES ONLY SERVES STATIC FILES

To refresh TailwindCSS, run(in the frontend dir):
```
npx @tailwindcss/cli -i ./src/index.css -o ./src/output.css --watch
```


## ToDos
Containerize the application(so that anyone can spin it up) and then formalize everything lying around(basically get it ready as if an MVP)
Note that containerizing will isolate most things(ex: PSQL), will take a long time to setup but once setup anyone can run this app
by just spinning up the container

Add searching by fields(ex: search by ticker NVDA or search by expiration date)

Add a little refresh button to get latest prices too(maybe only have it work during market hours?)

Add percentage to profit

Make a loading screen since it takes a while to load the current prices

Add financial data(ex: implied volatility, delta, etc)

Allow users to update fields(ex: quantity, premium)

Add a "newly expired" section for contracts that expired since last time you opened app and also signs for "about to expire", etc

Make the input section only as wide as necessary, not a set width of 1/6

Add a way to clone contracts to the inputs and also other mechanisms to make making multiple positions easier

Look into making the operations async. Separation between frontend and backend, we can show things frontend and async do things in the backend, like delete from frontend then async delete from backend DB

Make sessions sync their data, ex: people can have multiple tabs open

Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date
