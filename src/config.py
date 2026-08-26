import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# SEARCH API
# =========================

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_API_URL = os.getenv(
    "SEARCH_API_URL",
    "https://serpapi.com/search.json"
)

# =========================
# AI
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "")

# =========================
# SEARCH LIMITS
# =========================

# Search more than 20 candidates so we can filter
# and finally select the best 20 qualified companies.
MAX_RESULTS_PER_QUERY = int(
    os.getenv("MAX_RESULTS_PER_QUERY", "10")
)

MAX_COMPANIES = int(
    os.getenv("MAX_COMPANIES", "60")
)

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "10")
)

# =========================
# SEARCH PRIORITY
# =========================

# FIRST PRIORITY — SCAN TO BIM
SCAN_TO_BIM_QUERIES = [
    '"Scan to BIM" company',
    '"Scan to BIM" services',
    '"Scan to BIM" outsourcing',
    '"Point Cloud to BIM" company',
    '"Point Cloud to BIM" services',
    '"Laser Scan to BIM" company',
    '"Scan-to-Revit" services',
]

# SECOND PRIORITY — CAD TO BIM
CAD_TO_BIM_QUERIES = [
    '"CAD to BIM" company',
    '"CAD to BIM" services',
    '"CAD to BIM" outsourcing',
    '"2D CAD to Revit" services',
    '"DWG to Revit" services',
    '"AutoCAD to BIM" company',
]

# Scan-to-BIM is intentionally BEFORE CAD-to-BIM
SEARCH_QUERIES = (
    SCAN_TO_BIM_QUERIES +
    CAD_TO_BIM_QUERIES
)

# =========================
# WORLDWIDE REGIONS
# =========================

REGIONS = [
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "United Arab Emirates",
    "Saudi Arabia",
    "Qatar",
    "Singapore",
    "New Zealand",
    "Germany",
    "Netherlands",
    "Ireland",
    "India",
    "Europe",
    "Middle East",
]

# =========================
# SERVICE KEYWORDS
# =========================

SERVICE_KEYWORDS = [
    # Scan to BIM
    "scan to bim",
    "scan-to-bim",
    "point cloud to bim",
    "laser scan to bim",
    "scan to revit",
    "point cloud",
    "reality capture",

    # CAD to BIM
    "cad to bim",
    "2d cad to revit",
    "dwg to revit",
    "autocad to bim",
    "cad conversion",

    # General BIM
    "bim outsourcing",
    "bim modeling",
    "revit modeling",
    "bim coordination",
    "architectural bim",
    "mep bim",
    "as-built bim",
]
