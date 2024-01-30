from src.main import app
from src import os_service


if "__main__" == __name__:
    os_service.init()
    app.run(debug=True)
