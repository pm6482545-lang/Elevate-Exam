import os
from flask import Flask, request, jsonify, send_from_directory
from .generator import build_knec_prompt
from .compiler import prepare_pdf_latex

# Point Flask to the frontend folder located in the parent directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
