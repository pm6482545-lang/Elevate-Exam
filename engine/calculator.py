import os
from supabase import create_client, Client

SUPABASE_URL = "https://jakdpkzswcxcspoyoqck.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_CORRECT_SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def calculate_test_blueprint(target_grade, target_term, total_marks):
    """
    Queries Supabase curriculum blueprints for grades 1 through 9.
    """
    try:
        response = supabase.table('exam_blueprints').select('*').eq('grade_level', target_grade).eq('term', target_term).execute()
        
        if response.data and len(response.data) > 0:
            blueprint_record = response.data[0]
            curriculum_data = blueprint_record.get('syllabus_weight_distribution', [])
            records = [dict(item) for item in curriculum_data]
        else:
            records = [
                {"strand": f"{target_grade} Core Strand 1", "weight_factor": 1.5},
                {"strand": f"{target_grade} Core Strand 2", "weight_factor": 1.0}
            ]
            
        if not records:
            return [{"strand": "Default Assessment Area", "marks_allocated": total_marks}]

        total_weight = sum(float(r.get('weight_factor', 1.0)) for r in records)
        if total_weight == 0:
            total_weight = len(records)

        allocated_sum = 0
        processed_records = []
        
        for r in records:
            wf = float(r.get('weight_factor', 1.0))
            effective_weight = wf / total_weight
            marks = round(effective_weight * total_marks)
            
            item = dict(r)
            item['effective_weight'] = effective_weight
            item['marks_allocated'] = marks
            processed_records.append(item)
            allocated_sum += marks

        remainder = total_marks - allocated_sum
        if remainder != 0 and processed_records:
            processed_records[0]['marks_allocated'] += remainder

        return processed_records
    except Exception as e:
        return [{"error": str(e), "strand": "Default Assessment Area", "marks_allocated": total_marks}]
