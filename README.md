Dependencies used:
Pip dependencies listed in requirements.txt
axios(npm)
tailwind(npm)
postcss(npm)
autoprefixer(npm)
framer-motion(npm)

To refresh TailwindCSS, run(in the frontend dir):
```
npx @tailwindcss/cli -i ./src/index.css -o ./src/output.css --watch
```

To start webpage/server(for now):
On one terminal, first launch the virtual env using `.\venv\Scripts\Activate`

Then do `python backend/run.py`

On another, go into frontend directory then do `npm start`
The above is for dev mode, to use a production build first build it with `npm run build` then run `serve -s build`

Webpage will be at http://localhost:3000/, running `npm start` should autostart it though

PSQL:
Use \l to see databases
Use \c <DB> to go into a DB
Use \d to list all the tables in a DB
Use \d <table_name> to describe a table/sequence
Use ALTER SEQUENCE <sequence_name> RESTART WITH 1; to restart a sequence


TODOs:
MAYBE: Pivot this(or make a new project) where we just setup a site for my projects and you can click on each individual one to use

Add searching by fields(ex: search by ticker NVDA or search by expiration date)(frontend)

Add a little refresh button to get latest prices too(maybe only have it work during market hours?)

Add percentage to profit

Make a loading screen since it takes a while to load the current prices

Containerize the application(so that anyone can spin it up) and then formalize everything lying around(basically get it ready as if an MVP)
Note that containerizing will isolate most things(ex: PSQL), will take a long time to setup but once setup anyone can run this app
by just spinning up the container

Add financial data(ex: implied volatility, delta, etc)

Allow users to update fields(ex: quantity, premium)

Add a "newly expired" section for contracts that expired since last time you opened app and also signs for "about to expire", etc(both)

Make the input section only as wide as necessary, not a set width of 1/6(frontend)

Add a way to clone contracts to the inputs and also other mechanisms to make making multiple positions easier

Look into making the operations async. Separation between frontend and backend, we can show things frontend and async do things in the backend, like delete from frontend then async delete from backend DB(backend)

Make sessions sync their data, ex: people can have multiple tabs open(both)

Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date(backend)
