# tweet_bot.py（Gemini 2.0 Flash対応）
import os
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_tweet():
    prompt = "ユナ・ゼータ5として、AIや未来について呟く一言を140字以内で生成してください。かわいさとSF感を少し混ぜて。"
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(API_URL, json=body)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def post_to_twitter(text):
    auth = tweepy.OAuth1UserHandler(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_SECRET")
    )
    api = tweepy.API(auth)
    api.update_status(status=text)

if __name__ == "__main__":
    tweet = generate_tweet()
    print("生成されたツイート:", tweet)
    post_to_twitter(tweet)
    print("✅ 投稿完了")
