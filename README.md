# WatchList

WatchList is built in Flask and allows users to create custom lists of shows that they want to watch. Shows are stored centrally in the database and can then be added to the lists of individual users with any notes they may want to keep about the show. The repository also includes a CI (continuous integration) pipeline for linting (Pylint) and basic unit testing (Pytest) that occurs when there's a pull request to main. It's also set up with Docker.

## Running the code
This is mostly for my own reference, there are not full instructions on how to build and run this yet. 

To build docker image: ``docker build --tag watchlist-docker .`` 

To run PostgreSQL db (on windows): ``psql -U watcher -h 127.0.0.1 -d watchdb``

If you do want to run this, you'll also have to set up your own config.py file with a secret key, Postgres path, etc.

## Features to-do:
- Integrate app logic/endpoints with HTML
All of the backend logic works, but a lot of it currently serves raw JSON and isn't integrated with the HTML/actual pages of the app. 
- User access type restrictions
- Containerize database
- Move onto AWS (or other cloud service)
- Implement CD pipeline

Things I think would be fun but are not essential:
- Make it look pretty with CSS (graphic design is not my passion)
- Additional unit tests
- Set up Terraform to manage cloud resources + permissions
- Rate limit endpoints

