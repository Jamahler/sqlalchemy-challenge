import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt
import numpy as np

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
         f"<br>List of Routes:<br/>"
         
         f"<br>/api/v1.0/precipitation<br/>"
                  
         f"<br>/api/v1.0/stations<br/>"
         
         f"<br>/api/v1.0/tobs<br/>"

         f"<br>/api/v1.0/&lt;start&gt;<br/>" 
                 
         f"<br>/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"         
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date <= '2017-08-23').filter(measurement.date >= '2016-08-23').all()

    precipitation = dict(results)
   
    return jsonify(precipitation)
    
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    
    stations_l = list(np.ravel(results))
    
    return jsonify(stations_l)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(measurement.date, measurement.tobs).group_by(measurement.date).\
        filter(measurement.date <= '2017-08-23').filter(measurement.date >= '2016-08-23').all()

    temperature = list(np.ravel(results))
    return jsonify(temperature)

@app.route("/api/v1.0/<start>")
def start(start=None):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()

    start_temps = list(np.ravel(results))

    return jsonify(start_temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
    .filter(measurement.date >= start).filter(measurement.date <= end).all()

    start_end_temps = list(np.ravel(results))
    
    return jsonify(start_end_temps)

if __name__ == '__main__':
    app.run(debug=True)