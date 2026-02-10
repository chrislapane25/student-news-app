from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Student News App is running 🚀"
    })

if __name__ == "__main__":
    app.run(debug=True)

#!/usr/bin/env python3
"""
Student News App - Flask Web Application
"""
from flask import Flask, jsonify, render_template
import os
import sys

# Add services directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

# Import your services (create these later)
try:
    from services.news_service import get_news
    from services.summary_service import summarize_article
except ImportError:
    # Fallback for development
    def get_news(category=None, limit=10):
        return [{"title": "Sample News", "content": "Sample content", "category": category or "general"}]
    
    def summarize_article(text, max_length=150):
        return text[:max_length] + "..." if len(text) > max_length else text

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # You'll create this template later

# Main news route - all categories
@app.route('/news')
def news_all():
    """Get news from all categories"""
    try:
        news_items = get_news(limit=20)
        return jsonify({
            "status": "success",
            "count": len(news_items),
            "news": news_items
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Business news route
@app.route('/news/business')
def news_business():
    """Get business news"""
    try:
        news_items = get_news(category="business", limit=15)
        return jsonify({
            "status": "success",
            "category": "business",
            "count": len(news_items),
            "news": news_items
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Politics news route
@app.route('/news/politics')
def news_politics():
    """Get politics news"""
    try:
        news_items = get_news(category="politics", limit=15)
        return jsonify({
            "status": "success",
            "category": "politics",
            "count": len(news_items),
            "news": news_items
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Entertainment news route
@app.route('/news/entertainment')
def news_entertainment():
    """Get entertainment news"""
    try:
        news_items = get_news(category="entertainment", limit=15)
        return jsonify({
            "status": "success",
            "category": "entertainment",
            "count": len(news_items),
            "news": news_items
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Technology news route
@app.route('/news/technology')
def news_technology():
    """Get technology news"""
    try:
        news_items = get_news(category="technology", limit=15)
        return jsonify({
            "status": "success",
            "category": "technology",
            "count": len(news_items),
            "news": news_items
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Summary route (bonus)
@app.route('/summary/<path:url>')
def get_summary(url):
    """Get summary of a news article"""
    try:
        # In a real app, you'd fetch the article content from URL
        summary = summarize_article(f"Content from {url}")
        return jsonify({
            "status": "success",
            "url": url,
            "summary": summary
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Health check route
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "student-news-app"})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Route not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)