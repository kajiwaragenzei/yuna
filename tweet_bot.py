# tweet_bot.py
import os
from openai import OpenAI
import tweepy
from dotenv import load_dotenv

# Load .env if running locally
load_dotenv()

# OpenAI client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tweet():
    prompt = "ユナ・ゼータ5として、AIや未来について呟く一言を140字以内で生成してください。かわいさとSF感を少し混ぜて。"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

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
