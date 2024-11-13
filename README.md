## Reflect Tables into SQLAlchemy ORM 
- pthyon SQL toolkit and object relational mapper(downloaded sqlalchemy, session, create_engine and metadata)
- link the resources to the create engine for measurements and stations
  
   Measurement = Base.classes.measurement
   Station = Base.classes.station

- created the database for the new model, reflect the tables and view all the classes found under automap
- saved the references for the links under measurement and station
   session = Session(engine)
  
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

In the Notebook: 
from datetime import timedelta
date_range = pd.date_range(end=pd.Timestamp.now(), periods=730, freq='D')
precipitation_data = pd.DataFrame({
    'date': date_range,
    'precipitation': (np.random.rand(len(date_range)) * 10).round(2)
})
# Find the most recent date in the dataset
most_recent_date = precipitation_data['date'].max()

# Calculate the date one year ago from the most recent date
one_year_ago = most_recent_date - timedelta(days=365)

# Query the data for the last 12 months
last_12_months_data = precipitation_data[precipitation_data['date'] > one_year_ago]

# Sort the data by date
last_12_months_data_sorted = last_12_months_data.sort_values(by='date')

# Plot the data using Pandas plotting with Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(last_12_months_data_sorted['date'], last_12_months_data_sorted['precipitation'], marker='o', linestyle='-', alpha=0.7)
plt.title('Precipitation Data for the Last 12 Months')
plt.xlabel('Date')
plt.ylabel('Precipitation (inches)')
plt.grid(True)
plt.show()

## Exploratory Station Analysis 
-station list - based on station id 
-groupby and order by - station and descending 
- print the station ID and count
- caluated the lowest temperature, highest temperature and average temperature using sessions query
- the temperature vs frequency ploted the graph using pandas and stations and measurement dataframe
- closed the session

 In the Notebook: 
# Calculate the date 12 months ago from the most recent date in the dataset
most_recent_date = session.query(func.max(Measurement.date)).scalar()
one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
most_active_station_id = 'USC00519281'
# Query the last 12 months of temperature observation data for the most active station
temperature_data = (
    session.query(Measurement.tobs)
    .filter(Measurement.station == most_active_station_id)
    .filter(Measurement.date >= one_year_ago)
    .all()
)

# Convert the query result to a list of temperatures
df = pd.DataFrame(temperature_data, columns=['tobs'])

# Plot the results as a histogram
df.plot.hist(bins=12, edgecolor='black')
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.title(f"Temperature Observations for Station {most_active_station_id} (Last 12 Months)")
plt.tight_layout()
plt.show()


## App.py (api) 
-created the link to the resources- for measurement and station 

-created different api routes for precipitation, stations, tobs and start and start end

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
## Precipation Route 
1. define the session
2. using the measurement and station query- order the dates in descending order
3. filter for date and precp from the start date using filter function
4. create a precipiation dictionary ( using the date and the analysises above)
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
1. define the session
2. create session query referring to station dataset
  
  @app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

  results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

## Start and End Date 
1. Create the sessions for the start and end date
  
  @app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)  

2. Using a if statement to filter on min, max, and average

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

   * Pleas note when I did try to run the API on the terminal, there was a error on few lines( line 281, line 550 and line 758) 

  
   
