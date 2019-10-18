# import necessary libraries
import os
from sqlalchemy import create_engine
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################


# dburl = "sqlite:///db.sqlite"
dburl = "postgres://pqahrvlmkmfvmz:a23399fb321b1077bf988df28d8abc357f056602c83365949c8808e1d6af596a@ec2-54-235-100-99.compute-1.amazonaws.com:5432/dbns85t5gu8ndn"

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        insert_sql = f"insert into pets ( name, lat, lon) values ( '{name}', {lat}, {lon})"

        engine = create_engine(dburl)
        conn = engine.connect()
        conn.execute(insert_sql)
        conn.close()
        
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/pals")
def pals():
    
    engine = create_engine(dburl)
    conn = engine.connect()
    results = conn.execute("select name, lat, lon from pets").fetchall()
                      

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    conn.close()

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(pet_data)


if __name__ == "__main__":
    app.run()
