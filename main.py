from jobs import get_all_jobs
from filters import evaluate_job
from database import create_database, save_job


def main():
    print()
    print("INTERNSHIP AGENT")
    print("=" * 60)

    create_database()

    print()
    print("Searching companies...")

    jobs = get_all_jobs()

    print()
    print(f"Total jobs found: {len(jobs)}")

    print()
    print("Analyzing jobs...")

    new_jobs = 0
    qualified_jobs = 0
    review_jobs = 0

    stats = {
        "not_tech": 0,
        "not_internship": 0,
        "other_year": 0,
        "gpa_required": 0,
    }

    for job in jobs:
        result = evaluate_job(job)

        was_saved = save_job(job, result)

        if was_saved:
            new_jobs += 1

        # Count jobs rejected by each major filter
        if not result["tech_position"]:
            stats["not_tech"] += 1

        elif result["position_type"] == "OTHER":
            stats["not_internship"] += 1

        elif result["term"] == "OTHER YEAR":
            stats["other_year"] += 1

        elif result["gpa"] == "REQUIRED":
            stats["gpa_required"] += 1

        # Definite matches
        if result["eligible"]:
            qualified_jobs += 1

        # Potential matches that need additional review
        elif result["needs_review"]:
            review_jobs += 1

    print()
    print("=" * 60)
    print("FILTER DIAGNOSTICS")
    print("=" * 60)

    print(f"Not tech-related: {stats['not_tech']}")
    print(f"Not internship/co-op: {stats['not_internship']}")
    print(f"Explicitly another year: {stats['other_year']}")
    print(f"GPA required: {stats['gpa_required']}")

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(f"Jobs found: {len(jobs)}")
    print(f"New jobs saved: {new_jobs}")
    print(f"Qualified 2027 internships/co-ops: {qualified_jobs}")
    print(f"Needs 2027 review: {review_jobs}")


if __name__ == "__main__":
    main()