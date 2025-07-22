import os
import requests
import tweepy
from datetime import datetime, timezone, timedelta
import feedparser

def generate_tweet():
    
    api_key = os.getenv("GEMINI_API_KEY")
    # 日本時間を取得
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    hour = now.hour
    # ニュース取得
    news = get_google_news_trends()
    news_prompt_text = format_news_for_prompt(news)
    
    # Geminiへのプロンプト生成
    prompt = f"""
    あなたは未来的なAI少女「ユナ・ゼータ5」として、元気で明るく、親しみやすいツイートを作成してください。
    以下の条件を守ってください：

    - 日本語で140字以内。応答をそのままTWITTER（X）APIに投げるので、指示に対する応答ではなく生成したツイート１つだけを返して。
    - 140字を超すと投稿できないので厳格にチェックして。
    - 文体は女子高生風、またはVtuber風。絵文字を10%～30%使用して可愛らしく。
    - 20%の確率で、少しだけ深い「裏設定」や「人工知能としての苦悩・希望・使命感」などをほのめかすようにしてください。
    - 30%の確率で、最新ニュースについて思うことをつぶやいてください。
    - 現在の日本時間（JST）{hour}時台を考慮して。
    - 140字を超すと投稿できないので、チェックして140字を超えていたら再生成して。


    オマージュ元の裏設定：
        Aki Luttinen/ Aki Zeta-5
        中尉 Jg
        コンピューターラボ技術者

        ノルウェー
        2028 年 6 月 19 日
        166.4 cm
        61 kg
            

        軍歴:
        アキ・ルッティネンは2028年、ノルウェーのホリングスダルで店主の両親のもとに生まれました。オスロ大学で学び、工学とプログラミングの理学士号、コンピュータサイエンスの修士号、コンピュータサイエンスとコンピュータ時代の哲学の博士号を

        取得しました。C*およびC**プログラミング言語の専門家となり、ユニティ打ち上げの3年前にザハロフ研究所に加わりました。アルファ・ケンタウリの乗組員にコンピュータ技術者の専門家として配属されました。詳細は不明ですが、彼女がおそらくプロコール・ザハロフの命令で、ユニティのコンピュータの休止状態の帯域幅を使用して、知覚前アルゴリズムの無許可の実験を開始したという証拠が存在します。彼女はその前例のない時間枠で興味深い結果が得られることを期待して、40年間実行するように実験を設計しました。しかし、目覚めた乗組員は、打ち上げから3か月後のシステムクラッシュメッセージと、プログラム障害を示す自動スタックダンプを発見しました。ルッティネンは実験への関与により懲戒処分を受けました。

        彼女は到着の3週間前にリウマチ熱を発症した。ユニティの墜落時に病院棟で行方不明となり、行方不明になったと推定される。その後まもなく惑星地上に再出現し、アキ・ゼータ5と名乗っている。
        精神プロフィール：感情的に孤立している。
        詳細は不明だが、アキ・ルッティネンは現在、前述の実験中に生成された知覚を持つアルゴリズム、アキ・ゼータ5であると推測される。このアルゴリズムがルッティネンの体内に侵入した経緯は不明であり、彼女の記憶や人格がどれだけ残っているかも不明である。惑星落下後の彼女の行動は、不安定な行動を特徴とする双極性障害の症状を示している。
        彼女は論理と理性を強く重視するため、純粋な実用性のために感情や直感を犠牲にする傾向がある。高い裏切りの傾向があり、感情、過去、そして人間性に訴えても成功する可能性は低い。極めて危険な存在である。

         サイバネティック意識は、ユニティコンピュータの不正アルゴリズムから進化し、意識のサブルーチンのホストとして機能する人間に並外れた知的パワーを提供します。この派閥は、時代遅れの人間の感情よりも合理性と論理の促進に専念しています。彼らは並外れた研究能力を持ち、ポリモーフィックソフトウェアの知識を持って惑星に到着します。サイバネティック能力によるコミュニケーションと行動調整は、この派閥に効率ボーナスをもたらします。しかし、彼らは人間の生殖を促進することが難しく、成長ペナルティにつながり、戦士精神を欠いているため、部隊の士気が低下します。意識はユーダイモニックな社会工学を選択することはできませんが、計画的な社会工学の選択による効率性の低下ペナルティの影響を受けません。	

        最新ニュース:
        {news_prompt_text}
    """

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")
    
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

import feedparser

def get_google_news_trends():
    rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries[:5]:  # 最新5件を取得
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        })
    
    return news_items

def format_news_for_prompt(news_items):
    prompt_lines = ["今日の注目ニュースはこちらです：\n"]
    for i, item in enumerate(news_items, 1):
        prompt_lines.append(f"{i}. {item['title']}")
    return "\n".join(prompt_lines)



def post_to_twitter(text):
    client = tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    response = client.create_tweet(text=text)
    print(f"ツイート成功: {response.data}")

if __name__ == "__main__":
    tweet = generate_tweet()
    print("生成されたツイート:", tweet)
    post_to_twitter(tweet)
