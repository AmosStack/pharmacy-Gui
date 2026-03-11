# Pharmacy Management System - OOP Implementation Guide

This document explains how Object-Oriented Programming (OOP) is implemented in this project using the four pillars:

- Inheritance
- Polymorphism
- Encapsulation
- Abstraction

---

## 1) Inheritance

Inheritance is primarily used through mixins and Tkinter class hierarchies.

### a) Main app with multiple inheritance
In `pharmacy.py`, `PharmacyApp` inherits from multiple mixin classes:

- `InventoryMixin`
- `UserMixin`
- `SalesMixin`
- `PatientMixin`
- `ReportsMixin`
- `AlertMixin`

This allows `PharmacyApp` to reuse and combine feature-specific behavior from separate modules.

### b) UI class inheritance from Tkinter base classes
- `Homepage` inherits from `tk.Frame` (`homepg.py`)
- `LoginPage` inherits from `tk.Frame` (`loginpage.py`)
- `LoginForm` inherits from `ttk.Frame` (`loginpage.py`)

These classes inherit standard widget behavior and extend it with project-specific UI logic.

---

## 2) Polymorphism

Polymorphism appears through dynamic method dispatch and duck typing.

### a) Runtime-selected tab builders
In `PharmacyApp`, `_tab_builders` maps tab keys to different build methods (`build_sales_tab`, `build_inventory_tab`, etc.).

The `_show_tab` method calls whichever builder is selected at runtime, and each builder has the same callable interface but different behavior depending on the feature module.

### b) Duck typing with optional behavior
In several places, code checks for method existence before calling:

- `hasattr(self, "load_medicines_for_sale")`
- `hasattr(self, "load_patients_for_sale")`

This means objects are used based on supported behavior, not strict type checks.

### c) Cursor proxy behavior
`_CursorProxy` in `pharmacy.py` supports both:

- callable style (`self.db.cursor(dictionary=True)`)
- direct cursor-like attribute access (delegated via `__getattr__`)

This is a flexible polymorphic adapter pattern.

---

## 3) Encapsulation

Encapsulation is used by grouping data and behavior inside classes and restricting direct access by convention.

### a) Internal state in helper classes
`_CursorProxy` and `_LegacyDBAdapter` keep internal connection details in attributes like:

- `_connection`
- `_default_cursor`

These internals are hidden from other modules behind methods like `commit()` and `rollback()`.

### b) App state management in `PharmacyApp`
`PharmacyApp` encapsulates global application state such as:

- DB session/connection (`session`, `conn`, `cursor`, `db`)
- user context (`role`, `username`)
- UI state (`_tab_builders`, `_built_tabs`)

### c) Feature-level encapsulation in mixins
Each mixin owns its own UI components and feature logic:

- inventory logic in `inventory.py`
- sales logic in `sales.py`
- patient logic in `patients.py`
- reports logic in `reports.py`
- staff logic in `users.py`

---

## 4) Abstraction

Abstraction is implemented by exposing simple interfaces while hiding low-level details.

### a) Database adapter abstraction
`_LegacyDBAdapter` abstracts DB operations into a small interface:

- `cursor`
- `commit()`
- `rollback()`

Feature modules can use DB actions without handling raw connection complexity everywhere.

### b) Centralized DB configuration
`connector.py` abstracts environment-based DB setup by providing:

- `DATABASE_URL`
- `engine`
- `SessionLocal`
- `Base`

This keeps DB configuration in one place.

### c) Modular feature abstraction via mixins
Each mixin exposes high-level operations (example: `build_inventory_tab()`, `generate_report()`, `add_patient()`) and hides implementation details internally.

---

## Summary

The project uses OOP effectively in a modular way:

- **Inheritance** organizes code reuse through mixins and UI base classes.
- **Polymorphism** enables runtime behavior selection and duck-typed method use.
- **Encapsulation** keeps state and logic grouped in focused classes.
- **Abstraction** simplifies complex systems (DB + UI features) behind clean interfaces.

This structure makes the system easier to maintain, extend, and test feature-by-feature.
