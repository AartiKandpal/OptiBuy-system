from flask import Flask, render_template, request, jsonify
from scraper import get_all_prices

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify([])
    data = get_all_prices(query)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)