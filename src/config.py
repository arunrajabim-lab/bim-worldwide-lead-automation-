import os
from dotenv import load_dotenv
load_dotenv()

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_API_URL = os.getenv("SEARCH_API_URL", "https://serpapi.com/search.json")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-5.6-mini")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
REPORT_FROM_EMAIL = os.getenv("REPORT_FROM_EMAIL", SMTP_USERNAME)
REPORT_TO_EMAIL = os.getenv("REPORT_TO_EMAIL", "")

MAX_RESULTS_PER_QUERY = int(os.getenv("MAX_RESULTS_PER_QUERY", "10"))
MAX_COMPANIES = int(os.getenv("MAX_COMPANIES", "100"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))

SEARCH_QUERIES = [
    '"CAD to BIM" outsourcing company',
    '"CAD to BIM" services',
    '"Scan to BIM" services company',
    '"Scan to BIM" outsourcing',
    '"Revit modeling" outsourcing company',
    '"BIM outsourcing" services',
    '"BIM coordination" outsourcing',
    '"point cloud to BIM" company',
    '"architectural BIM" outsourcing',
    '"MEP BIM" outsourcing',
    '"as-built BIM" services',
    '"Revit conversion" services company',
    '"BIM modeling" outsourcing',
]

REGIONS = [
    "United States", "United Kingdom", "Canada", "Australia",
    "United Arab Emirates", "Saudi Arabia", "Qatar", "Singapore",
    "New Zealand", "Germany", "Netherlands", "Ireland"
]

SERVICE_KEYWORDS = [
    "cad to bim", "scan to bim", "point cloud to bim", "revit",
    "bim outsourcing", "bim modeling", "bim coordination",
    "architectural bim", "mep bim", "as-built", "3d modeling"
]
