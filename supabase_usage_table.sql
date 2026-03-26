create extension if not exists "pgcrypto";

create table if not exists public.usage (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  month text not null,
  single_posts int not null default 0,
  weekly_plans int not null default 0,
  calendars int not null default 0
);

create unique index if not exists usage_email_month_idx
  on public.usage (email, month);
