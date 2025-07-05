import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

# Try to import async_sessionmaker, fallback to sessionmaker for older SQLAlchemy
try:
    from sqlalchemy.ext.asyncio import async_sessionmaker
    ASYNC_SESSIONMAKER_AVAILABLE = True
except ImportError:
    from sqlalchemy.orm import sessionmaker
    ASYNC_SESSIONMAKER_AVAILABLE = False

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.schemas.user import UserCreate


# Test database URL - using in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for testing
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=False,
)

# Create test session factory
if ASYNC_SESSIONMAKER_AVAILABLE:
    TestingSessionLocal = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
else:
    TestingSessionLocal = sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up test database and create tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Version-agnostic approach for testing FastAPI with httpx
    try:
        # Try the newer approach first
        from httpx import ASGITransport
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac
    except (ImportError, TypeError):
        try:
            # Try the app parameter approach
            async with AsyncClient(
                app=app,
                base_url="http://test"
            ) as ac:
                yield ac
        except TypeError:
            # Fallback to basic client (this won't work for ASGI testing)
            async with AsyncClient(base_url="http://test") as ac:
                yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def test_user_create() -> UserCreate:
    """Sample UserCreate object for testing."""
    return UserCreate(
        name="Test User",
        email="test@example.com"
    )


@pytest.fixture
def test_users_data() -> list[dict]:
    """Multiple sample user data for testing."""
    return [
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"},
        {"name": "User 3", "email": "user3@example.com"},
    ]


# Configure pytest-asyncio
pytest_plugins = ["pytest_asyncio"]


# Mark all async tests with asyncio
def pytest_configure(config):
    """Configure pytest for async testing."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )


# Auto-mark async tests
def pytest_collection_modifyitems(config, items):
    """Automatically mark async test functions with asyncio marker."""
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio) 