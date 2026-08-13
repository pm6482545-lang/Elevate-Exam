import pandas as pd

def calculate_test_blueprint(target_grade, target_term, total_marks):
    """
    Uses Pandas to create a specification grid based on cumulative KICD rules.
    Example: Grade 8 Term 2 = 40% Grade 7 Content + 60% Grade 8 Content.
    """
    # Curriculum structure rules mapped for the engine
    curriculum_data = [
        {"grade": target_grade, "strand": "Core Subject Content Area 1", "weight_factor": 1.5},
        {"grade": target_grade, "strand": "Core Subject Content Area 2", "weight_factor": 1.0},
        {"grade": "Prior Grade", "strand": "Cumulative Revision Area", "weight_factor": 0.8},
    ]
    df = pd.DataFrame(curriculum_data)
    
    # Calculate effective weight distribution percentages
    df['effective_weight'] = df['weight_factor'] / df['weight_factor'].sum()
    df['marks_allocated'] = (df['effective_weight'] * total_marks).round()
    
    # Balance any rounding remainders to ensure exact mark totals
    remainder = total_marks - df['marks_allocated'].sum()
    if remainder != 0:
        df.loc[df.index[0], 'marks_allocated'] += remainder

    return df.to_dict(orient='records')
