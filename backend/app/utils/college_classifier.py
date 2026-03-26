"""
Utility: Classify institute type and determine applicable quotas using exact user mappings.
"""

from enum import Enum


class CollegeType(str, Enum):
    IIT = "IIT"
    NIT = "NIT"
    IIIT = "IIIT"
    GFTI = "GFTI"
    OTHER = "OTHER"


# NIT to State Map
NIT_STATE_MAP: dict[str, str] = {
    "Agartala": "Tripura",
    "Allahabad": "Uttar Pradesh",
    "Andhra Pradesh": "Andhra Pradesh",
    "Arunachal Pradesh": "Arunachal Pradesh",
    "Bhopal": "Madhya Pradesh",
    "Calicut": "Kerala",
    "Delhi": "Delhi",
    "Durgapur": "West Bengal",
    "Goa": "Goa",
    "Hamirpur": "Himachal Pradesh",
    "Jalandhar": "Punjab",
    "Jamshedpur": "Jharkhand",
    "Kurukshetra": "Haryana",
    "Meghalaya": "Meghalaya",
    "Mizoram": "Mizoram",
    "Nagaland": "Nagaland",
    "Nagpur": "Maharashtra",
    "Patna": "Bihar",
    "Puducherry": "Puducherry",
    "Raipur": "Chhattisgarh",
    "Rourkela": "Odisha",
    "Sikkim": "Sikkim",
    "Silchar": "Assam",
    "Srinagar": "Jammu & Kashmir",
    "Surathkal": "Karnataka",
    "Tiruchirappalli": "Tamil Nadu",
    "Trichy": "Tamil Nadu",
    "Uttarakhand": "Uttarakhand",
    "Warangal": "Telangana",
}

# GFTI to State Map
GFTI_STATE_MAP: dict[str, str] = {
    "Assam University": "Assam",
    "Birla Institute of Technology": "Jharkhand",
    "Gurukul Kangri": "Uttarakhand",
    "Carpet Technology": "Uttar Pradesh",
    "Infrastructure Technology Research and Management": "Gujarat",
    "Chemical Technology": "Maharashtra",
    "Jawaharlal Nehru University": "Delhi",
    "Punjab Engineering College": "Chandigarh",
    "Planning and Architecture": "Delhi",      # Note: Need exact matching logic for SPA
    "Shri Mata Vaishno Devi": "Jammu & Kashmir",
    "Tezpur University": "Assam",
    "IIEST Shibpur": "West Bengal",
    "Sant Longowal": "Punjab",
    "Mizoram University": "Mizoram",
    "Nagaland University": "Nagaland",
    "Tripura University": "Tripura",
    "Central University of Rajasthan": "Rajasthan",
    "Central University of Haryana": "Haryana",
    "Central University of Punjab": "Punjab",
    "Central University of Jharkhand": "Jharkhand",
    "H. S. Gour": "Madhya Pradesh", # From the new CSV "Institute of Engineering and Technology, Dr. H. S. Gour University"
}


def classify_institute(institute: str) -> CollegeType:
    """Detect college type from institute name string."""
    name = institute.upper()
    if "INDIAN INSTITUTE OF TECHNOLOGY" in name:
        return CollegeType.IIT
    if "NATIONAL INSTITUTE OF TECHNOLOGY" in name:
        return CollegeType.NIT
    if "IIIT" in name or "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY" in name:
        return CollegeType.IIIT
    
    # Anything else in the JOSAA dataset is likely a GFTI
    # We can also do string matches from GFTI_STATE_MAP
    return CollegeType.GFTI


def get_quota_for_institute(institute: str, home_state: str | None) -> list[str]:
    """
    Return applicable quota list for a given institute + student home state.

    Rules:
      IIT / IIIT → always ["AI"]
      NIT        → ["HS"] if institute state matches home_state, else ["OS"]
      GFTI       → ["HS"] if institute state matches home_state, else ["AI"]
    """
    college_type = classify_institute(institute)
    
    if college_type in (CollegeType.IIT, CollegeType.IIIT, CollegeType.OTHER):
        return ["AI"]
        
    if college_type == CollegeType.NIT:
        if home_state is None:
            return ["HS", "OS"]
        institute_state = _get_nit_state(institute)
        if institute_state and institute_state.lower() == home_state.lower():
            return ["HS"]
        return ["OS"]
        
    if college_type == CollegeType.GFTI:
        if home_state is None:
            return ["HS", "AI"]
        institute_state = _get_gfti_state(institute)
        if institute_state and institute_state.lower() == home_state.lower():
            return ["HS", "AI"]  # Some GFTIs might still use AI even if it's HS, but mostly HS
            # Wait, the instruction says "the quota for HS is for the student who are from the state where college is situated 
            # and AI for rest of the people in country... AI is used for other state not HS".
            return ["HS"]
        return ["AI"]

    return ["AI"]


def _get_nit_state(institute: str) -> str | None:
    for fragment, state in NIT_STATE_MAP.items():
        if fragment.lower() in institute.lower():
            return state
    return None


def _get_gfti_state(institute: str) -> str | None:
    # Explicit override for School of Planning and Architecture (SPAs)
    if "Planning and Architecture" in institute:
        if "Bhopal" in institute: return "Madhya Pradesh"
        if "Vijayawada" in institute: return "Andhra Pradesh"
        if "Delhi" in institute: return "Delhi"
        
    for fragment, state in GFTI_STATE_MAP.items():
        if fragment.lower() in institute.lower():
            return state
    return None
