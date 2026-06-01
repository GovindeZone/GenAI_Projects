def rank_candidates(resumes, role, required_skills):

    results = []

    for resume in resumes:

        text = resume["content"].lower()

        matched_skills = []

        for skill in required_skills:

            if skill.lower() in text:
                matched_skills.append(skill)

        match_percent = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

        results.append({

            "Candidate Resume":
                resume["file_name"],

            "Role":
                role,

            "Matched Skills":
                ", ".join(matched_skills),

            "Match %":
                round(match_percent, 2)
        })

    return results