import pandas as pd
import re
from typing import List, Tuple
from helpers.mentions import extract_mentions

def load_tweets(file_path: str) -> pd.DataFrame:
    
    return pd.read_json(file_path, lines=True)

def count_user_mentions(tweets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates the count of user mentions from tweet contents.
    
    Args:
        tweets_df (pd.DataFrame): DataFrame with tweets data, expected to have a 'content' column.
    
    Returns:
        pd.DataFrame: DataFrame with usernames and their respective mention counts.
    """
    all_mentions = tweets_df['content'].apply(extract_mentions).explode()

    mentions_count = all_mentions.value_counts().reset_index()
    mentions_count.columns = ['Username', 'Mentions']
    return mentions_count

def find_top_influencers(file_path: str, top_n: int = 10) -> List[Tuple[str, int]]:
 
    tweets_df = load_tweets(file_path)
    user_mentions_count = count_user_mentions(tweets_df)
    top_mentions = user_mentions_count.head(top_n)
    return list(zip(top_mentions['Username'], top_mentions['Mentions']))

def get_top_influencers_by_time(file_path: str) -> List[Tuple[str, int]]:
    return find_top_influencers(file_path)


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    return get_top_influencers_by_time(file_path)
    