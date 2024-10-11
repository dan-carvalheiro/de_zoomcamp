# libraries
import argparse
import os
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url

    # extract data
    data = os.system(f"curl {url} -o data.parquet")
    df = pd.read_parquet("data.parquet")

    # remove data file from local drive
    os.remove("data.parquet")

    # transform data
    df["lpep_pickup_datetime"] = pd.to_datetime(df.lpep_pickup_datetime)
    df["lpep_dropoff_datetime"] = pd.to_datetime(df.lpep_dropoff_datetime)

    # connect to pg database
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    engine.connect()

    # load data to database
    df.head(n=0).to_sql(f"{table}", index=False, con=engine, if_exists="replace")
    df.to_sql(f"{table}", index=False, con=engine, if_exists="append")

    # return statement that data was successfully loaded
    print(f"data upload complete for {table} table!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ingestion script for homework 1 question 3")
    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--database", help="database name for postgres")
    parser.add_argument("--table", help="table name for postgres")
    parser.add_argument("--url", help="url for postgres")

    args = parser.parse_args()
    main(args)
