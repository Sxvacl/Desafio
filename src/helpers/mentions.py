import re
from typing import List, Tuple

def extract_mentions(text: str) -> List[str]:
    """
    Extracts mentions from a text using a regular expression.
    """
    
    mentions = re.findall(r'@\w+', text)
    return mentions
