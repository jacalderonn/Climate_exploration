import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Saving reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

## Flask routes
# Home site
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start-date)<br/>"
        f"/api/v1.0/(start-date)/(end-date)<br/>"
        f"NOTE: Dates have to be in the format yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    # Query data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Convert into normal list
    data = list(np.ravel(results))
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stats():
    session = Session(engine)
    # Query data
    results = session.query(Station.id, Station.station).all()
    session.close()
    # Convert into normal list
    data = list(np.ravel(results))
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    # Query data
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter_by(station = "USC00519281").filter(Measurement.date > "2016-08-23").all()
    session.close()
    # Convert into normal list
    data = list(np.ravel(results))
    return jsonify(data)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    # Query data
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).all()
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).all()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).all()
    data_dict = [
        {"TMIN": tmin[0][0]},
        {"TAVG": tavg[0][0]},
        {"TMAX": tmax[0][0]}
    ]
    return jsonify(data_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    # Query data
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()
    data_dict = [
        {"TMIN": tmin[0][0]},
        {"TAVG": tavg[0][0]},
        {"TMAX": tmax[0][0]}
    ]
    return jsonify(data_dict)


if __name__ == '__main__':
    app.run(debug=True)
