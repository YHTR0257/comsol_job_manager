"""Database connection and session management for the ESP project."""

import os
from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool

from src.config.loader import get_logger
from src.data.models.base import Base

log = get_logger(__name__)


class DatabaseConfig:
    """Database configuration manager."""

    def __init__(
        self,
        database_url: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        echo: bool = False,
    ):
        """
        Initialize database configuration.

        Args:
            database_url: Database connection URL. If None, reads from DATABASE_URL env var
            pool_size: Connection pool size (default: 5)
            max_overflow: Maximum overflow connections (default: 10)
            pool_timeout: Connection timeout in seconds (default: 30)
            echo: Echo SQL statements (default: False)
        """
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError(
                "Database URL not provided. Set DATABASE_URL environment variable "
                "or pass database_url parameter."
            )

        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.echo = echo

        # Detect database type
        self.is_sqlite = self.database_url.startswith('sqlite')

    def create_engine_config(self) -> dict:
        """Create engine configuration based on database type."""
        config = {
            'echo': self.echo,
            'future': True,  # Use SQLAlchemy 2.0 style
        }

        if self.is_sqlite:
            # SQLite specific configuration
            config['poolclass'] = NullPool  # Disable pooling for SQLite
            config['connect_args'] = {'check_same_thread': False}
        else:
            # PostgreSQL/MySQL configuration
            config['pool_size'] = self.pool_size
            config['max_overflow'] = self.max_overflow
            config['pool_timeout'] = self.pool_timeout
            config['poolclass'] = QueuePool
            config['pool_pre_ping'] = True  # Verify connections before using

        return config


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize database manager.

        Args:
            config: Database configuration
        """
        self.config = config
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None

    def initialize(self) -> None:
        """Initialize database engine and session factory."""
        if self.engine is not None:
            log.warning("Database already initialized")
            return

        log.info(f"Initializing database connection: {self._mask_url(self.config.database_url)}")

        engine_config = self.config.create_engine_config()
        self.engine = create_engine(self.config.database_url, **engine_config)

        # Add SQLite specific optimizations
        if self.config.is_sqlite:
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.close()

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        log.info("Database initialized successfully")

    def create_tables(self) -> None:
        """Create all tables defined in models."""
        if self.engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        log.info("Creating database tables...")
        Base.metadata.create_all(bind=self.engine)
        log.info("Tables created successfully")

    def drop_tables(self) -> None:
        """Drop all tables. Use with caution!"""
        if self.engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        log.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=self.engine)
        log.info("Tables dropped")

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy session

        Note:
            Caller is responsible for closing the session.
        """
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope around a series of operations.

        Yields:
            SQLAlchemy session

        Example:
            with db_manager.session_scope() as session:
                session.add(material)
                # Automatically commits on success, rolls back on exception
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            log.error(f"Database transaction failed: {e}")
            raise
        finally:
            session.close()

    def close(self) -> None:
        """Close database connections and dispose engine."""
        if self.engine is not None:
            log.info("Closing database connections...")
            self.engine.dispose()
            self.engine = None
            self.SessionLocal = None
            log.info("Database connections closed")

    @staticmethod
    def _mask_url(url: str) -> str:
        """Mask password in database URL for logging."""
        if '@' in url:
            # Format: scheme://user:password@host/db
            parts = url.split('@')
            credentials = parts[0].split('://')
            if len(credentials) == 2 and ':' in credentials[1]:
                user = credentials[1].split(':')[0]
                return f"{credentials[0]}://{user}:****@{parts[1]}"
        return url


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(config: Optional[DatabaseConfig] = None) -> DatabaseManager:
    """
    Get or create global database manager instance.

    Args:
        config: Database configuration. If None, creates from environment variables

    Returns:
        DatabaseManager instance
    """
    global _db_manager

    if _db_manager is None:
        if config is None:
            config = DatabaseConfig()
        _db_manager = DatabaseManager(config)
        _db_manager.initialize()

    return _db_manager


def get_session() -> Session:
    """
    Get a new database session from the global manager.

    Returns:
        SQLAlchemy session

    Note:
        Caller is responsible for closing the session.
    """
    return get_db_manager().get_session()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Provide a transactional scope using the global database manager.

    Yields:
        SQLAlchemy session

    Example:
        with session_scope() as session:
            material = MaterialSystem(name='Al', formula='Al')
            session.add(material)
    """
    db_manager = get_db_manager()
    with db_manager.session_scope() as session:
        yield session


def init_db(database_url: Optional[str] = None, create_tables: bool = True) -> DatabaseManager:
    """
    Initialize database with optional table creation.

    Args:
        database_url: Database connection URL
        create_tables: Whether to create tables (default: True)

    Returns:
        DatabaseManager instance
    """
    config = DatabaseConfig(database_url=database_url)
    db_manager = DatabaseManager(config)
    db_manager.initialize()

    if create_tables:
        db_manager.create_tables()

    return db_manager