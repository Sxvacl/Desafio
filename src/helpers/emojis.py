from typing import List, Tuple
import re

def extract_emojis(text: str) -> List[str]:
    """
    Extracts and returns all emojis found in the given text string.
    
    Uses a regular expression pattern to match and find all characters that fall within
    various Unicode ranges designated for emojis.
    
    Returns:
        List[str]: A list of all emojis found in the input text.
    """

    # Regex of emojis for finding in each tweet.
    # Emoticons, Symbols & pictograms, Transport & maps, Additional symbols, More symbols, Dingbats, Miscellaneous Technical symbols
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F700-\U0001FBFF"  
        u"\U0001F900-\U0001FAFF"  
        u"\U00002702-\U000027B0"  
        u"\U00002300-\U000023FF"  
        "]+", flags=re.UNICODE)

    return emoji_pattern.findall(text)
    