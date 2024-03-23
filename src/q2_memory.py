from collections import Counter
import pandas as pd
from typing import List, Tuple
from helpers.emojis import extract_emojis


def q2_memory(file_path: str, chunksize: int = 5000) -> List[Tuple[str, int]]:
    """
    Processes a JSON file in chunks to efficiently count emoji frequencies in text.
    
    Args:
        file_path (str): Path to the JSON file with texts under the 'content' key.
        chunksize (int): Number of lines to read into memory at once. Defaults to 5000.
    
    Returns:
        List[Tuple[str, int]]: The 10 most common emojis and their counts.
    
    The function uses a Counter to tally emojis found using `extract_emojis` across the file's 'content'.
    """
    emoji_counter = Counter()
    
   
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunksize):
        for content in chunk['content']:
            emojis = extract_emojis(content)
            emoji_counter.update(emojis)
    
   
    return emoji_counter.most_common(10)
