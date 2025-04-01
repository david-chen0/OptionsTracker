import os

current_dir = os.path.dirname(os.path.abspath(__file__))
migrations_folder_name = "migrations"
migrations_file_path = os.path.join(current_dir, migrations_folder_name)

# Adding the SQL migration files sorted by name(ex: 0_init.sql comes first)
migration_files = sorted(
    [f for f in os.listdir(migrations_file_path) if f.endswith("sql") and os.path.isfile(os.path.join(migrations_file_path, f))]
)

def init_migrations_table(conn, cursor):
    """Ensure the `schema_migrations` table exists."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
        id SERIAL PRIMARY KEY,
        migration TEXT UNIQUE NOT NULL,
        applied_at TIMESTAMP DEFAULT now()
    );
    """)
    
    conn.commit()

def get_applied_migrations(cursor):
    """Fetch the list of already applied migrations."""
    cursor.execute("SELECT migration FROM schema_migrations;")
    applied_migrations = {row[0] for row in cursor.fetchall()}
    
    return applied_migrations

def apply_migrations(conn, cursor):
    """Apply new migration files in order."""
    init_migrations_table(conn, cursor)
    
    applied_migrations = get_applied_migrations(cursor)
    
    for migration_file in migration_files:
        if migration_file in applied_migrations:
            print(f"✅ {migration_file} already applied, skipping.")
            continue  # Skip already applied migrations

        print(f"🚀 Applying {migration_file}...")
        with open(os.path.join(migrations_file_path, migration_file), "r") as f:
            sql = f.read()

        try:
            cursor.execute(sql)
            cursor.execute("INSERT INTO schema_migrations (migration) VALUES (%s)", (migration_file,))
            conn.commit()
            print(f"✅ {migration_file} applied successfully.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error applying {migration_file}: {e}")
            raise e

    print("🎉 Schema Migrations complete!")
