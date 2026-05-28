from app import create_app
from dotenv import load_dotenv

import os

load_dotenv()


if __name__ == '__main__':
    app = create_app()
    port= os.getenv('PORT',4500)
    debug=os.getenv('FLASK_DEBUG',"False")=="True"
    app.run(port=port,debug=debug)