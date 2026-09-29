# Appointment Booking System

A local appointment booking system for a clinic or medical practice. Supports patient registration, doctor profiles, doctor availability, appointment booking, cancellation, appointment history, and an administrator dashboard.

## Project Structure

```
appointment-booking-system/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services/appointments.py
│   └── routes/
│       ├── patients.py
│       ├── doctors.py
│       ├── appointments.py
│       └── admin.py
├── tests/
│   ├── test_patients.py
│   ├── test_doctors.py
│   ├── test_appointments.py
│   └── test_booking_conflicts.py
├── frontend/
├── requirements.txt
├── README.md
└── project_requirements.md
```

## Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Access the API:
   - API docs: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health

## Features

- Patient registration and management
- Doctor profiles with specialties
- Slot management for doctor availability
- Appointment booking with duplicate booking prevention
- Appointment cancellation with history retention
- Administrator dashboard with appointment counts

## Duplicate-Booking Prevention

The system enforces a critical duplicate-booking rule: the same doctor and appointment slot must never be successfully assigned to two active appointments. This is enforced at both the application level (business logic) and database level (foreign key constraints). Two competing booking attempts will result in at most one active appointment, with the losing request rejected safely and without a partial record.