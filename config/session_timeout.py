from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
from django.utils import timezone


SESSION_ACTIVITY_KEY = "session_last_activity_ts"


def get_session_timeout_seconds():
    return max(60, int(getattr(settings, "SESSION_INACTIVITY_TIMEOUT_SECONDS", 1800)))


def get_session_warning_seconds():
    timeout_seconds = get_session_timeout_seconds()
    return max(30, min(timeout_seconds, int(getattr(settings, "SESSION_TIMEOUT_WARNING_SECONDS", 300))))


def get_session_last_activity(request):
    raw_value = request.session.get(SESSION_ACTIVITY_KEY)
    if raw_value in (None, ""):
        return None

    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return None


def set_session_last_activity(request, now=None):
    now = now or timezone.now()
    timeout_seconds = get_session_timeout_seconds()
    request.session[SESSION_ACTIVITY_KEY] = int(now.timestamp())
    request.session.set_expiry(timeout_seconds)
    request.session.modified = True
    return timeout_seconds


def get_session_remaining_seconds(request, now=None):
    now = now or timezone.now()
    timeout_seconds = get_session_timeout_seconds()
    last_activity_ts = get_session_last_activity(request)

    if last_activity_ts is None:
        try:
            expiry_age = int(request.session.get_expiry_age())
        except Exception:
            expiry_age = timeout_seconds
        return max(0, min(timeout_seconds, expiry_age))

    elapsed_seconds = max(0, int(now.timestamp()) - last_activity_ts)
    return max(0, timeout_seconds - elapsed_seconds)


def format_session_remaining_seconds(total_seconds):
    total_seconds = max(0, int(total_seconds or 0))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return f"{minutes:02d}:{seconds:02d}"


def is_session_timed_out(request, now=None):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return False
    return get_session_remaining_seconds(request, now=now) <= 0


def build_session_login_url(next_url=""):
    query_params = {"session": "expired"}
    if next_url:
        query_params["next"] = next_url
    return f"{reverse('login')}?{urlencode(query_params)}"
