# runs flask in production mode
from src.app import app

if __name__ == '__main__':
    app.run(debug=False)
