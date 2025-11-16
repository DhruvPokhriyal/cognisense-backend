-- 1. The "Profiles" table
-- This table links to Supabase Auth and stores public user data.
CREATE TABLE public.profiles (
  -- This "id" is both the Primary Key and the Foreign Key.
  -- It directly references the id from auth.users.
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  
  username TEXT,
  avatar_url TEXT,
  
  -- Add any other public profile fields you need
  
  CONSTRAINT username_length CHECK (char_length(username) >= 3)
);

-- 2. Your Page View Sessions Table
-- This table now references public.profiles(id)
CREATE TABLE public.page_view_sessions (
    session_id BIGSERIAL PRIMARY KEY,
    
    -- This now correctly links to your profiles table
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    url TEXT NOT NULL,
    domain VARCHAR(255) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL
);

-- 3. Your Content Analysis Table
CREATE TABLE public.content_analysis (
    analysis_id BIGSERIAL PRIMARY KEY,
    
    -- This now correctly links to your profiles table
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    page_url TEXT NOT NULL UNIQUE,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    happy_score DECIMAL(5, 4) DEFAULT 0.0,
    sad_score DECIMAL(5, 4) DEFAULT 0.0,
    angry_score DECIMAL(5, 4) DEFAULT 0.0,
    neutral_score DECIMAL(5, 4) DEFAULT 0.0,
    dominant_emotion VARCHAR(50),
    system_suggested_category VARCHAR(50)
);

-- 4. Your User-Specific Categories Table
CREATE TABLE public.user_domain_categories (
    user_category_id BIGSERIAL PRIMARY KEY,
    
    -- This now correctly links to your profiles table
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    domain_pattern VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority INT DEFAULT 1,
    
    -- A user can only categorize a pattern once
    UNIQUE (user_id, domain_pattern)
);


CREATE TABLE public.user_domain_limits (
    limit_id BIGSERIAL PRIMARY KEY,

    -- Link to your profiles table
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

    -- Domain/platform for which limit is applied
    domain VARCHAR(255) NOT NULL,

    -- Allowed time per day in MINUTES
    allowed_minutes INT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- A user can set only one daily limit per domain
    UNIQUE (user_id, domain)
);