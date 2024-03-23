import re
from collections import Counter
import pandas as pd
from typing import List, Tuple
from helpers.emojis import extract_emojis


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Reads a JSON file line by line into a pandas DataFrame, extracts emojis from the 'content' field of each row,
    counts the occurrences of each emoji, and returns the 10 most common emojis with their counts.
    
    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains an emoji and its count, 
        representing the 10 most common emojis found in the file.
    """

    df = pd.read_json(file_path, lines=True)
    
    emoji_counter = Counter()

    for content in df['content']:
        emojis = extract_emojis(content)
        emoji_counter.update(emojis)
    
    return emoji_counter.most_common(10)
