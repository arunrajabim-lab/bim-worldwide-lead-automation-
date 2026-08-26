import json
from . import config

def keyword_score(text):
    t = text.lower()
    hits = [k for k in config.SERVICE_KEYWORDS if k in t]
    score = min(95, 20 + len(hits) * 9)
    positives = ["outsourcing", "subcontract", "freelance",
                 "project based", "residential", "commercial",
                 "as-built", "point cloud", "coordination"]
    score = min(100, score + sum(3 for x in positives if x in t))
    service = ", ".join(dict.fromkeys(k.title() for k in hits)) or "BIM / CAD services"
    return {
        "lead_score": score,
        "service": service,
        "reason": "Matched public BIM/CAD service and outsourcing keywords."
    }

def ai_score(company, website, text):
    if not config.OPENAI_API_KEY:
        return keyword_score(text)

    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    prompt = f'''Qualify this B2B lead for a freelance BIM/CAD-to-BIM provider.

Company: {company}
Website: {website}
Public website text:
{text[:18000]}

Return JSON only with:
lead_score (0-100), service (short list), reason (short explanation).
Higher scores for BIM/CAD-to-BIM/Scan-to-BIM/Revit/MEP/architectural modeling
companies that appear likely to use project-based outsourcing.
Do not invent facts.'''
    try:
        r = client.chat.completions.create(
            model=config.AI_MODEL, temperature=0,
            messages=[{"role":"user", "content":prompt}]
        )
        return json.loads(r.choices[0].message.content)
    except Exception:
        return keyword_score(text)
