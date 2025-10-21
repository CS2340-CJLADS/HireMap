from django.db.models import Q
from accounts.models import Applicant
from jobs.models import JobPosting
import re


def normalize_skills(skills_text):
    """Normalize skills text for comparison

    Args:
        skills_text (str): Raw skills text

    Returns:
        set: Set of normalized skill strings
    """
    if not skills_text:
        return set()
    # Convert to lowercase, split on common separators
    skills = re.split(r'[,;/\n]+', skills_text.lower())
    # Remove whitespace and empty strings
    return {skill.strip() for skill in skills if skill.strip()}


def normalize_words(text):
    """Return a set of normalized words from freeform text for subject matching."""
    if not text:
        return set()
    # Split on non-word characters, keep alpha tokens > 2 chars
    words = re.split(r'\W+', text.lower())
    return {w for w in (word.strip() for word in words) if len(w) > 2}


def parse_degree_level(text):
    """Parse education text and return a coarse degree level integer.

    Levels: 0 = none/unspecified, 1 = associate, 2 = bachelor, 3 = master, 4 = phd/doctorate
    """
    if not text:
        return 0
    t = text.lower()
    if 'phd' in t or 'doctor' in t or 'doctoral' in t:
        return 4
    if 'master' in t or "m.sc" in t or "msc" in t or "m.s." in t or "m.s" in t or 'ma ' in t:
        return 3
    if 'bachelor' in t or 'b.sc' in t or 'b.s.' in t or 'bs ' in t or 'ba ' in t:
        return 2
    if 'associate' in t:
        return 1
    return 0


def parse_education_info(text):
    """Extract degree level and subject words from education text."""
    if not text:
        return {'degree_level': 0, 'subjects': set()}
    degree_level = parse_degree_level(text)
    subjects = normalize_words(text)
    return {'degree_level': degree_level, 'subjects': subjects}


def compute_skill_score(job_skills, applicant_skills):
    """Compute skill-based score in [0,1]."""
    if not job_skills:
        return 0.0
    if not applicant_skills:
        return 0.0
    matching = job_skills.intersection(applicant_skills)
    return len(matching) / len(job_skills)


def compute_education_score(job_edu_info, applicant_edu_info):
    """Compute education-based score in [0,1].

    The score combines degree-level match and subject overlap. If the job specifies no degree level
    we rely more heavily on subject overlap.
    """
    job_level = job_edu_info.get('degree_level', 0)
    app_level = applicant_edu_info.get('degree_level', 0)
    job_subjects = job_edu_info.get('subjects', set())
    app_subjects = applicant_edu_info.get('subjects', set())

    subject_overlap = 0.0
    if job_subjects:
        subject_overlap = len(job_subjects.intersection(app_subjects)) / max(len(job_subjects), 1)

    if job_level > 0:
        # Degree ratio: applicant_level / job_level (capped at 1)
        degree_ratio = min(1.0, app_level / job_level) if job_level > 0 else 0.0
        # Weight degree more heavily when job asks for a degree
        return 0.7 * degree_ratio + 0.3 * subject_overlap
    else:
        # No explicit degree requested; rely on subject overlap primarily
        return subject_overlap


def get_recommended_jobs(applicant, min_score=0.15, limit=10, include_drafts=False):
    """Get recommended jobs for an applicant.

    Scoring weights:
    - skills: 0.60
    - education: 0.35
    - location/other small bonuses: 0.05

    Args:
        include_drafts (bool): Whether to include draft jobs in the recommendations.
    """
    SKILL_WEIGHT = 0.60
    EDU_WEIGHT = 0.35
    BONUS_WEIGHT = 0.05

    applicant_skills = normalize_skills(applicant.skills)
    applicant_edu = parse_education_info(applicant.education)

    # Applicants should not see draft jobs
    active_jobs = JobPosting.objects.filter(is_closed=False, is_draft=False)

    matches = []
    for job in active_jobs:
        job_skills = normalize_skills(job.skills_required)
        job_edu_text = ' '.join(filter(None, [job.description, job.title, job.skills_required]))
        job_edu = parse_education_info(job_edu_text)

        skill_score = compute_skill_score(job_skills, applicant_skills)
        edu_score = compute_education_score(job_edu, applicant_edu)

        score = SKILL_WEIGHT * skill_score + EDU_WEIGHT * edu_score

        # Small location/remote bonus (kept within BONUS_WEIGHT cap)
        bonus = 0.0
        if applicant.location and job.location:
            if applicant.location.lower() == job.location.lower():
                bonus = 0.05
            elif job.remote:
                bonus = 0.02

        score += min(bonus, BONUS_WEIGHT)
        score = max(0.0, min(1.0, score))

        if score >= min_score:
            matches.append((job, score))
            print(f"Job: {job.title}, Score: {score}")

    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:limit]


def get_recommended_applicants(job_posting, min_score=0.15, limit=10):
    """Get recommended applicants for a job posting.

    Uses symmetric weights to `get_recommended_jobs`.
    """
    try:
        print(f"\nProcessing recommendations for job: {job_posting.title}")
        print(f"Required skills: {job_posting.skills_required}")
        
        SKILL_WEIGHT = 0.60
        EDU_WEIGHT = 0.35
        BONUS_WEIGHT = 0.05

        job_skills = normalize_skills(job_posting.skills_required)
        print(f"Normalized job skills: {job_skills}")
        
        job_edu_text = ' '.join(filter(None, [job_posting.description, job_posting.title, job_posting.skills_required]))
        job_edu = parse_education_info(job_edu_text)
        print(f"Parsed job education info: {job_edu}")

        available_applicants = Applicant.objects.filter(availability__in=['available', 'open-to-work'])
        print(f"Found {available_applicants.count()} available applicants")

        matches = []
        for applicant in available_applicants:
            print(f"\nEvaluating applicant: {applicant.first_name} {applicant.last_name}")
            
            applicant_skills = normalize_skills(applicant.skills)
            print(f"Applicant skills: {applicant_skills}")
            
            applicant_edu = parse_education_info(applicant.education)
            print(f"Applicant education: {applicant_edu}")

            skill_score = compute_skill_score(job_skills, applicant_skills)
            edu_score = compute_education_score(job_edu, applicant_edu)
            print(f"Scores - Skills: {skill_score:.2f}, Education: {edu_score:.2f}")

            score = SKILL_WEIGHT * skill_score + EDU_WEIGHT * edu_score

            bonus = 0.0
            if applicant.location and job_posting.location:
                if applicant.location.lower() == job_posting.location.lower():
                    bonus = 0.05
                    print("Added location match bonus: 0.05")
                elif job_posting.remote:
                    bonus = 0.02
                    print("Added remote work bonus: 0.02")

            score += min(bonus, BONUS_WEIGHT)
            score = max(0.0, min(1.0, score))
            print(f"Final score: {score:.2f}")

            if score >= min_score:
                matches.append((applicant, score))
                print("Added to matches (passed minimum score)")
            else:
                print("Score below minimum threshold")

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:limit]
        
    except Exception as e:
        print(f"Error in get_recommended_applicants: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return []