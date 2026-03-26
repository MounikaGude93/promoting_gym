"""Usage tracking helpers backed by Supabase table `usage`."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from auth import init_supabase


class UsageTableNotReadyError(RuntimeError):
    """Raised when Supabase `usage` table is missing."""


def get_current_month() -> str:
    """Return current month in YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")


def get_user_usage(email: str) -> dict[str, Any]:
    """Fetch monthly usage row for a user; create it if missing."""
    supabase = init_supabase()
    month = get_current_month()
    try:
        res = (
            supabase.table("usage")
            .select("*")
            .eq("email", email)
            .eq("month", month)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        # PGRST205 typically means relation/table is missing from schema cache.
        if "PGRST205" in str(exc) or "public.usage" in str(exc):
            raise UsageTableNotReadyError(
                "Supabase table `usage` is not ready. Run supabase_usage_table.sql in SQL Editor."
            ) from exc
        raise

    if res.data:
        return res.data[0]

    insert_res = (
        supabase.table("usage")
        .insert(
            {
                "email": email,
                "month": month,
                "single_posts": 0,
                "weekly_plans": 0,
                "calendars": 0,
            }
        )
        .execute()
    )
    return insert_res.data[0]


def _increment_usage(email: str, field_name: str) -> dict[str, Any]:
    usage = get_user_usage(email)
    current_value = int(usage.get(field_name, 0))
    supabase = init_supabase()
    update_res = (
        supabase.table("usage")
        .update({field_name: current_value + 1})
        .eq("id", usage["id"])
        .execute()
    )
    return update_res.data[0]


def increment_single_post(email: str) -> dict[str, Any]:
    """Increment `single_posts` counter for this month."""
    return _increment_usage(email, "single_posts")


def increment_weekly_plan(email: str) -> dict[str, Any]:
    """Increment `weekly_plans` counter for this month."""
    return _increment_usage(email, "weekly_plans")


def increment_calendar(email: str) -> dict[str, Any]:
    """Increment `calendars` counter for this month."""
    return _increment_usage(email, "calendars")
