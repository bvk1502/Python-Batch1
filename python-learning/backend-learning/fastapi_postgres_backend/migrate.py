import os
import shutil
from pathlib import Path
import subprocess
import sys
from sqlalchemy import create_engine, text, inspect
from app.core.config import settings
from app.db.base import Base  # Import Base here to check metadata

def run_command(command):
    """Run a shell command and print its output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True
    )
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    if process.returncode != 0:
        print(f"Command failed with return code {process.returncode}")
        sys.exit(1)

def delete_alembic_version_table():
    """Delete the alembic_version table from the database"""
    print("\nStep 0: Deleting alembic_version table...")
    # Convert async URL to sync URL for migrations
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    
    try:
        # Create engine and connect to database
        engine = create_engine(sync_url)
        with engine.connect() as connection:
            # Drop the alembic_version table if it exists
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
            connection.commit()
        print("✓ Deleted alembic_version table")
    except Exception as e:
        print(f"Error deleting alembic_version table: {e}")
        sys.exit(1)

def check_tables():
    """Check what tables exist in the database"""
    print("\nChecking database tables...")
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Print debug information
    print("\nDebug Information:")
    print(f"Base metadata tables: {Base.metadata.tables.keys()}")
    
    # Path to versions directory
    versions_dir = project_root / "alembic" / "versions"
    
    # Step 0: Delete alembic_version table
    delete_alembic_version_table()
    
    # Step 1: Remove existing versions
    print("\nStep 1: Removing existing versions...")
    if versions_dir.exists():
        shutil.rmtree(versions_dir)
        print("✓ Removed existing versions")
    else:
        print("✓ No existing versions found")
    
    # Create versions directory if it doesn't exist
    versions_dir.mkdir(exist_ok=True)
    
    # Step 2: Create new migration
    print("\nStep 2: Creating new migration...")
    run_command("alembic revision --autogenerate -m 'initial migration'")
    
    # Step 3: Apply migration
    print("\nStep 3: Applying migration...")
    run_command("alembic upgrade head")
    
    # Step 4: Check tables after migration
    check_tables()
    
    print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    main()
