# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Starting Date (12 months ago)
start_date = '2016-08-23'

@app.route("/")
def welcome():
    return (
        f"<p>Welcome to the Hawaii weather API.</p>"
        f"<p>How to use the API:</p>"
        f"/api/v1.0/precipitation<br/>JSON dictionary of the percipitation data<br/><br/>"
        f"/api/v1.0/stations<br/>JSON list of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>JSON list of temperatures observed (tobs)<br/><br/>"
        f"/api/v1.0/selected_start_date<br/>JSON list of the min temp, avg temp, and the max temp based on selected start date<br/><br/>"
        f"/api/v1.0/start_date/end_date<br/>JSON list of the min, avg, and max temp<br/><br/>"
    )

# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    precip_result = session.query(measurement.date, func.avg(measurement.prcp)).filter(measurement.date >= start_date).group_by(measurement.date).all()
    

    precip_keys = []
    precip_values = []
    for item in range(len(precip_result)):
        precip_keys.append(precip_result[item][0])
        precip_values.append(precip_result[item][1])
    

    precip_dictionary = dict(zip(precip_keys, precip_values))


    return jsonify(precip_dictionary)


# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():

    station_result = session.query(station.station, station.name).all()
    

    station_list = []
    for item in range(len(station_result)):
        station_list.append([station_result[item][0],station_result[item][1]])
    

    return jsonify(station_list)


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():

    tobs_results = session.query(measurement.date, measurement.station, measurement.tobs).filter(measurement.date >= start_date).filter(measurement.station == 'USC00519281').all()
    

    tobs_list = []
    for item in range(len(tobs_results)):
        tobs_list.append([tobs_results[item][0],tobs_results[item][1],tobs_results[item][2]])
    
    return jsonify(tobs_list)


# /api/v1.0/<selected_start_date>
@app.route("/api/v1.0/<selected_start_date>")
def data_from_start_date(selected_start_date):

    temperature_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= selected_start_date).all()


    temperature_list = []
    for item in range(len(temperature_results)):
        temperature_list.append([temperature_results[item][0],temperature_results[item][1],temperature_results[item][2]])
    

    return jsonify(temperature_list)


# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def data_from_date_range(start_date,end_date):

    multi_date_temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    

    temperature_list = []
    for item in range(len(multi_date_temp_results)):
        temperature_list.append([multi_date_temp_results[item][0],multi_date_temp_results[item][1],multi_date_temp_results[item][2]])
    

    return jsonify(temperature_list)

if __name__ == "__main__":
    app.run(debug=True)