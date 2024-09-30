from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the request.py script
        result = subprocess.run(['python', 'request.py'], capture_output=True, text=True)
        return jsonify({
            'output': result.stdout,
            'error': result.stderr
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

