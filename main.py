"""
This module contains the functions to query the database.
"""
import csv
import os
from datetime import datetime
import sqlalchemy
import flights_data


IATA_LENGTH = 3

def delayed_flights_by_airline():
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("Enter airline name: ")
    results = flights_data.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport():
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_airport".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Validate input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = flights_data.get_delayed_flights_by_airport(airport_input)
    print_results(results)

def flight_by_id():
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except ValueError:
            print("Try again... Please enter a number.")
        else:
            valid = True
    results = flights_data.get_flight_by_id(id_input)
    print_results(results)

def flights_by_date():
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = flights_data.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)

def print_results(results):
    """
    Get a list of flight results (List of dictionary-like objects from SQLAachemy).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    """
    print(f"Got {len(results)} results.")
    for result in results:

        # Check that all required columns are in place
        try:
            # If delay columns is NULL, set it to 0
            delay = int(result['DELAY']) if result['DELAY'] else 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")

    export_choice = input("\nWould you like to export this data to a CSV file? (y/n)\n")

    if export_choice.lower() == "y":
        filename = input("Enter a filename (e.g. delayed_flights.csv): ")
        if filename == "":
            filename = "delayed_flights.csv"
        if not filename.endswith(".csv"):
            filename += ".csv"
        export_to_csv(results, filename)
    else:
        return

def export_to_csv(results, filename):
    """
    Export the results to a CSV file.
    """
    if not os.path.exists("data/output"):
        os.makedirs("data/output")

    with open(f"data/output/{filename}", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "ID",
            "ORIGIN_AIRPORT",
            "DESTINATION_AIRPORT",
            "AIRLINE",
            "DELAY"
        ])
        for result in results:
            writer.writerow([
                result['ID'],
                result['ORIGIN_AIRPORT'],
                result['DESTINATION_AIRPORT'],
                result['AIRLINE'],
                result['DELAY']
            ])

    print(f"Data exported to {filename}")

def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError:
            pass
        print("Try again...")

FUNCTIONS = { 1: (flight_by_id, "Show flight by ID"),
              2: (flights_by_date, "Show flights by date"),
              3: (delayed_flights_by_airline, "Delayed flights by airline"),
              4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
              5: (quit, "Exit")
             }

def main():
    """ Runs the main menu loop of the application. """
    # The Main Menu loop
    while True:
        choice_func= show_menu_and_get_input()
        choice_func()


if __name__ == "__main__":
    main()
