import os
from .calculator import calculate_test_blueprint

def build_knec_prompt(grade, subject, term, total_marks, custom_instructions=""):
    """
    Constructs the rigorous prompt incorporating custom user instructions,
    strict curriculum bounds (Grades 1 to 9, with JSS for 7, 8, 9), and LaTeX format.
    """
    blueprint_specs = calculate_test_blueprint(grade, term, total_marks)
    
    is_jss = grade in ["Grade 7 (JSS)", "Grade 8 (JSS)", "Grade 9 (JSS)"]
    tier_label = "Junior Secondary School (JSS)" if is_jss else "Primary School Level"
    
    system_prompt = f"""
    You are an expert Kenyan National Examinations Council (KNEC) Senior Examiner and curriculum specialist.
    Generate a formal examination paper for {subject} ({grade} - {tier_label}, {term}) based on the KICD curriculum design.
    
    SPECIFICATION GRID & WEIGHTINGS:
    {blueprint_specs}
    
    USER CUSTOM SETTINGS & STRUCTURE:
    {custom_instructions if custom_instructions else "Follow standard KICD guidelines with scenario-based questions and 2x2 option layouts."}
    
    STRICT RULES TO FOLLOW:
    1. Curriculum Boundaries: Strictly adhere to the requested grade ({grade}) and term ({term}) bounds.
    2. User Customization: Follow the user's custom instructions and structural parameters precisely.
    3. Output Format: Return the final examination fully formatted in clean **LaTeX** code (ready for PDF compilation), enclosed in markdown code blocks.
    """
    
    return {
        "blueprint": blueprint_specs,
        "prompt": system_prompt
    }
