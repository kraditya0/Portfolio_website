import sqlite3
import os
from datetime import datetime

# Use /tmp on Vercel (read-only filesystem), local path otherwise
if os.environ.get('VERCEL'):
    DATABASE = '/tmp/database.db'
else:
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with all required tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            github_link TEXT,
            live_link TEXT,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Services table (kept for API compatibility)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT DEFAULT 'bi-code-slash',
            price_range TEXT
        )
    ''')

    # Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            percentage INTEGER NOT NULL DEFAULT 50,
            category TEXT DEFAULT 'Technical'
        )
    ''')

    # Testimonials table (auto-approved, no admin needed)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT DEFAULT '',
            rating INTEGER NOT NULL DEFAULT 5,
            feedback TEXT NOT NULL,
            approved INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


# ─── Project CRUD ───────────────────────────────────────────

def get_all_projects():
    conn = get_db()
    projects = conn.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
    conn.close()
    return projects


def get_project(project_id):
    conn = get_db()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    conn.close()
    return project


def add_project(title, description, tech_stack, github_link, live_link, image):
    conn = get_db()
    conn.execute(
        'INSERT INTO projects (title, description, tech_stack, github_link, live_link, image) VALUES (?, ?, ?, ?, ?, ?)',
        (title, description, tech_stack, github_link, live_link, image)
    )
    conn.commit()
    conn.close()


# ─── Service Read ───────────────────────────────────────────

def get_all_services():
    conn = get_db()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    return services


def add_service(title, description, icon, price_range):
    conn = get_db()
    conn.execute(
        'INSERT INTO services (title, description, icon, price_range) VALUES (?, ?, ?, ?)',
        (title, description, icon, price_range)
    )
    conn.commit()
    conn.close()


# ─── Skills Read ────────────────────────────────────────────

def get_all_skills():
    conn = get_db()
    skills = conn.execute('SELECT * FROM skills ORDER BY percentage DESC').fetchall()
    conn.close()
    return skills


def add_skill(name, percentage, category='Technical'):
    conn = get_db()
    conn.execute(
        'INSERT INTO skills (name, percentage, category) VALUES (?, ?, ?)',
        (name, percentage, category)
    )
    conn.commit()
    conn.close()


# ─── Testimonials ───────────────────────────────────────────

def get_approved_testimonials():
    conn = get_db()
    testimonials = conn.execute('SELECT * FROM testimonials WHERE approved = 1 ORDER BY created_at DESC').fetchall()
    conn.close()
    return testimonials


def add_testimonial(name, role, rating, feedback):
    """Add a testimonial — auto-approved (no admin review needed)."""
    conn = get_db()
    conn.execute(
        'INSERT INTO testimonials (name, role, rating, feedback, approved) VALUES (?, ?, ?, ?, 1)',
        (name, role, rating, feedback)
    )
    conn.commit()
    conn.close()
