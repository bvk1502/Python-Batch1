# FastAPI Clean Architecture Tutorial

This project demonstrates a complete FastAPI application using Clean Architecture principles, featuring:

- FastAPI with async support
- SQLAlchemy ORM
- PostgreSQL database
- Pydantic for data validation
- JWT Authentication
- Role-Based Access Control (RBAC)
- Clean Architecture implementation

## Project Structure

```
fastapi/
├── app/
│   ├── api/            # API routes and endpoints
│   ├── core/           # Core functionality (config, security)
│   ├── db/             # Database configuration and session
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic models/schemas
│   ├── services/       # Business logic layer
│   └── utils/          # Utility functions
├── tests/              # Test files
├── alembic/            # Database migrations
├── .env                # Environment variables
└── requirements.txt    # Project dependencies
```

## Features

- User authentication with JWT tokens
- Role-based access control
- Input validation using Pydantic
- Database migrations with Alembic
- Clean Architecture implementation
- Error handling and logging
- Environment configuration
- API documentation with Swagger UI

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## Testing

Run tests using pytest:
```bash
pytest
```

## Clean Architecture Principles

This project follows Clean Architecture principles:

1. **Entities**: Core business objects (models)
2. **Use Cases**: Application-specific business rules (services)
3. **Interface Adapters**: Convert data between use cases and external agencies (schemas)
4. **Frameworks & Drivers**: External frameworks and tools (FastAPI, SQLAlchemy)

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation
- CORS middleware
- Rate limiting
- Security headers

## Contributing

Feel free to submit issues and enhancement requests! 