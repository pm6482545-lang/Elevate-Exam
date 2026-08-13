-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table for storing KICD curriculum-aligned exam blueprints and rules
CREATE TABLE exam_blueprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grade_level TEXT NOT NULL,          -- e.g., 'Grade 8', 'Grade 9'
    subject TEXT NOT NULL,            -- e.g., 'Integrated Science', 'Mathematics'
    term TEXT NOT NULL,               -- e.g., 'Term 1', 'Term 2', 'Term 3'
    paper_number INT DEFAULT 1,       -- Supports Paper 1 and Paper 2 (e.g., for Integrated Science)
    
    -- Cumulative syllabus weighting rule (incorporating prior grade rules)
    syllabus_weight_distribution JSONB NOT NULL, 

    -- User-defined structural rules (Sections count, marks per section, question counts)
    user_section_config JSONB NOT NULL, 

    -- Formatting rules (e.g., 2-column layout, 2x2 matrix options, vertical dividers)
    formatting_preferences JSONB DEFAULT '{
        "mcq_layout": "2x2_matrix",
        "column_format": "two_column_with_vertical_rule",
        "answer_shuffling": true
    }'::jsonb,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Table to store generated exam sessions and history
CREATE TABLE exam_generation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id UUID REFERENCES exam_blueprints(id),
    user_id TEXT, 
    session_parameters JSONB NOT NULL, 
    generated_content JSONB NOT NULL,  
    status TEXT DEFAULT 'draft',       
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);
