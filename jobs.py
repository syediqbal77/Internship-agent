import requests
from dataclasses import dataclass

from companies import COMPANIES


@dataclass
class Job:
    title: str
    company: str
    description: str
    location: str = ""
    url: str = ""


def get_greenhouse_jobs(board_token, company_name):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    response = requests.get(
        url,
        params={"content": "true"},
        headers={"User-Agent": "InternshipAgent/1.0"},
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for item in data.get("jobs", []):
        jobs.append(
            Job(
                title=item.get("title", ""),
                company=company_name,
                description=item.get("content", ""),
                location=item.get("location", {}).get("name", ""),
                url=item.get("absolute_url", "")
            )
        )

    return jobs


def get_all_jobs():
    all_jobs = []

    for company in COMPANIES:
        try:
            print(f"Searching {company['name']}...")

            jobs = get_greenhouse_jobs(
                company["token"],
                company["name"]
            )

            all_jobs.extend(jobs)

            print(f"  Found {len(jobs)} jobs.")

        except requests.RequestException as error:
            print(
                f"  Could not retrieve jobs from "
                f"{company['name']}: {error}"
            )

    return all_jobs


if __name__ == "__main__":
    jobs = get_all_jobs()

    print()
    print("=" * 60)
    print(f"TOTAL JOBS FOUND: {len(jobs)}")
    print("=" * 60)