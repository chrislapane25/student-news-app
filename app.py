from flask import Flask, jsonify, render_template
from services.news_service import get_news

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news")
def news_all():
    news_items = get_news(limit=20)
    return jsonify({
        "status": "success",
        "count": len(news_items),
        "news": news_items
    })


@app.route("/news/<category>")
def news_by_category(category):
    news_items = get_news(category=category, limit=15)
    return jsonify({
        "status": "success",
        "category": category,
        "count": len(news_items),
        "news": news_items
    })


@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "student-news-app"
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Route not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
