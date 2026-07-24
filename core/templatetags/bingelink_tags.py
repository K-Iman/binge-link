from django import template
from django.conf import settings

register = template.Library()


@register.filter
def rating_class(value):
    """Return CSS class for a TMDB vote_average value."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "rating-low"
    if v >= 7.0:
        return "rating-high"
    elif v >= 5.0:
        return "rating-mid"
    return "rating-low"


@register.filter
def tmdb_image(path, size="w500"):
    """Build a full TMDB image URL from a path fragment."""
    if not path:
        return ""
    base = getattr(settings, "TMDB_IMAGE_BASE_URL", "https://image.tmdb.org/t/p")
    return f"{base}/{size}{path}"


@register.filter
def media_title(item):
    """Return title for movie or name for TV show."""
    return item.get("title") or item.get("name") or "Untitled"


@register.filter
def media_year(item):
    """Extract year from release_date or first_air_date."""
    date = item.get("release_date") or item.get("first_air_date") or ""
    return date[:4] if date else "—"
