from django import template

register = template.Library()


@register.filter
def is_hlavnice(team_name: str) -> bool:
    """
    Returns True if the provided team name looks like Hlavnice.
    Accepts None. Case-insensitive. Matches common variants.
    """
    if not team_name:
        return False
    name = str(team_name).lower()
    aliases = {
        "hlavnice",
        "tj hlavnice",
        "tj družba hlavnice",
        "tj druzba hlavnice",
        "družba hlavnice",
        "druzba hlavnice",
        "tj hlavnice a",
        "tj hlavnice b",
    }
    # direct alias hit
    if name in aliases:
        return True
    # contains 'hlavnice' is a strong signal
    return "hlavnice" in name


@register.filter
def team_display(team) -> str:
    """
    Prefer team's short_name, fallback to name. Accepts model or plain dict-like.
    """
    if not team:
        return ""
    short = getattr(team, "short_name", None) or getattr(team, "shortName", None)
    name = getattr(team, "name", None)
    return short or name or str(team)
