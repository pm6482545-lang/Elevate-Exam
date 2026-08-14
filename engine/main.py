import os
import sys

# Ensure the parent directory is in the path for absolute/relative execution compatibility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

try:
    from engine.generator import build_knec_prompt
    from engine.compiler import prepare_pdf_latex
except ImportError:
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
        data = request.json or {}
        grade = data.get('grade')
        subject = data.get('subject')
        term = data.get('term')
        total_marks = data.get('total_marks', 100)
        custom_instructions = data.get('custom_instructions', '')

        # 1. Build strict custom prompt and calculate blueprint
        result = build_knec_prompt(grade, subject, term, total_marks, custom_instructions)
        
        # 2. Safely initialize OpenAI client at runtime using environment variables
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is missing or empty.")
            
        client = OpenAI(api_key=api_key)

        # 3. Call OpenAI to generate the complete LaTeX exam following user custom rules
        openai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional KNEC exam generator and LaTeX author."},
                {"role": "user", "content": result["prompt"]}
            ],
            temperature=0.7
        )
        
        generated_exam_content = openai_response.choices[0].message.content

        # 4. Prepare the final LaTeX file
        latex_file = prepare_pdf_latex(generated_exam_content)

        return jsonify({
            "success": True,
            "message": "Elevate Kenya Predictions engine successfully generated the custom LaTeX exam paper.",
            "data": {
                "blueprint": result["blueprint"],
                "latex_file_path": latex_file,
                "generated_latex": generated_exam_content
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
