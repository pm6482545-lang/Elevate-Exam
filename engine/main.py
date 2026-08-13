from flask import Flask, request, jsonify
from generator import build_knec_prompt
from compiler import prepare_pdf_latex

app = Flask(__name__)

@app.route('/api/generate-exam', methods=['POST'])
def generate_exam():
    try:
        data = request.json
        grade = data.get('grade')
        subject = data.get('subject')
        term = data.get('term')
        total_marks = data.get('total_marks', 100)

        # 1. Build prompt and calculate blueprint from Supabase
        result = build_knec_prompt(grade, subject, term, total_marks)

        # 2. Prepare the LaTeX output file using the template compiler
        # For now, we pass a placeholder for generated exam content string
        sample_generated_content = "\\noindent \\textbf{1.} [AI Generated content based on blueprint will appear here...]"
        latex_file = prepare_pdf_latex(sample_generated_content)

        return jsonify({
            "success": True,
            "message": "Elevate Kenya Predictions engine successfully compiled specifications and LaTeX template.",
            "data": {
                "blueprint": result["blueprint"],
                "latex_file_path": latex_file
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
