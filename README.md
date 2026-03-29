# ✈️ Flight Database Manager

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red.svg)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-green.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based application to manage and query flight data from a SQLite database using SQLAlchemy 2.0. Users can search for flights by ID, date, airline, or airport, and export results to CSV.

## 📁 Project Structure

```text
.
├── data/
│   └── flights.sqlite3    # SQLite Database
├── flights_data.py         # Data Access Layer (SQLAlchemy)
├── main.py                # Command Line Interface (CLI)
└── README.md              # Project Documentation
```

## 🚀 Features

- **Search by ID**: Find specific flight details by its unique identifier.
- **Search by Date**: List all flights for a specific day/month/year.
- **Delayed Flights by Airline**: Find delayed flights for a specific airline.
- **Delayed Flights by Airport**: Find delayed flights originating from a specific airport (IATA code).
- **CSV Export**: Export any search results to a CSV file in `data/output/`.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <project-folder>
    ```

2.  **Install dependencies**:
    ```bash
    pip install sqlalchemy
    ```

## 📖 Usage

Run the main application:

```bash
python main.py
```

Follow the on-screen menu instructions to query the database.

## ⚖️ License

This project is licensed under the MIT License.
