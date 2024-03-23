from typing import List, Tuple
import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed


# chunksize for chunk files
CHUNKSIZE = 1000


def process_chunk(chunk:pd.DataFrame):
    """
        Processes a chunk of the JSON file to obtain the count of messages by date and user.
        
        Parameters:
        - chunk (DataFrame): A chunk of the full DataFrame representing message data.
        
        Returns:
        - DataFrame: A DataFrame grouped by date and user with the count of messages.
    """
    chunk['date'] = chunk['date'].dt.date
    chunk['user'] = chunk['user'].apply(
        lambda x: x['username'] if isinstance(x, dict) and 'username' in x else None)

    return chunk.groupby(['date', 'user']).size().reset_index(name='count')


def combine_results(results:list[pd.DataFrame]):
    """
        Combines the processed chunks' results into a single DataFrame.
        
        Parameters:
        - results (List[DataFrame]): A list of DataFrames representing the processed chunks' results.
    
        Returns:
        - DataFrame: A DataFrame containing the combination of all chunks' results.
    """

    aggregated_df = pd.DataFrame()

    for result in results:
        aggregated_df = pd.concat([aggregated_df, result])

    return aggregated_df


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
        Processes a large JSON file in chunks to find the top 10 users and dates with the most messages.
        
        Uses parallel processing to improve data processing efficiency.
        
        Parameters:
        - file_path (str): The path to the JSON file containing message data.
        
        Returns:
        - List[Tuple[datetime.date, str]]: A list of tuples, where each tuple contains a date and a username,
        representing the top 10 most active users and their corresponding dates.
    """

    futures = []
    
    with ProcessPoolExecutor() as executor:
        for chunk in pd.read_json(file_path, lines=True, chunksize=CHUNKSIZE, convert_dates=['date']):
            futures.append(executor.submit(process_chunk, chunk))

        results = [future.result() for future in as_completed(futures)]

    aggregated_df = combine_results(results)
    final_grouped = aggregated_df.groupby(['date', 'user']).sum().reset_index()
    top_10 = final_grouped.sort_values(by='count', ascending=False).head(10)

    result = list(top_10[['date', 'user']].to_records(index=False))

    return result
