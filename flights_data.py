"""
This module contains the functions to query the database.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Connect to the database
# Make sure the flights.sqlite file is in the 'data' directory
engine = create_engine("sqlite:///data/flights.sqlite")

def get_delayed_flights_by_airline(airline_input):
    """
    Returns a list of dictionaries with delayed flights for a given airline.
    """
    query = text("""
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT,
        airlines.AIRLINE, flights.DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE airlines.AIRLINE LIKE :airline AND flights.DELAY > 0
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"airline": f"%{airline_input}%"})
            return result.mappings().all()
    except SQLAlchemyError as e:  # W0718 düzeltildi
        print(f"Database error: {e}")
        return []

def get_delayed_flights_by_airport(airport_input):
    """
    Returns a list of dictionaries with delayed flights for a given airport.
    """
    query = text("""
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT,
        airlines.AIRLINE, flights.DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.ORIGIN_AIRPORT = :airport AND flights.DELAY > 0
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"airport": airport_input})
            return result.mappings().all()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []

def get_flight_by_id(flight_id):
    """
    Returns a list containing one dictionary for a flight with the given ID.
    """
    query = text("""
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT,
        airlines.AIRLINE, flights.DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.ID = :id
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"id": flight_id})
            return result.mappings().all()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []

def get_flights_by_date(day, month, year):
    """
    Returns a list of dictionaries for flights on a specific date.
    """
    query = text("""
        SELECT flights.ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT,
        airlines.AIRLINE, flights.DELAY
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year
    """)
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {
                "day": day,
                "month": month,
                "year": year
            })
            return result.mappings().all()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []
