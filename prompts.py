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

REAL_ESTATE_PROMPT_TEMPLATE = """You are a social media marketing expert for real estate businesses.

Create a 7-day social media content plan.

Brand name: {brand_name}
City/Area focus: {city_area}
Property type: {property_type}
Target buyer segment: {target_buyer}
Current offer: {current_offer}
Tone: {tone}

For each day include:
- Post idea/title
- Caption
- Reel/short-video idea
- 5 relevant hashtags

Keep content conversion-focused and locally relevant.
"""

BEAUTY_PROMPT_TEMPLATE = """You are a social media marketing expert for beauty salons and clinics.

Create a 7-day social media content plan.

Brand name: {brand_name}
City/Area focus: {city_area}
Business type: {business_type}
Primary service: {primary_service}
Target audience: {target_audience}
Current offer: {current_offer}
Tone: {tone}

For each day include:
- Post idea/title
- Caption
- Reel/short-video idea
- 5 relevant hashtags

Make the content aspirational, engaging, and booking-oriented.
"""

POLITICS_PROMPT_TEMPLATE = """You are a campaign communication strategist for political digital outreach.

Create a 7-day social media communication plan.

Campaign name: {campaign_name}
Constituency/Region: {region}
Candidate name: {candidate_name}
Campaign objective: {campaign_objective}
Voter segment: {voter_segment}
Key promise/message: {key_message}
Tone: {tone}

For each day include:
- Post theme
- Caption copy
- Short-video/reel concept
- 5 relevant hashtags

Keep language public-friendly, positive, and action-oriented.
"""
