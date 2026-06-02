from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    # Placeholder: implement sales rep search logic here
    return jsonify({'results': [], 'query': query})

if __name__ == '__main__':
    app.run(debug=False)
