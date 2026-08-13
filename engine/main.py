import os
from flask import Flask, request, jsonify, send_from_directory
from .generator import build_knec_prompt
from .compiler import prepare_pdf_latex

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
        custom_instructions = data.get('custom_instructions', '')

        # 1. Build strict custom prompt and calculate blueprint
        result = build_knec_prompt(grade, subject, term, total_marks, custom_instructions)

        # 2. Prepare the LaTeX output file
        sample_generated_content = f"\\section*{{{subject} - {grade}}}\n\\noindent \\textbf{{Custom Instructions Applied:}} {custom_instructions}\n\n\\begin{{enumerate}}\n\\item Sample generated question based on user custom settings...\n\\end{{enumerate}}"
        latex_file = prepare_pdf_latex(sample_generated_content)

        return jsonify({
            "success": True,
            "message": "Exam specifications and custom LaTeX parameters compiled successfully.",
            "data": {
                "blueprint": result["blueprint"],
                "prompt_used": result["prompt"],
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
