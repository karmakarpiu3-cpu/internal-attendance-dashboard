import sqlite3

# Database Connection
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# ---------------- ATTENDANCE TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    time TEXT NOT NULL
);
""")


# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
""")


# ---------------- DEFAULT USERS ----------------
users = [
    ("admin", "admin123", "Admin"),

    ("somenath karmakar", "somenath@2006", "Intern"),
    ("koushal kashyap", "koushal@2005", "Contributor"),
    ("sougata dutta", "sougata@2005", "Team Member")
]

cursor.executemany("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES (?, ?, ?)
""", users)


# ---------------- COMMIT & CLOSE ----------------
conn.commit()
conn.close()

print("✅ Database setup completed successfully!")