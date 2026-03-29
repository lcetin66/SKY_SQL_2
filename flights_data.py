"""
This module contains the functions to query the database.   
"""
from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = ""

# Define the database URL
DATABASE_URL = "sqlite:///data/flights.sqlite3"

# Create the engine
engine = create_engine(DATABASE_URL)

def execute_query(query, params):
    """
    Execute an SQL query with the params provided in a dictionary,
    and returns a list of records (dictionary-like objects).
    If an exception was raised, print the error, and return an empty list.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return list(result)
   
    except Exception as e:
        print("Query error:", e)
        return []


def get_flight_by_id(flight_id):
    """
    Searches for flight details using flight ID.
    If the flight was found, returns a list with a single record.
    """

    query = """
    SELECT flights.*, 
        airlines.airline, 
        flights.ID as FLIGHT_ID, 
        flights.DEPARTURE_DELAY as DELAY 
    FROM flights 
    JOIN airlines ON flights.airline = airlines.id 
    WHERE flights.ID = :id
    """
    
    params = {'id': flight_id}
    return execute_query(query, params)

def get_flights_by_date(day, month, year):
    """
    Searches for flights by date (day, month, year).
    Returns a list of flights that match the date.
    """

    query = """
        SELECT flights.ID, 
            flights.ORIGIN_AIRPORT, 
            flights.DESTINATION_AIRPORT, 
            airlines.airline AS AIRLINE, 
            flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE 
            flights.DAY = :day AND 
            flights.MONTH = :month AND 
            flights.YEAR = :year
        ORDER BY 
            flights.DEPARTURE_TIME
    """
    
    params = {'day': day, 'month': month, 'year': year}
    return execute_query(query, params)

def get_delayed_flights_by_airline(airline_name):
    """
    Searches for delayed flights by airline name.
    Returns a list of delayed flights for the given airline.
    """
    
    query = """
        SELECT flights.ID, 
            flights.ORIGIN_AIRPORT, 
            flights.DESTINATION_AIRPORT, 
            airlines.airline AS AIRLINE, 
            flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE 
            airlines.airline LIKE :airline_name AND 
            flights.DEPARTURE_DELAY > 0
        ORDER BY 
            flights.DEPARTURE_DELAY DESC
    """
    
    params = {'airline_name': f"%{airline_name}%"}
    return execute_query(query, params)
    
def get_delayed_flights_by_airport(airport_code):
    """
    Searches for delayed flights by origin airport code.
    Returns a list of delayed flights for the given airport.
    """
    
    query = """
        SELECT flights.ID, 
            flights.ORIGIN_AIRPORT, 
            flights.DESTINATION_AIRPORT, 
            airlines.airline AS AIRLINE, 
            flights.DEPARTURE_DELAY AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE 
            flights.ORIGIN_AIRPORT = :airport_code AND 
            flights.DEPARTURE_DELAY > 0
        ORDER BY 
            flights.DEPARTURE_DELAY DESC
    """
    
    params = {'airport_code': airport_code}
    return execute_query(query, params)
    