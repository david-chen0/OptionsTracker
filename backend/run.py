# import asyncio
from src import create_app

if __name__ == '__main__':
    # TODO: Async not working as expected, fix this later
    # app = asyncio.run(create_app())

    app = create_app()

    app.run(debug=True)
