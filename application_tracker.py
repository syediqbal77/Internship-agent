import sqlite3
from datetime import datetime


DATABASE_NAME = "internships.db"


STATUSES = [
    "INTERESTED",
    "SAVED",
    "APPLYING",
    "APPLIED",
    "INTERVIEW",
    "OFFER",
    "REJECTED",
    "WITHDRAWN",
]


def connect():
    return sqlite3.connect(DATABASE_NAME)


def create_application_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_id INTEGER NOT NULL,

            status TEXT NOT NULL DEFAULT 'INTERESTED',

            date_added TEXT,

            date_applied TEXT,

            notes TEXT,

            FOREIGN KEY (job_id)
                REFERENCES jobs(id)
        )
    """)

    connection.commit()
    connection.close()


def get_job(job_id):
    connection = connect()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            url,
            position_type,
            term
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    job = cursor.fetchone()

    connection.close()

    return job


def add_application(job_id, status="INTERESTED", notes=""):
    job = get_job(job_id)

    if job is None:
        print()
        print(f"Job ID {job_id} was not found.")
        return

    if status not in STATUSES:
        print()
        print("Invalid status.")
        print()
        print("Valid statuses:")

        for item in STATUSES:
            print(f"  {item}")

        return

    connection = connect()
    cursor = connection.cursor()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    date_applied = None

    if status == "APPLIED":
        date_applied = now

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE job_id = ?
    """, (job_id,))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE applications
            SET
                status = ?,
                notes = ?,
                date_applied = ?
            WHERE job_id = ?
        """, (
            status,
            notes,
            date_applied,
            job_id
        ))

        print()
        print("Application updated.")

    else:

        cursor.execute("""
            INSERT INTO applications (
                job_id,
                status,
                date_added,
                date_applied,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            job_id,
            status,
            now,
            date_applied,
            notes
        ))

        print()
        print("Application added.")

    connection.commit()
    connection.close()

    print()
    print(f"Job: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Status: {status}")


def update_status(job_id, status):
    if status not in STATUSES:
        print()
        print("Invalid status.")

        return

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM applications
        WHERE job_id = ?
    """, (job_id,))

    existing = cursor.fetchone()

    if not existing:
        print()
        print(
            "This job is not currently being tracked."
        )

        connection.close()

        return

    date_applied = None

    if status == "APPLIED":
        date_applied = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    cursor.execute("""
        UPDATE applications
        SET
            status = ?,
            date_applied = COALESCE(
                ?,
                date_applied
            )
        WHERE job_id = ?
    """, (
        status,
        date_applied,
        job_id
    ))

    connection.commit()
    connection.close()

    print()
    print(
        f"Application status updated to {status}."
    )


def get_applications():
    connection = connect()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.id,
            applications.job_id,
            applications.status,
            applications.date_added,
            applications.date_applied,
            applications.notes,

            jobs.title,
            jobs.company,
            jobs.location,
            jobs.url,
            jobs.position_type,
            jobs.term

        FROM applications

        JOIN jobs
            ON applications.job_id = jobs.id

        ORDER BY
            applications.date_added DESC
    """)

    applications = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return applications


def print_applications():
    applications = get_applications()

    print()
    print("=" * 75)
    print("INTERNSHIP APPLICATION TRACKER")
    print("=" * 75)

    if not applications:
        print()
        print("No applications are being tracked yet.")
        print()
        print(
            "Use add_application() to add one."
        )

        return

    for application in applications:

        print()
        print("-" * 75)

        print(
            f"Job ID: "
            f"{application['job_id']}"
        )

        print(
            f"Title: "
            f"{application['title']}"
        )

        print(
            f"Company: "
            f"{application['company']}"
        )

        print(
            f"Location: "
            f"{application['location']}"
        )

        print(
            f"Type: "
            f"{application['position_type']}"
        )

        print(
            f"Term: "
            f"{application['term']}"
        )

        print(
            f"Status: "
            f"{application['status']}"
        )

        print(
            f"Added: "
            f"{application['date_added']}"
        )

        if application["date_applied"]:
            print(
                f"Applied: "
                f"{application['date_applied']}"
            )

        if application["notes"]:
            print(
                f"Notes: "
                f"{application['notes']}"
            )

        print(
            f"URL: "
            f"{application['url']}"
        )


def print_statistics():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*)
        FROM applications
        GROUP BY status
    """)

    rows = cursor.fetchall()

    connection.close()

    counts = {
        status: 0
        for status in STATUSES
    }

    for status, count in rows:
        counts[status] = count

    print()
    print("=" * 50)
    print("APPLICATION STATISTICS")
    print("=" * 50)

    for status in STATUSES:
        print(
            f"{status:<15} "
            f"{counts[status]}"
        )

    print("=" * 50)


def main():
    create_application_table()

    print()
    print("Application tracker is ready.")

    print_statistics()

    print_applications()


if __name__ == "__main__":
    main()