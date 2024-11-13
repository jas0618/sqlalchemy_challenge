# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func 
from flask import Flask, jsonify
from datetime import datetime,timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("splite:///hawaii.splite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    start_date = latest_date - timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()
    
    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    start_date = latest_date - timedelta(days=365)
    
    most_active_station = session.query(Measurement.station).group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc()).first()[0]
    
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= start_date).all()
    
    session.close()
    
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)
    
    if end:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()
    
    session.close()
    
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": round(results[0][1], 2),
        "TMAX": results[0][2]
    }
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)