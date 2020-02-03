from flask import Flask, render_template, redirect
import flask
import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    mars = list(db.data.find())
    print(mars)

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrapes():
    #execute scrape script and return dictionary
    mars_data = scrape.scrape()

    # Drops collection if available to remove duplicates
    db.data.drop()

    # Creates a collection in the database and inserts two documents
    db.data.insert_one(mars_data)

    return redirect('/')
    


if __name__ == "__main__":
    app.run(debug=True)
