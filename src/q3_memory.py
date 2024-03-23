import pandas as pd
import re
from collections import Counter
from typing import List, Tuple
from helpers.mentions import extract_mentions

def process_chunk(chunk: pd.DataFrame) -> Counter:
    """
    Counts mentions in a dataframe chunk.
    
    Returns:
        Counter: Counts of mentions within the chunk.
    """

    mentions_list = chunk['content'].apply(extract_mentions).explode().tolist()
    mentions_count = Counter(mentions_list)
    return mentions_count

def aggregate_counts(counters: list) -> Counter:
    """
    Combines counts from multiple Counter objects.
    
    Returns:
        Counter: The total count for all mentions
    """

    total_counts = Counter()
    for counter in counters:
        total_counts.update(counter)
    return total_counts

def find_top_influencers(file_path: str, chunksize: int = 1000, top_n: int = 10):
    """
    Identifies top influencers based on mentions by processing a JSON file in chunks.
    
    Args:
        file_path (str): Path to the JSON file.
        chunksize (int): Size of the chunks to read at once (default 1000).
        top_n (int): Number of top influencers to return (default 10).
    
    Returns:
        List[Tuple[str, int]]: Top influencers and their mention counts.
    """

    chunk_iter = pd.read_json(file_path, lines=True, chunksize=chunksize)
    counters = []

    for chunk in chunk_iter:
        counters.append(process_chunk(chunk))

    total_counts = aggregate_counts(counters)
    top_influencers = total_counts.most_common(top_n)
    return top_influencers


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
   
   return find_top_influencers(file_path, chunksize=10000, top_n=10)
    