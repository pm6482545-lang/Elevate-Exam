import os
from calculator import calculate_test_blueprint

def build_knec_prompt(grade, subject, term, total_marks):
    """
    Constructs the rigorous prompt logic enforcing KICD curriculum bounds,
    scenario-based design, and 2x2 option layouts.
    """
    blueprint_specs = calculate_test_blueprint(grade, term, total_marks)
    
    system_prompt = f"""
    You are an expert Kenyan National Examinations Council (KNEC) Senior Examiner and curriculum specialist.
    Generate a formal examination paper for {subject} ({grade}, {term}) based on the KICD curriculum design.
    
    SPECIFICATION GRID & WEIGHTINGS:
    {blueprint_specs}
    
    STRICT RULES TO FOLLOW:
    1. Curriculum Boundaries: Draw questions only from sub-strands mapped for this grade and term requirements.
    2. Question Styling: Avoid short direct-recall questions. Write long, descriptive, scenario-based items grounded in realistic Kenyan contexts.
    3. Multiple Choice Format: Provide 4 options (A, B, C, D) structured for a 2x2 matrix layout. Shuffle correct answers evenly.
    4. Output Format: Return structured markdown ready for LaTeX PDF compilation.
    """
    
    return {
        "blueprint": blueprint_specs,
        "prompt": system_prompt
    }
