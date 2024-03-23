import pandas as pd
import re
from collections import Counter
from typing import List, Tuple
from helpers.mentions import extract_mentions

def process_chunk(chunk: pd.DataFrame) -> Counter:
    """
    Processes a chunk of the dataset to count mentions.
    """
    mentions_list = chunk['content'].apply(extract_mentions).explode().tolist()
    mentions_count = Counter(mentions_list)
    return mentions_count

def aggregate_counts(counters: list) -> Counter:
    """
    Aggregates counts from a list of Counter objects.
    """
    total_counts = Counter()
    for counter in counters:
        total_counts.update(counter)
    return total_counts

def find_top_influencers(file_path: str, chunksize: int = 10000, top_n: int = 10):
    """
    Finds the top N influencers by processing the dataset in chunks.
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
    