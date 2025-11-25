# Lost & Found Backend

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` and update the values with your actual credentials.
    ```bash
    cp .env.example .env
    ```
    **Important**: Update `DATABASE_URL` with your MySQL connection string.

3.  **Database Migrations**:
    Run the initial migration to create the tables.
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```

4.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
