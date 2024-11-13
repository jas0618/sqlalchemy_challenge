## Reflect Tables into SQLAlchemy ORM 
- pthyon SQL toolkit and object relational mapper(downloaded sqlalchemy, session, create_engine and metadata)
- link the resources to the create engine for measurements and stations 
- created the database for the new model, reflect the tables and view all the classes found under automap
- saved the references for the links under measurement and station
## Exploratory Precipitation Analysis 
- using the link to measurement- order the dates in descending
- date range- periods and frequency
- precipiation- date range- random(round)
- most recent date- date max
- one year ago - most recent date- subtract the number of days
- last 12 month data- calculated the percipitation data is more than one year ago
- sorted the data by date- sorted the values by date
- using pandas to plot the line graph(date vs precipitation)
-simulating percipiatation dataset- a summary table of the total count, mean, std, and min and max
## Exploratory Station Analysis 
-station list - based on station id 
-groupby and order by - station and descending 
- print the station ID and count
- caluated the lowest temperature, highest temperature and average temperature using sessions query
- the temperature vs frequency ploted the graph using pandas and stations and measurement dataframe
- closed the session

## App.py (api) 
-created the link to the resources- for measurement and station 

-created different api routes for precipitation, stations, tobs and start and start end

## Precipation Route 
- first define the session
- using the measurement and station query- order the dates in descending order
- filter for date and precp from the start date using filter function
- create a precipiation dictionary ( using the date and the analysises above)
* Please note tobs follows the same sequence 

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
    
## Station Route 
- first define the session
- second create session query referring to station dataset
  
  @app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)


  
-the station query, the latest date order by descending - from the start date to late date 

-api start and end date- calculated the function of max, min and avg 

-run the function using the terminal( please note there are some errors- tried my best to fix them) 
  

  
   
