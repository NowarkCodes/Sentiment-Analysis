import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Replace with your actual Instagram credentials
ACCESS_TOKEN = "IGAATotzjOF5NBZAE83X2djUG1EcVVabWljd3JZAUUtobEVGbVI2N1ZA3dkc0MUd4QldwVlY3ZAzJVZAVVlTUtKQkwwc3FSaEt3aHU2QUhKZATd3NTZAEZAFNFQ3hCSWhNNlQ0UFVpekl1dkY2a240NGg5akdsMmcyOWQ2b1VLb3IxS0JtYwZDZD"  # Get this from Graph API Explorer
USER_ID = "9189421437802018"  # Get this from https://graph.instagram.com/me?fields=id&access_token=YOUR_ACCESS_TOKEN

# Function to fetch Instagram posts
def get_instagram_posts(user_id, access_token):
    url = f"https://graph.instagram.com/{user_id}/media?fields=id,caption&access_token={access_token}"
    response = requests.get(url)
    
    # Debugging: Print API response
    print(f"API Response: {response.status_code}, {response.text}")  
    return response.json()

# Function to analyze sentiment using VADER
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)

# Fetch posts and analyze sentiment
data = get_instagram_posts(USER_ID, ACCESS_TOKEN)

if "data" in data and data["data"]:
    for post in data["data"]:
        caption = post.get("caption", "No caption available")
        sentiment = analyze_sentiment(caption)
        
        print(f"\n📝 Post: {caption}")
        print(f"📊 Sentiment: {sentiment}\n")
else:
    print("🚫 No posts found or API error occurred.")
