import logging
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def robots_txt(request):
    return render(request, "robots.txt", content_type="text/plain")


def health_check(request):
    """
    Lightweight health check endpoint for Render and uptime monitors.
    Validates process responsiveness and database connectivity.
    """
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
    except Exception as e:
        logger.error("Health check database probe error: %s", e)
        db_ok = False

    status_code = 200 if db_ok else 503
    return JsonResponse(
        {
            "status": "healthy" if db_ok else "unhealthy",
            "app": "ssfarms",
            "database": "connected" if db_ok else "disconnected",
        },
        status=status_code,
    )