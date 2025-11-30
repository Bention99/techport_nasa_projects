import pandas as pd
import sqlite3
from collections import Counter


def interesting_stats():
    conn = sqlite3.connect("data/techport.db")
    df = pd.read_sql("SELECT * FROM projects", conn)

    print(df)
    avg_views = df["view_count"].mean()

    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    df["duration_days"] = (df["end_date"] - df["start_date"]).dt.days

    average_duration_days = df["duration_days"].mean()

    df["destination_list"] = df["destinationType"].fillna("").apply(
    lambda x: [d.strip() for d in x.split(",")] if x else []
    )

    all_destinations = [d for sublist in df["destination_list"] for d in sublist]

    counts = Counter(all_destinations)

    most_destination, most_count = counts.most_common(1)[0]
    least_destination, least_count = counts.most_common()[-1]

    print("Most mentioned destination:", most_destination, most_count)
    print("Least mentioned destination:", least_destination, least_count)
    print(f"Average Project duration: {average_duration_days} days")
    print(f"Average Project views: {avg_views}")

    conn.close()

if __name__ == "__main__":
    interesting_stats()