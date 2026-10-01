import sqlite3


DATABASE_NAME = "internships.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            url TEXT UNIQUE,
            gpa_status TEXT,
            position_type TEXT,
            tech_position INTEGER,
            term TEXT,
            eligible INTEGER,
            needs_review INTEGER,
            status TEXT,
            date_found TEXT
        )
    """)

    connection.commit()
    connection.close()


def job_exists(url):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM jobs WHERE url = ?",
        (url,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def save_job(job, result):
    if job_exists(job.url):
        return False

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            title,
            company,
            location,
            description,
            url,
            gpa_status,
            position_type,
            tech_position,
            term,
            eligible,
            needs_review,
            status,
            date_found
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        job.title,
        job.company,
        job.location,
        job.description,
        job.url,
        result["gpa"],
        result["position_type"],
        int(result["tech_position"]),
        result["term"],
        int(result["eligible"]),
        int(result["needs_review"]),
        result["status"],
    ))

    connection.commit()
    connection.close()

    return True


def get_eligible_jobs():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            title,
            company,
            location,
            url,
            gpa_status,
            position_type,
            term
        FROM jobs
        WHERE eligible = 1
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    connection.close()

    return jobs


def get_review_jobs():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            title,
            company,
            location,
            url,
            gpa_status,
            position_type,
            term
        FROM jobs
        WHERE needs_review = 1
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    connection.close()

    return jobs


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")