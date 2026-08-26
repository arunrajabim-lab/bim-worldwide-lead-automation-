import json
from . import config


# =========================================================
# SERVICE PRIORITY
# =========================================================

SCAN_TO_BIM_KEYWORDS = [
    "scan to bim",
    "scan-to-bim",
    "point cloud to bim",
    "point-cloud-to-bim",
    "laser scan to bim",
    "scan to revit",
    "reality capture",
    "point cloud",
]

CAD_TO_BIM_KEYWORDS = [
    "cad to bim",
    "cad-to-bim",
    "2d cad to revit",
    "dwg to revit",
    "autocad to bim",
    "cad conversion",
]


# =========================================================
# GOOD LEAD SIGNALS
# =========================================================

OUTSOURCING_KEYWORDS = [
    "outsourcing",
    "outsource",
    "subcontract",
    "subcontracting",
    "external team",
    "external resource",
    "project based",
    "project-based",
    "remote team",
    "bim production",
    "bim support",
    "production support",
]


PROJECT_KEYWORDS = [
    "project",
    "projects",
    "residential",
    "commercial",
    "hospital",
    "hotel",
    "villa",
    "apartment",
    "construction",
    "architecture",
    "engineering",
    "contractor",
]


BIM_KEYWORDS = [
    "bim",
    "revit",
    "architectural bim",
    "mep bim",
    "structural bim",
    "bim modeling",
    "bim coordination",
    "as-built",
]


# =========================================================
# BAD / LOW PRIORITY SIGNALS
# =========================================================

LOW_PRIORITY_KEYWORDS = [
    "training only",
    "course",
    "training institute",
    "software training",
    "student",
    "tutorial",
]


def contains_any(text, keywords):
    return [
        keyword
        for keyword in keywords
        if keyword.lower() in text
    ]


def keyword_score(text):

    text = text.lower()

    scan_hits = contains_any(
        text,
        SCAN_TO_BIM_KEYWORDS
    )

    cad_hits = contains_any(
        text,
        CAD_TO_BIM_KEYWORDS
    )

    outsourcing_hits = contains_any(
        text,
        OUTSOURCING_KEYWORDS
    )

    project_hits = contains_any(
        text,
        PROJECT_KEYWORDS
    )

    bim_hits = contains_any(
        text,
        BIM_KEYWORDS
    )

    low_priority_hits = contains_any(
        text,
        LOW_PRIORITY_KEYWORDS
    )

    # -----------------------------------------------------
    # BASE SCORE
    # -----------------------------------------------------

    score = 20

    # -----------------------------------------------------
    # SCAN TO BIM = HIGHEST PRIORITY
    # -----------------------------------------------------

    if scan_hits:
        score += 35

    # -----------------------------------------------------
    # CAD TO BIM = SECOND PRIORITY
    # -----------------------------------------------------

    elif cad_hits:
        score += 28

    # -----------------------------------------------------
    # GENERAL BIM
    # -----------------------------------------------------

    score += min(
        15,
        len(bim_hits) * 3
    )

    # -----------------------------------------------------
    # OUTSOURCING SIGNAL
    # -----------------------------------------------------

    score += min(
        15,
        len(outsourcing_hits) * 5
    )

    # -----------------------------------------------------
    # PROJECT SIGNAL
    # -----------------------------------------------------

    score += min(
        10,
        len(project_hits) * 2
    )

    # -----------------------------------------------------
    # LOW PRIORITY PENALTY
    # -----------------------------------------------------

    score -= min(
        25,
        len(low_priority_hits) * 8
    )

    score = max(
        0,
        min(100, score)
    )

    # -----------------------------------------------------
    # SERVICE
    # -----------------------------------------------------

    if scan_hits:
        service = "Scan to BIM"

    elif cad_hits:
        service = "CAD to BIM"

    elif "mep bim" in text:
        service = "MEP BIM"

    elif "architectural bim" in text:
        service = "Architectural BIM"

    elif "bim coordination" in text:
        service = "BIM Coordination"

    elif "revit" in text:
        service = "Revit / BIM Services"

    else:
        service = "BIM / CAD Services"

    # -----------------------------------------------------
    # REASON
    # -----------------------------------------------------

    reasons = []

    if scan_hits:
        reasons.append(
            "Scan-to-BIM service detected"
        )

    elif cad_hits:
        reasons.append(
            "CAD-to-BIM service detected"
        )

    if outsourcing_hits:
        reasons.append(
            "outsourcing/project-support signal detected"
        )

    if project_hits:
        reasons.append(
            "active project/service-market signal detected"
        )

    if not reasons:
        reasons.append(
            "BIM/CAD service detected"
        )

    return {
        "lead_score": score,
        "service": service,
        "reason": "; ".join(reasons)
    }


# =========================================================
# AI QUALIFICATION
# =========================================================

def ai_score(company, website, text):

    # If OpenAI key is not configured,
    # use the reliable keyword scoring system.
    if not config.OPENAI_API_KEY:
        return keyword_score(text)

    from openai import OpenAI

    client = OpenAI(
        api_key=config.OPENAI_API_KEY
    )

    prompt = f"""
You are qualifying a company as a potential B2B client
for a freelance BIM/CAD-to-BIM production service.

Target priority:

1. Scan to BIM
2. Point Cloud to BIM
3. Laser Scan to BIM
4. Scan to Revit
5. CAD to BIM
6. DWG to Revit
7. 2D CAD to Revit
8. AutoCAD to BIM
9. Revit/BIM outsourcing
10. Architectural / MEP BIM production

Company:
{company}

Website:
{website}

Public website text:
{text[:18000]}

Scoring:

90-100:
Very strong potential project/outsourcing lead.

75-89:
Strong BIM/CAD service company with good potential.

60-74:
Possible lead.

Below 60:
Low priority.

Give higher scores when the company shows:
- Scan-to-BIM work
- Point cloud projects
- CAD-to-BIM conversion
- Revit production
- BIM outsourcing
- subcontracting
- external BIM support
- project-based work
- architecture/construction projects
- commercial/residential projects

Give lower scores to:
- training institutes
- software vendors only
- education websites
- companies with no BIM/CAD production service

Do NOT invent facts.

Return JSON only:

{{
    "lead_score": 0,
    "service": "Scan to BIM",
    "reason": "short factual explanation"
}}
"""

    try:

        response = client.chat.completions.create(
            model=config.AI_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = json.loads(
            response.choices[0]
            .message.content
        )

        # Safety check
        result["lead_score"] = max(
            0,
            min(
                100,
                int(result.get("lead_score", 0))
            )
        )

        return result

    except Exception as e:

        print(
            f"AI qualification failed: {e}"
        )

        # Always fall back to keyword scoring
        return keyword_score(text)
