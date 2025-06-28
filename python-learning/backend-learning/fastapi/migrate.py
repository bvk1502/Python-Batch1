#!/usr/bin/env python3
# migrate.py
import os
import sys
from pathlib import Path
import logging

# Get project root directory and set it in Python path BEFORE any other imports
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Now import alembic after setting up the path
from alembic.config import Config
from alembic import command

def clear_versions():
    """Clear existing alembic versions"""
    versions_dir = PROJECT_ROOT / "alembic/versions"
    if versions_dir.exists():
        for file in versions_dir.glob("*.py"):
            file.unlink()
        logger.info("Cleared existing versions")

def create_migration():
    """Create new migration"""
    logger.info("Creating new migration...")
    alembic_cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
    command.revision(
        alembic_cfg,
        message="auto migration",
        autogenerate=True
    )
    logger.info("Created new migration")

def apply_migration():
    """Apply migration to database"""
    logger.info("Applying migration...")
    alembic_cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    logger.info("Applied migration")

def main():
    """Main function to run all steps"""
    try:
        # Clear existing versions
        clear_versions()
        
        # Create new migration
        create_migration()
        
        # Apply migration
        apply_migration()
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()