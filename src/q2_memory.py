from collections import Counter
import pandas as pd
from typing import List, Tuple
from helpers.emojis import extract_emojis


def q2_memory(file_path: str, chunksize: int = 5000) -> List[Tuple[str, int]]:
    # Inicializar el contador de emojis
    emoji_counter = Counter()
    
    # Procesar el archivo JSON en fragmentos
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunksize):
        for content in chunk['content']:
            emojis = extract_emojis(content)
            emoji_counter.update(emojis)
    
    # Devolver el top 10
    return emoji_counter.most_common(10)
