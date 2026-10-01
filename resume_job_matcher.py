import re
import sqlite3

from resume_matcher import (
    extract_resume_text,
    find_resume_skills
)


DATABASE_NAME = "internships.db"


# ---------------------------------------------------------
# Job-related skill categories
# ---------------------------------------------------------

TECH_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "git",
    "github",
    "linux",
    "matlab",
    "r",
    "aws",
    "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai/ml",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "computer vision",
    "natural language processing",
    "nlp",
    "rest api",
    "api",
    "mongodb",
    "postgresql",
    "mysql",
    "sqlite",
    "firebase",
    "flask",
    "django",
    "spring",
    "spring boot",
    "object oriented programming",
    "data structures",
    "algorithms",
    "operating systems",
    "computer networks",
    "digital logic",
]


# ---------------------------------------------------------
# Job title keywords
# ---------------------------------------------------------

STRONG_JOB_TITLES = [
    "software engineer",
    "software engineering",
    "software developer",
    "software development",
    "computer science",
    "computer engineering",
    "data engineer",
    "data engineering",
    "data scientist",
    "data science",
    "machine learning",
    "artificial intelligence",
    "ai engineer",
    "ml engineer",
    "cybersecurity",
    "cyber security",
    "cloud engineer",
    "devops",
    "systems engineer",
    "embedded engineer",
    "firmware engineer",
    "web developer",
    "web development",
    "application developer",
    "application engineering",
]


# ---------------------------------------------------------
# Load jobs
# ---------------------------------------------------------

def get_jobs():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            description,
            url,
            gpa_status,
            position_type,
            term,
            eligible,
            needs_review,
            status
        FROM jobs
        WHERE eligible = 1
           OR needs_review = 1
    """)

    jobs = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return jobs


# ---------------------------------------------------------
# Find skills inside text
# ---------------------------------------------------------

def find_skills_in_text(text):
    text = text.lower()

    found = []

    for skill in TECH_SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found.append(skill)

    return found


# ---------------------------------------------------------
# Calculate match
# ---------------------------------------------------------

def calculate_match(job, resume_skills):

    title = job["title"].lower()

    description = job["description"].lower()

    full_text = title + " " + description


    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    job_skills = find_skills_in_text(
        full_text
    )

    matched_skills = []

    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)


    # -----------------------------------------------------
    # Skill score
    # -----------------------------------------------------

    if job_skills:

        skill_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 60

    else:

        skill_score = 0


    score = skill_score


    reasons = []


    # -----------------------------------------------------
    # Job title relevance
    # -----------------------------------------------------

    title_match = False

    for keyword in STRONG_JOB_TITLES:

        if keyword in title:

            title_match = True

            break


    if title_match:

        score += 15

        reasons.append(
            "Strong CS/technology job title"
        )


    # -----------------------------------------------------
    # Internship/co-op
    # -----------------------------------------------------

    if job["position_type"] in [
        "INTERNSHIP",
        "CO-OP",
        "INTERNSHIP / CO-OP",
    ]:

        score += 10

        reasons.append(
            "Internship/co-op position"
        )


    # -----------------------------------------------------
    # 2027 term
    # -----------------------------------------------------

    if job["term"] in [
        "SPRING 2027",
        "SUMMER 2027",
        "SPRING + SUMMER 2027",
    ]:

        score += 10

        reasons.append(
            "2027 opportunity"
        )


    # -----------------------------------------------------
    # GPA
    # -----------------------------------------------------

    if job["gpa_status"] == "NOT_MENTIONED":

        score += 5

        reasons.append(
            "GPA not mentioned"
        )

    elif job["gpa_status"] == "PREFERRED":

        score += 3

        reasons.append(
            "GPA preferred but not required"
        )


    # -----------------------------------------------------
    # Remote
    # -----------------------------------------------------

    if "remote" in job["location"].lower():

        score += 3

        reasons.append(
            "Remote position"
        )


    # -----------------------------------------------------
    # Score cap
    # -----------------------------------------------------

    score = min(
        round(score),
        100
    )


    # -----------------------------------------------------
    # Return results
    # -----------------------------------------------------

    return {
        "score": score,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "reasons": reasons,
    }


# ---------------------------------------------------------
# Rank all jobs
# ---------------------------------------------------------

def rank_jobs(
    jobs,
    resume_skills
):

    results = []

    for job in jobs:

        match = calculate_match(
            job,
            resume_skills
        )

        results.append({

            "score":
                match["score"],

            "job_skills":
                match["job_skills"],

            "matched_skills":
                match["matched_skills"],

            "missing_skills":
                match["missing_skills"],

            "reasons":
                match["reasons"],

            "title":
                job["title"],

            "company":
                job["company"],

            "location":
                job["location"],

            "position_type":
                job["position_type"],

            "term":
                job["term"],

            "gpa_status":
                job["gpa_status"],

            "url":
                job["url"],
        })


    results.sort(
        key=lambda job: job["score"],
        reverse=True
    )


    return results


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

def print_results(
    results,
    limit=20
):

    print()

    print("=" * 75)

    print(
        "TOP RESUME → INTERNSHIP MATCHES"
    )

    print("=" * 75)


    if not results:

        print(
            "No matching jobs found."
        )

        return


    for number, job in enumerate(
        results[:limit],
        start=1
    ):

        print()

        print("-" * 75)

        print(
            f"#{number} "
            f"— {job['score']}% MATCH"
        )

        print(
            f"Title: {job['title']}"
        )

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


        print()

        print(
            "Skills you have:"
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
                "  None detected"
            )


        print()

        print(
            "Potential missing skills:"
        )


        if job["missing_skills"]:

            # Don't print an enormous list
            for skill in job[
                "missing_skills"
            ][:10]:

                print(
                    f"  ○ {skill}"
                )

        else:

            print(
                "  None detected"
            )


        print()

        print(
            "Why this matched:"
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
            f"URL: {job['url']}"
        )


    print()

    print("=" * 75)

    print(
        f"Showing top "
        f"{min(limit, len(results))} "
        f"of {len(results)} jobs"
    )

    print("=" * 75)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print()

    print(
        "Reading resume..."
    )


    resume_text = (
        extract_resume_text()
    )


    if not resume_text.strip():

        print()

        print(
            "ERROR: No text could be "
            "extracted from resume.pdf."
        )

        print()

        print(
            "If your PDF is image-based, "
            "we can add OCR later."
        )

        return


    resume_skills = (
        find_resume_skills(
            resume_text
        )
    )


    print()

    print(
        f"Detected "
        f"{len(resume_skills)} "
        f"skills in your resume."
    )


    print()

    print(
        "Your detected skills:"
    )


    for skill in resume_skills:

        print(
            f"  ✓ {skill}"
        )


    print()

    print(
        "Loading internship database..."
    )


    jobs = get_jobs()


    print(
        f"Loaded "
        f"{len(jobs)} "
        f"potential internships/co-ops."
    )


    print()

    print(
        "Matching resume against jobs..."
    )


    results = rank_jobs(
        jobs,
        resume_skills
    )


    print_results(
        results,
        limit=20
    )


if __name__ == "__main__":

    main()