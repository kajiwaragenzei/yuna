import os
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def generate_tweet():
    prompt = "ユナ・ゼータ5として、AIや未来について呟く一言を140字以内で生成してください。かわいさとSF感を少し混ぜて。"
    response = model.generate_content(prompt)
    return response.text.strip()

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
