from django.shortcuts import render
import requests
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.http import JsonResponse

# Use environment variables for security
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "your_default_token_here")
USER_ID = os.getenv("INSTAGRAM_USER_ID", "your_default_user_id_here")

def get_instagram_posts():
    url = f"https://graph.instagram.com/{USER_ID}/media?fields=id,caption&access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url, timeout=10)  # Set timeout for request
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        data = response.json()
        return data.get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Instagram posts: {e}")
        return []  # Return empty list on failure

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    if text:  # Ensure text is not None
        return analyzer.polarity_scores(text)
    return {"compound": 0, "neg": 0, "neu": 0, "pos": 0}  # Default neutral sentiment

def home(request):
    posts = get_instagram_posts()
    analyzed_posts = [
        {"caption": post.get("caption", "No caption"), "sentiment": analyze_sentiment(post.get("caption", ""))}
        for post in posts
    ]
    return render(request, "index.html", {"posts": analyzed_posts})

def api_sentiment_analysis(request):
    """ API endpoint to get sentiment analysis for Instagram posts """
    posts = get_instagram_posts()
    analyzed_posts = [
        {"caption": post.get("caption", "No caption"), "sentiment": analyze_sentiment(post.get("caption", ""))}
        for post in posts
    ]
    return JsonResponse({"posts": analyzed_posts})
