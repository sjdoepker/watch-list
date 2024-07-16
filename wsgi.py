# runs flask in production mode
from src.app import app

if __name__ == '__main__':
    app.run(debug=False)

#for running the server on windows (if you need to for some reason) use waitress, eg:
# waitress-serve --threads=1 --listen=127.0.0.1:8000 src:app
# (currently broken but it shouldn't matter)
