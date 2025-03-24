Dependencies used:
Pip dependencies listed in requirements.txt
axios(npm)
tailwind(npm)
postcss(npm)
autoprefixer(npm)
framer-motion(npm)

To refresh TailwindCSS, run(in the frontend dir):
npx @tailwindcss/cli -i ./src/index.css -o ./src/output.css --watch


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

One main thing to have at the top is a jump-to section, which will let you jump to newly expired, active, or expired table


TODOs:
Add searching by fields(ex: search by ticker NVDA or search by expiration date)(frontend)

Add a "newly expired" section for contracts that expired since last time you opened app and also signs for "about to expire", etc(both)

Make the input section only as wide as necessary, not a set width of 1/4(frontend)

When adding expired contracts, it doesn't get added automatically due to the backend needing to fetch the price, which takes a while. Change it to show up automatically once it's added(will likely need async)

Add a way to clone contracts to the inputs and also other mechanisms to make making multiple positions easier

Add a price section for active contracts, which will query for the option's latest price only on first load or refresh(both)

Add a profit section for both active and expired positions. Expired positions profit will be set using the premium, strike, and close price while active
positions profit will require adding a query for the option's current price and then subtracting from the initial premium.(both)

Look into making the operations async. Separation between frontend and backend, we can show things frontend and async do things in the backend, like delete from frontend then async delete from backend DB(backend)

Make sessions sync their data, ex: people can have multiple tabs open(both)

Explore all the possibilities that yf offers and try to see what can be improved using that. For example, yf offers something to display the next upcoming earnings date(backend)
