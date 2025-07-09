import os
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

# 環境変数
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")  # OAuth2 access_token
PROMPT = "AIについて、Vtuberのユナ・ゼータ5として明るく可愛くつぶやいてください。140文字以内で。"

# Geminiでツイート内容を生成
def generate_tweet():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT}
                ]
            }
        ]
    }
    response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")

    candidates = response.json()["candidates"]
    text = candidates[0]["content"]["parts"][0]["text"].strip()
    return text

# X (Twitter) に投稿
def post_to_twitter(text):
    bearer_token = os.getenv("TWITTER_ACCESS_TOKEN")
    client = tweepy.Client(bearer_token=bearer_token)
    response = client.create_tweet(text=text)
    print("✅ 投稿完了:", response.data["id"])


# 実行
if __name__ == "__main__":
    tweet = generate_tweet()
    print("生成されたツイート:", tweet)
    post_to_twitter(tweet)
