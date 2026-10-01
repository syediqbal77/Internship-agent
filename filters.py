import re


def check_gpa_requirement(description):
    text = description.lower()

    required_patterns = [
        r"minimum gpa.{0,40}\d\.\d",
        r"gpa.{0,30}required",
        r"gpa.{0,30}requirement",
        r"required.{0,30}gpa",
        r"must have.{0,40}gpa",
        r"must maintain.{0,40}gpa",
        r"gpa.{0,30}of at least \d\.\d",
        r"gpa.{0,30}of \d\.\d or higher",
        r"minimum.{0,30}\d\.\d gpa",
    ]

    for pattern in required_patterns:
        if re.search(pattern, text):
            return "REQUIRED"

    preferred_patterns = [
        r"gpa.{0,40}preferred",
        r"preferred.{0,40}gpa",
        r"gpa.{0,40}recommended",
        r"recommended.{0,40}gpa",
    ]

    for pattern in preferred_patterns:
        if re.search(pattern, text):
            return "PREFERRED"

    if "gpa" in text:
        return "MENTIONED"

    return "NOT_MENTIONED"


def get_position_type(title, description):
    text = (title + " " + description).lower()

    internship_terms = [
        "intern",
        "internship",
    ]

    coop_terms = [
        "co-op",
        "coop",
        "cooperative education",
        "cooperative program",
    ]

    has_internship = any(term in text for term in internship_terms)
    has_coop = any(term in text for term in coop_terms)

    if has_internship and has_coop:
        return "INTERNSHIP / CO-OP"

    if has_internship:
        return "INTERNSHIP"

    if has_coop:
        return "CO-OP"

    return "OTHER"


def is_tech_position(title, description):
    text = (title + " " + description).lower()

    tech_terms = [
        "software",
        "software engineer",
        "software development",
        "computer science",
        "computer engineering",
        "programming",
        "developer",
        "data science",
        "data scientist",
        "data engineer",
        "machine learning",
        "artificial intelligence",
        "ai/ml",
        "cybersecurity",
        "information technology",
        "cloud",
        "database",
        "web development",
        "devops",
        "systems engineering",
        "network engineering",
        "firmware",
        "embedded systems",
        "robotics",
        "computer vision",
        "mobile development",
    ]

    return any(term in text for term in tech_terms)


def detect_2027_term(title, description):
    text = (title + " " + description).lower()

    spring_patterns = [
        r"spring\s+(?:of\s+)?2027",
        r"2027\s+spring",
        r"spring\s+2027\s+(?:intern|internship|co[- ]?op)",
    ]

    summer_patterns = [
        r"summer\s+(?:of\s+)?2027",
        r"2027\s+summer",
        r"summer\s+2027\s+(?:intern|internship|co[- ]?op)",
    ]

    spring = any(
        re.search(pattern, text)
        for pattern in spring_patterns
    )

    summer = any(
        re.search(pattern, text)
        for pattern in summer_patterns
    )

    if spring and summer:
        return "SPRING + SUMMER 2027"

    if spring:
        return "SPRING 2027"

    if summer:
        return "SUMMER 2027"

    # Explicitly identified as another year
    if "2026" in text and "2027" not in text:
        return "OTHER YEAR"

    if "2028" in text and "2027" not in text:
        return "OTHER YEAR"

    # No specific term found
    return "NOT_SPECIFIED"


def evaluate_job(job):
    gpa_status = check_gpa_requirement(job.description)

    position_type = get_position_type(
        job.title,
        job.description
    )

    tech_status = is_tech_position(
        job.title,
        job.description
    )

    term = detect_2027_term(
        job.title,
        job.description
    )

    valid_position = position_type in [
        "INTERNSHIP",
        "CO-OP",
        "INTERNSHIP / CO-OP",
    ]

    explicit_2027 = term in [
        "SPRING 2027",
        "SUMMER 2027",
        "SPRING + SUMMER 2027",
    ]

    other_year = term == "OTHER YEAR"

    gpa_ok = gpa_status != "REQUIRED"

    # Definitely qualifies
    eligible = (
        valid_position
        and tech_status
        and explicit_2027
        and gpa_ok
    )

    # Potentially qualifies, but the posting doesn't explicitly
    # identify Spring/Summer 2027.
    needs_review = (
        valid_position
        and tech_status
        and not explicit_2027
        and not other_year
        and gpa_ok
    )

    # Completely rejected
    rejected = not eligible and not needs_review

    if eligible:
        status = "QUALIFIED"
    elif needs_review:
        status = "NEEDS_REVIEW"
    else:
        status = "REJECTED"

    return {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "url": job.url,
        "position_type": position_type,
        "tech_position": tech_status,
        "term": term,
        "gpa": gpa_status,
        "eligible": eligible,
        "needs_review": needs_review,
        "rejected": rejected,
        "status": status,
    }