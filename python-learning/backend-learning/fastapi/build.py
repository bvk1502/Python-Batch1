#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

def verify_python_environment():
    """Verify Python environment and print debug information"""
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python path: {sys.path}")
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    logger.info(f"Running in virtual environment: {in_venv}")
    if in_venv:
        logger.info(f"Virtual environment path: {sys.prefix}")

def install_requirements():
    """Install required packages if not present"""
    required_packages = [
        "alembic",
        "sqlalchemy",
        "psycopg2-binary",
        "python-dotenv"
    ]
    
    for package in required_packages:
        try:
            # Try importing the package
            __import__(package)
            logger.info(f"{package} is already installed")
        except ImportError:
            logger.info(f"Installing {package}...")
            try:
                # Use pip to install the package
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    "--no-cache-dir",  # Disable cache to ensure fresh install
                    package
                ])
                logger.info(f"Successfully installed {package}")
                
                # Verify installation
                try:
                    __import__(package)
                    logger.info(f"Verified {package} installation")
                except ImportError:
                    raise RuntimeError(f"Failed to import {package} after installation")
                    
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install {package}: {str(e)}")
                raise

def setup_environment():
    """Setup environment variables and Python path"""
    from dotenv import load_dotenv
    
    # Load environment variables
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info("Loaded environment variables from .env file")
    else:
        logger.warning(".env file not found")
    
    # Verify required environment variables
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "FIRST_SUPERUSER_EMAIL",
        "FIRST_SUPERUSER_PASSWORD"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logger.info(f"Python path set to: {PROJECT_ROOT}")

def clear_alembic_versions():
    """Clear existing alembic versions"""
    versions_dir = PROJECT_ROOT / "alembic/versions"
    if versions_dir.exists():
        logger.info("Clearing existing alembic versions...")
        for file in versions_dir.glob("*.py"):
            file.unlink()
        logger.info("Cleared existing versions")
    else:
        logger.info("No existing versions to clear")

def create_migration():
    """Create new migration"""
    logger.info("Creating new migration...")
    
    # Import models to ensure they are available to Alembic
    from app.db.base import Base  # noqa
    
    # Create versions directory if it doesn't exist
    versions_dir = PROJECT_ROOT / "alembic/versions"
    versions_dir.mkdir(parents=True, exist_ok=True)
    
    # Create alembic directory if it doesn't exist
    alembic_dir = PROJECT_ROOT / "alembic"
    alembic_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py if it doesn't exist
    init_file = alembic_dir / "__init__.py"
    if not init_file.exists():
        init_file.touch()
    
    # Use absolute path for alembic.ini
    alembic_ini_path = PROJECT_ROOT / "alembic.ini"
    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")
    
    try:
        # Import alembic modules
        import alembic
        from alembic.config import Config
        from alembic import command
        
        logger.info(f"Alembic version: {alembic.__version__}")
        
        alembic_cfg = Config(str(alembic_ini_path))
        
        command.revision(
            alembic_cfg,
            message="initial migration",
            autogenerate=True
        )
        logger.info("Created new migration")
    except ImportError as e:
        logger.error(f"Failed to import alembic: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to create migration: {str(e)}")
        raise

def apply_migration():
    """Apply migration to database"""
    logger.info("Applying migration...")
    alembic_ini_path = PROJECT_ROOT / "alembic.ini"
    
    try:
        from alembic.config import Config
        from alembic import command
        
        alembic_cfg = Config(str(alembic_ini_path))
        command.upgrade(alembic_cfg, "head")
        logger.info("Applied migration")
    except ImportError as e:
        logger.error(f"Failed to import alembic: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to apply migration: {str(e)}")
        raise

def initialize_database():
    """Initialize database with first superuser"""
    logger.info("Initializing database...")
    from app.db.session import SessionLocal
    from app.db.init_db import init_db
    
    db = SessionLocal()
    init_db(db)
    logger.info("Database initialized")

def main():
    """Main function to run all steps"""
    try:
        # Verify Python environment
        verify_python_environment()
        
        # Install required packages
        install_requirements()
        
        # Setup environment and Python path
        setup_environment()
        
        # Clear existing versions
        clear_alembic_versions()
        
        # Create new migration
        create_migration()
        
        # Apply migration
        apply_migration()
        
        # Initialize database
        initialize_database()
        
        logger.info("Build completed successfully!")
        
    except Exception as e:
        logger.error(f"Build failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()