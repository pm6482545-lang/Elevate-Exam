const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client using environment variables
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

async function generateExamPaper(grade, subject, term, userSectionConfig) {
    // 1. Fetch curriculum blueprint rules from Supabase
    const { data: blueprint, error } = await supabase
        .from('exam_blueprints')
        .select('*')
        .eq('grade_level', grade)
        .eq('subject', subject)
        .eq('term', term)
        .single();

    if (error) {
        throw new Error("Blueprint configuration not found for this specific grade, subject, and term.");
    }

    // 2. Construct the strict KNEC-aligned system prompt incorporating all your rules
    const systemPrompt = `
    You are an expert Kenyan National Examinations Council (KNEC) Senior Examiner and curriculum specialist.
    Generate a formal examination paper for ${subject} (${grade}, ${term}) based on the KICD curriculum design.
    
    STRICT RULES TO FOLLOW:
    1. Curriculum Boundaries: Draw questions only from sub-strands mapped for this grade and term. Incorporate cumulative prior-grade weightings where specified: ${JSON.stringify(blueprint.syllabus_weight_distribution)}.
    2. Question Styling: Avoid short direct-recall questions. Write long, descriptive, scenario-based questions grounded in real-world Kenyan contexts (local environments, practical settings, realistic data tables).
    3. User-Defined Structure: Adhere strictly to the requested section counts, question numbers, and marks defined by the user: ${JSON.stringify(userSectionConfig)}.
    4. Multiple Choice Format: Provide 4 options (A, B, C, D) structured for a 2x2 matrix layout. Actively shuffle correct answers across options to eliminate patterns.
    `;

    return {
        blueprintUsed: blueprint,
        promptToSendToAI: systemPrompt
    };
}

module.exports = { generateExamPaper };
