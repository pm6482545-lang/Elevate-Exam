from flask import Flask, request, jsonify
from generator import build_knec_prompt

app = Flask(__name__)

@app.route('/api/generate-exam', methods=['POST'])
def generate_exam():
    try:
        data = request.json
        grade = data.get('grade')
        subject = data.get('subject')
        term = data.get('term')
        total_marks = data.get('total_marks', 100)

        result = build_knec_prompt(grade, subject, term, total_marks)

        return jsonify({
            "success": True,
            "message": "Elevate Kenya Predictions engine successfully compiled specifications.",
            "data": result
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
