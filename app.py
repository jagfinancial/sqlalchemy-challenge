import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station


# Flask Setup
app = Flask(__name__)

# List all routes that are available
# Home Page

@app.route("/")
def home_page():
   
    return (
        f"SQL Alchemy-Challenge<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date>/<end_date<br/>"
      
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    """Return a list of all Precipitation Data"""
   
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").\
        all()

    session.close()
  
    
    # Convert the list to Dictionary
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
  
    session = Session(engine)

    #Return a JSON list of stations from the dataset.
      
    results = session.query(station.station).\
                 order_by(station.station).all()

    session.close()

    #Return a JSON list of stations from the dataset.
    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    

    results = session.query(measurement.date,  measurement.tobs,measurement.prcp).\
                filter(measurement.date >= '2016-08-23').\
                filter(measurement.station=='USC00519281').\
                order_by(measurement.date).all()

    session.close()

   

    # Convert the list to Dictionary

    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

    
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):

    session = Session(engine)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs) 

    return jsonify(start_date_tobs)

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
  
    session = Session(engine)
   
    # Query all tobs

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs) 
    

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)
 