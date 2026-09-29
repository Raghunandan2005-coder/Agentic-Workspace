# Appointment Booking System - Project Requirements

## Project Overview

Build a small, local appointment booking system for a clinic or medical practice. The system supports patient registration, doctor profiles, doctor availability, appointment booking, cancellation, appointment history, and an administrator dashboard.

## Requirements

### Patient Features
- Patient registration with email, name, phone
- View available slots for a doctor
- Book an available slot
- Cancel eligible appointments
- View appointment history

### Doctor Features
- Doctor profiles with name, specialty, phone
- View doctor availability (slots)

### Appointment Features
- Book appointments with validation
- Cancel appointments (status changes to cancelled)
- Cancelled appointments remain in history

### Administrator Features
- Dashboard with basic counts (total appointments, active, cancelled)

### Critical Business Rules
1. Only available/unoccupied slots can be booked
2. Duplicate booking is prevented (same doctor + same slot = only one active appointment)
3. Cancelled appointments remain in history
4. Data persists across restart

### Validation Requirements
- Validate patient, doctor, slot existence
- Validate slot availability
- Handle validation/error states
- Automated tests must pass

## Tech Stack
- Python
- FastAPI (API framework)
- SQLAlchemy (ORM)
- SQLite (database)
- Pydantic (validation)
- Uvicorn (ASGI server)