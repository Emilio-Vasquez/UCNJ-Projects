"""
This is the run.py script 

The purpose of this script is to serve as an entry point of the flask app 

All it does: 
    - import the flask application function we created in the __init__.py (created_app)
    - Then it runs the app, with the debug mode on 
"""

from app import create_app

## Creates the flask application instance 
app = create_app()

## Now run the flask development server 
if __name__ == "__main__":
    ## it set s the __name__ variable = "__main__"
    ## __name__ should be the same as __main__
    app.run(debug=True)