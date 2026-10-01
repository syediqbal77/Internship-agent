import re
from pathlib import Path

from pypdf import PdfReader


RESUME_PATH = Path("resume.pdf")


SKILLS = [
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


def extract_resume_text():
    if not RESUME_PATH.exists():
        raise FileNotFoundError(
            "resume.pdf was not found. "
            "Make sure resume.pdf is inside the Internship-agent folder."
        )

    reader = PdfReader(str(RESUME_PATH))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text


def find_resume_skills(text):
    text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:
        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def print_resume_summary():
    print()
    print("=" * 60)
    print("RESUME ANALYZER")
    print("=" * 60)

    text = extract_resume_text()

    if not text.strip():
        print()
        print("WARNING: No text could be extracted from the PDF.")
        print()
        print(
            "Your resume may be an image/scanned PDF."
        )
        return

    skills = find_resume_skills(text)

    print()
    print(
        f"Resume characters extracted: {len(text)}"
    )

    print()
    print("Skills detected:")
    print("-" * 60)

    if not skills:
        print("No known skills were detected.")
    else:
        for skill in skills:
            print(f"✓ {skill}")

    print()
    print(
        f"Total skills detected: {len(skills)}"
    )

    print()
    print("=" * 60)
    print("RESUME ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    print_resume_summary()