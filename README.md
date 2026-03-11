# Pharmacy Management System

This project is a desktop pharmacy operations application built with Python, Tkinter, SQLAlchemy, and MySQL. It is designed to help a pharmacy manage day-to-day work such as medicine inventory, sales recording, patient tracking, reporting, alerts, and staff access control from a single graphical interface.

## Project Definition

The system provides a role-based pharmacy dashboard where managers and staff sign in and work with the parts of the system relevant to their responsibilities.

- Staff users can handle sales and patient-related workflows.
- Manager users can additionally manage inventory, view reports, monitor alerts, and manage staff accounts.

The application follows a modular design. The main dashboard coordinates several feature-specific modules, while the database layer uses SQLAlchemy models backed by a MySQL database.

## Core Features

- Secure login with role-based access
- Medicine inventory and stock entry management
- Sales recording and sale item tracking
- Patient registration and history tracking
- Reporting for pharmacy operations
- Alerts for stock and medicine expiry conditions
- Staff account management for managers

## How The Project Is Organized

- main.py: starts the application and opens the home/login flow
- pharmacy.py: main dashboard window and module integration
- loginpage.py: login form and authentication flow
- homepg.py: landing screen
- inventory.py: inventory and stock-related features
- sales.py: sales workflow
- patients.py: patient management
- reports.py: reporting features
- alert.py: alert-related views
- users.py: staff management
- models.py: SQLAlchemy data models
- connector.py: database connection settings
- db.py: database table creation/reset script
- admin.py: seed script for default users
- db_tables/: SQL reference scripts for database tables

## Data Model

The application is centered around these core entities:

- User: stores usernames, passwords, and roles
- Medicine: stores medicine details, price, quantity, type, and expiry date
- Patient: stores patient identity and medical history
- Sale: records a transaction linked to a patient
- SaleItem: stores line items for each sale
- StockEntry: tracks added medicine stock over time

## Intended Use

This project is suitable as:

- A school or university pharmacy management system project
- A learning project for Tkinter, SQLAlchemy, and MySQL integration
- A base application that can be extended with billing, prescriptions, audit logs, or analytics

## Requirements

- Python 3.10 or newer recommended
- MySQL server
- Required Python packages:

```bash
pip install sqlalchemy mysql-connector-python pymysql pillow
```

## Database Setup

Database settings are read from environment variables in connector.py.

Default values:

- DB_HOST=localhost
- DB_PORT=3307
- DB_USER=root
- DB_PASSWORD=Aruserver@123
- DB_NAME=pharmacy

After configuring the database, initialize the schema and seed default accounts:

```bash
python db.py
python admin.py
```

Default users:

- Manager: admin / admin123
- Staff: staff1 / 1234

## Run The Project

```bash
python main.py
```

## Notes

- The interface is built with Tkinter and intended for desktop use.
- The project mixes a GUI layer with feature mixins to keep responsibilities separated by module.
- SQL scripts in db_tables/ can be used as a reference for the database structure.
