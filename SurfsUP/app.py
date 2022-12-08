# Import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import datetime as dt

# Database set-up
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Store last date of data
date = dt.date(2017, 8, 23)

# Flask set-up
app = Flask(__name__)

# Flask routes

#landing page route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start_date><br/>"
        f"/api/v1.0/start/end/<start_date>/<end_date><br/>"
    )

# Precipitation route

@app.route("/api/v1.0/precipitation")

# Precipitation page query function
def precip():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement table for precipitation in the last year
    precip_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > (date - dt.timedelta(days = 365))).\
        group_by(measurement.date).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(precip_data))

    return jsonify(data)


# Stations route
@app.route("/api/v1.0/stations")

# Stations page query function
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query stations table to return all stations
    stations = session.query(station.station).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(stations))

    return jsonify(station_data)

# TObs route
@app.route("/api/v1.0/tobs")

# tobs page query function
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement table to return all temps from station USC00519281 for the last 3 years
    tobs_active_station = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date > (date - dt.timedelta(days = 3*365))).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(tobs_active_station))

    return jsonify(tobs_data)

# Start date route
@app.route("/api/v1.0/start/<start_date>")

# start page query function
def start(start_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query that accepts given start date to end and returns min, max, and average temps
    sel = [measurement.station, 
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]
    start_date_temps = session.query(*sel).filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= start_date).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    start_data = list(np.ravel(start_date_temps))

    return jsonify(start_data)

# Start and end date route
@app.route("/api/v1.0/start/end/<start_date>/<end_date>")

# start and end page query function
def startend(start_date, end_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query that accepts given start date to end and returns min, max, and average temps
    sel = [measurement.station, 
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]
    start_end_date_temps = session.query(*sel).filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    start_end_data = list(np.ravel(start_end_date_temps))

    return jsonify(start_end_data)

if __name__ == "__main__":
    app.run(debug=True)