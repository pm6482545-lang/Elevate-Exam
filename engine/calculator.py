import os
import pandas as pd
from supabase import create_client, Client

# Initialize Supabase client using your project details
SUPABASE_URL = "https://jakdpkzswcxcspoyoqck.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impha2Rwa3pzd2N4Y3Nwb3lvcWNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY1NDA3MTQsImV4cCI6MjEwMjExNjcxNH0.jCnp-k_oZtHB0LveOZBbMvBSttu3ExoH9I_R5DjC0rc")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def calculate_test_blueprint(target_grade, target_term, total_marks):
    """
    Queries Supabase curriculum blueprints and uses Pandas to calculate
    exact specification weightings for Elevate Kenya Predictions.
    """
    try:
        # Query your Supabase database for the matching grade and term
        response = supabase.table('exam_blueprints').select('*').eq('grade_level', target_grade).eq('term', target_term).execute()
        
        if response.data and len(response.data) > 0:
            blueprint_record = response.data[0]
            curriculum_data = blueprint_record.get('syllabus_weight_distribution', [])
            df = pd.DataFrame(curriculum_data)
        else:
            # Fallback structure if specific blueprint is not yet seeded
            df = pd.DataFrame([
                {"strand": "Primary Strand 1", "weight_factor": 1.5},
                {"strand": "Primary Strand 2", "weight_factor": 1.0}
            ])
            
        # Calculate effective weight distribution percentages
        df['effective_weight'] = df['weight_factor'] / df['weight_factor'].sum()
        df['marks_allocated'] = (df['effective_weight'] * total_marks).round()
        
        # Balance any rounding remainders to ensure exact mark totals
        remainder = total_marks - df['marks_allocated'].sum()
        if remainder != 0 and len(df) > 0:
            df.loc[df.index[0], 'marks_allocated'] += remainder

        return df.to_dict(orient='records')
    except Exception as e:
        # Safe fallback in case of connection exceptions
        return [{"error": str(e), "strand": "Default Assessment Area", "marks_allocated": total_marks}]
