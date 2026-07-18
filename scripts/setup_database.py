import os
import sys
import subprocess
from sqlalchemy import create_engine, text

# Add project root to sys.path
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config.settings import settings

def verify_connection() -> bool:
    print(f"[INFO] Connecting to database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'local'}")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[SUCCESS] Database connectivity verified.")
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False

def run_migrations() -> bool:
    print("[INFO] Running Alembic migrations to upgrade to head...")
    try:
        res = subprocess.run(["python", "-m", "alembic", "upgrade", "head"], cwd=PROJECT_ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            print("[SUCCESS] Alembic migrations upgraded to head successfully.")
            return True
        else:
            print(f"[ERROR] Migration failed:\n{res.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to run migration process: {e}")
        return False

if __name__ == "__main__":
    print("--- HydroGrow AI Production Database Setup ---")
    if verify_connection():
        run_migrations()
    else:
        sys.exit(1)
