"""Prompt templates for AI content generation."""

CONTENT_CALENDAR_PROMPT = """You are a social media marketing expert for gyms and fitness studios.

Create a 30-day Instagram content calendar.

Gym name: {gym_name}
City: {city}
Target audience: {audience}
Tone: {tone}

Generate 30 posts.

For each day include:
Day number
Post caption
Suggested image idea
5 relevant hashtags

Make captions engaging and ready to post.
"""

LOCATION_CONTEXT_SUFFIX = """

Important local context:
- This gym is based in {region_focus}.
- Make the content feel locally relevant for Hyderabad/Telangana audiences.
- Use culturally and geographically relevant references where appropriate.
- Keep language clear, modern, and Instagram-friendly.
"""
