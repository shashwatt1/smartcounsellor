"""
Utility: Parse academic program metadata from program name strings.
"""

import re


class ProgramType(str):
    BTECH = "BTech"          # 4-Year programs
    INTEGRATED = "Integrated"  # 5-Year programs
    UNKNOWN = "Unknown"


def get_program_type(program_name: str) -> str:
    """
    Extract program duration type from academic program name.

    JoSAA naming convention:
      '... (4 Years, ...)' → BTech
      '... (5 Years, ...)' → Integrated
    """
    name_lower = program_name.lower()
    if "4 year" in name_lower:
        return ProgramType.BTECH
    if "5 year" in name_lower:
        return ProgramType.INTEGRATED
    # Fallback: try numeric year patterns
    match = re.search(r"(\d)\s*year", name_lower)
    if match:
        years = int(match.group(1))
        return ProgramType.BTECH if years == 4 else ProgramType.INTEGRATED
    return ProgramType.UNKNOWN


def extract_branch_name(program_name: str) -> str:
    """
    Extract clean branch name from full academic program name.
    Example: 'Computer Science and Engineering (4 Years, B.Tech)' → 'Computer Science and Engineering'
    """
    # Remove parenthetical suffixes like '(4 Years, B.Tech)'
    clean = re.sub(r"\s*\(.*?\)\s*$", "", program_name).strip()
    return clean if clean else program_name


def is_five_year_program(program_name: str) -> bool:
    """Return True if this is a 5-year integrated program."""
    return get_program_type(program_name) == ProgramType.INTEGRATED
