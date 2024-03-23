from datetime import datetime
from typing import List, Tuple

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Retrieves the top 10 dates with the highest number of tweets per user from a JSON file.
    
    Returns:
        List[Tuple[datetime.date, str]]: List of (date, username) tuples for the top 10 dates.
    """
    
    spark = SparkSession.builder.appName("TwitterDataAnalysis").getOrCreate()

    twitts_df = spark.read.json(file_path)
    reduced_twits_df = twitts_df[['date', 'user']]

    reduced_twits_df = reduced_twits_df.withColumn("date", to_date(col("date")))
    reduced_twits_df = reduced_twits_df.withColumn("user", col("user.username"))

    max_tweets = reduced_twits_df.groupBy("date", "user").count().orderBy(col("count").desc())[['date', 'user']]
    top_10_results = max_tweets.select("date", "user").limit(10).collect()

    result = [(row['date'], row['user']) for row in top_10_results]

    spark.stop()

    return result
