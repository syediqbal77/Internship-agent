import sqlite3

from resume_matcher import (
    extract_resume_text,
    find_resume_skills
)

from resume_job_matcher import (
    get_jobs,
    rank_jobs
)

from application_tracker import (
    create_application_table,
    add_application,
    update_status,
    get_applications,
    print_statistics,
    STATUSES
)


DATABASE_NAME = "internships.db"


# ---------------------------------------------------------
# Database helper
# ---------------------------------------------------------

def get_job_by_id(job_id):
    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    job = cursor.fetchone()

    connection.close()

    return job


# ---------------------------------------------------------
# Resume
# ---------------------------------------------------------

def load_resume():

    try:

        resume_text = extract_resume_text()

    except Exception as error:

        print()
        print(
            f"Could not read resume: {error}"
        )

        return []


    if not resume_text.strip():

        print()
        print(
            "No text could be extracted "
            "from resume.pdf."
        )

        return []


    skills = find_resume_skills(
        resume_text
    )


    print()
    print(
        f"Detected {len(skills)} "
        "skills from your resume."
    )


    return skills


# ---------------------------------------------------------
# Show resume matches
# ---------------------------------------------------------

def show_matches():

    print()
    print("=" * 75)
    print("FINDING BEST INTERNSHIP MATCHES")
    print("=" * 75)


    resume_skills = load_resume()


    if not resume_skills:

        print()
        print(
            "No resume skills were detected."
        )

        return


    jobs = get_jobs()


    print()

    print(
        f"Checking {len(jobs)} jobs..."
    )


    results = rank_jobs(
        jobs,
        resume_skills
    )


    if not results:

        print()
        print(
            "No jobs found."
        )

        return


    print()
    print("=" * 75)
    print("TOP MATCHES")
    print("=" * 75)


    for number, job in enumerate(
        results[:20],
        start=1
    ):

        print()

        print(
            f"{number}. "
            f"{job['title']}"
        )

        print(
            f"   Company: "
            f"{job['company']}"
        )

        print(
            f"   Location: "
            f"{job['location']}"
        )

        print(
            f"   Match: "
            f"{job['score']}%"
        )

        print(
            f"   Type: "
            f"{job['position_type']}"
        )

        print(
            f"   Term: "
            f"{job['term']}"
        )

        print(
            f"   GPA: "
            f"{job['gpa_status']}"
        )


    print()

    print(
        "Enter a number to view the job."
    )

    print(
        "Press ENTER to return."
    )


    choice = input(
        "\nChoice: "
    ).strip()


    if not choice:

        return


    try:

        number = int(choice)

        if number < 1 or number > min(
            20,
            len(results)
        ):

            print(
                "Invalid selection."
            )

            return

    except ValueError:

        print(
            "Please enter a number."
        )

        return


    job = results[number - 1]


    show_job_details(job)


# ---------------------------------------------------------
# Show job details
# ---------------------------------------------------------

def show_job_details(job):

    print()
    print("=" * 75)

    print(
        job["title"]
    )

    print("=" * 75)

    print(
        f"Company: {job['company']}"
    )

    print(
        f"Location: {job['location']}"
    )

    print(
        f"Type: {job['position_type']}"
    )

    print(
        f"Term: {job['term']}"
    )

    print(
        f"GPA: {job['gpa_status']}"
    )

    print(
        f"Match score: {job['score']}%"
    )

    print()

    print(
        "Matched skills:"
    )


    if job["matched_skills"]:

        for skill in job[
            "matched_skills"
        ]:

            print(
                f"  ✓ {skill}"
            )

    else:

        print(
            "  None"
        )


    print()

    print(
        "Missing skills:"
    )


    if job["missing_skills"]:

        for skill in job[
            "missing_skills"
        ][:15]:

            print(
                f"  ○ {skill}"
            )

    else:

        print(
            "  None detected"
        )


    print()

    print(
        "Why it matched:"
    )


    if job["reasons"]:

        for reason in job[
            "reasons"
        ]:

            print(
                f"  + {reason}"
            )

    else:

        print(
            "  No additional reasons"
        )


    print()

    print(
        f"Apply URL:"
    )

    print(
        job["url"]
    )


    print()

    print(
        "1. Add to tracker"
    )

    print(
        "2. Open application URL"
    )

    print(
        "3. Return"
    )


    choice = input(
        "\nChoice: "
    ).strip()


    if choice == "1":

        tracker_add_job(
            job
        )

    elif choice == "2":

        print()

        print(
            "Copy the URL above into "
            "your browser."
        )

        input(
            "\nPress ENTER to continue..."
        )


# ---------------------------------------------------------
# Add job to tracker
# ---------------------------------------------------------

def tracker_add_job(job):

    print()

    print(
        "Choose status:"
    )


    for number, status in enumerate(
        STATUSES,
        start=1
    ):

        print(
            f"{number}. {status}"
        )


    choice = input(
        "\nStatus: "
    ).strip()


    try:

        status_number = int(
            choice
        )

        if (
            status_number < 1
            or status_number > len(STATUSES)
        ):

            print(
                "Invalid status."
            )

            return

    except ValueError:

        print(
            "Please enter a number."
        )

        return


    status = STATUSES[
        status_number - 1
    ]


    notes = input(
        "Notes (optional): "
    ).strip()


    add_application(
        job["id"],
        status,
        notes
    )


    input(
        "\nPress ENTER to continue..."
    )


# ---------------------------------------------------------
# View applications
# ---------------------------------------------------------

def view_applications():

    applications = get_applications()


    print()

    print("=" * 75)

    print(
        "YOUR APPLICATIONS"
    )

    print("=" * 75)


    if not applications:

        print()

        print(
            "You aren't tracking "
            "any applications yet."
        )

        input(
            "\nPress ENTER to continue..."
        )

        return


    for number, application in enumerate(
        applications,
        start=1
    ):

        print()

        print(
            f"{number}. "
            f"{application['title']}"
        )

        print(
            f"   Company: "
            f"{application['company']}"
        )

        print(
            f"   Status: "
            f"{application['status']}"
        )

        print(
            f"   Location: "
            f"{application['location']}"
        )

        print(
            f"   Term: "
            f"{application['term']}"
        )

        if application[
            "date_applied"
        ]:

            print(
                f"   Applied: "
                f"{application['date_applied']}"
            )


    print()

    print(
        "Enter an application number "
        "to change its status."
    )

    print(
        "Press ENTER to return."
    )


    choice = input(
        "\nChoice: "
    ).strip()


    if not choice:

        return


    try:

        number = int(choice)

        if (
            number < 1
            or number > len(applications)
        ):

            print(
                "Invalid selection."
            )

            return

    except ValueError:

        print(
            "Please enter a number."
        )

        return


    application = applications[
        number - 1
    ]


    change_application_status(
        application
    )


# ---------------------------------------------------------
# Change application status
# ---------------------------------------------------------

def change_application_status(
    application
):

    print()

    print(
        f"Current status: "
        f"{application['status']}"
    )

    print()

    print(
        "Choose new status:"
    )


    for number, status in enumerate(
        STATUSES,
        start=1
    ):

        print(
            f"{number}. {status}"
        )


    choice = input(
        "\nStatus: "
    ).strip()


    try:

        number = int(choice)

        if (
            number < 1
            or number > len(STATUSES)
        ):

            print(
                "Invalid selection."
            )

            return

    except ValueError:

        print(
            "Please enter a number."
        )

        return


    new_status = STATUSES[
        number - 1
    ]


    update_status(
        application["job_id"],
        new_status
    )


    input(
        "\nPress ENTER to continue..."
    )


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

def show_statistics():

    print_statistics()

    input(
        "\nPress ENTER to continue..."
    )


# ---------------------------------------------------------
# Main menu
# ---------------------------------------------------------

def main():

    create_application_table()


    while True:

        print()

        print("=" * 75)

        print(
            "INTERNSHIP AGENT"
        )

        print("=" * 75)

        print()

        print(
            "1. Find my best internship matches"
        )

        print(
            "2. View my applications"
        )

        print(
            "3. View application statistics"
        )

        print(
            "4. Exit"
        )

        print()


        choice = input(
            "Choose an option: "
        ).strip()


        if choice == "1":

            show_matches()


        elif choice == "2":

            view_applications()


        elif choice == "3":

            show_statistics()


        elif choice == "4":

            print()

            print(
                "Goodbye."
            )

            break


        else:

            print()

            print(
                "Invalid option."
            )


if __name__ == "__main__":

    main()