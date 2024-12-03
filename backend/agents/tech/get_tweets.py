import tweepy
import csv
import os

# 替换为你的 API Key 和 Access Token
API_KEY = "aESCheyjuDgBjXCQvQPFOexmm"
API_SECRET = "plwF9czzovGqTQBwcfIaLpOxrsm4aM0zR71gOfy79w3eDGnFdW"
ACCESS_TOKEN = "1612463157305569280-q81xOdvalXcZMYRAgr4M9LVddj76fj"
ACCESS_TOKEN_SECRET = "Gdci68B55lqVDHamlNP6mmsO4AmzzJNN3s92u4RG2nI1R"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFE7xQEAAAAAK3GHAgbpFYM4UYolT7bO4eA86is%3DL1fzeSSTewA2FBc500bH31E2zNsRfRndjk0DaRBLmpKlN0irpG"  # API v2 需要 Bearer Token

# 使用 API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)


def get_tweets_v2(username, max_results=100):
    """
    获取特定博主的推文并返回列表。
    """
    try:
        # 获取用户ID
        user = client.get_user(username=username)
        user_id = user.data.id

        # 获取推文
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "text"]
        )

        return [
            {"username": username, "date": tweet.created_at, "text": tweet.text}
            for tweet in tweets.data
        ]
    except Exception as e:
        print(f"Error for {username}: {e}")
        return []


def save_tweets_to_csv(data, file_path="data/tweets.csv"):
    """
    保存推文到 CSV 文件。
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 写入 CSV 文件
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "date", "text"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Tweets saved to {file_path}")


if __name__ == "__main__":
    usernames = ["lidangzzz", "oran_ge", "FinanceYF5", "ezshine"]
    all_tweets = []

    # 获取每个用户的推文
    for username in usernames:
        print(f"Fetching tweets for {username}...")
        tweets = get_tweets_v2(username)
        all_tweets.extend(tweets)

    # 保存到 CSV 文件
    save_tweets_to_csv(all_tweets)