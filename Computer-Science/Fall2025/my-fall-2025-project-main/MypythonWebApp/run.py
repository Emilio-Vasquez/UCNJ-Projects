'''
this is the run.py script
this script will run the application on a development server
the purpose of the script is to serve as an entry point to the flask app
all it does:
   - import the flask application function we created in the init.py (create_app)
   - then it runs the app, with the debug mode on
'''

from app import create_app
## this creates the falsk application instance
app = create_app()
## now run the flask development server
if __name__ == "__main__":
    ##it sets the __name__ variable = ""__main__"
    ## __name__ should be the same as __main__
    app.run(debug=True)