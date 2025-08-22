from django import template

register = template.Library()


def _is_hlavnice_name(value: str) -> bool:
    if not value:
        return False
    name = str(value).lower()
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
    if name in aliases:
        return True
    return "hlavnice" in name


@register.filter
def is_hlavnice(team_name: str) -> bool:
    """
    Returns True if the provided team name looks like Hlavnice.
    Accepts None. Case-insensitive. Matches common variants.
    """
    return _is_hlavnice_name(team_name)


@register.filter
def is_hlavnice_team(team) -> bool:
    """Returns True if the team object (or dict-like) looks like Hlavnice."""
    if not team:
        return False
    short = getattr(team, "short_name", None) or getattr(team, "shortName", None)
    name = getattr(team, "name", None)
    return _is_hlavnice_name(short or name)


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
