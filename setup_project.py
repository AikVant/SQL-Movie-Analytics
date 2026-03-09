import csv
import ast
import sqlite3
import pandas as pd
import os

def safe_to_sql(df, table_name, connection):
    # Cleaning spaces from the column names
    df.columns = df.columns.str.strip()
    
    # Retrieving columns from the database
    cursor = connection.execute(f"PRAGMA table_info({table_name})")
    columns_in_db = [info[1] for info in cursor.fetchall()]
    
    # Keeping only common columns
    cols_to_keep = [c for c in columns_in_db if c in df.columns]
    
    if not cols_to_keep:
        print(f"WARNING: No common columns found for {table_name}!")
        return
    
    # Keep only necessary columns
    df_filtered = df[cols_to_keep].copy()

    # Drop EXACT duplicates to avoid IntegrityErrors
    df_filtered = df_filtered.drop_duplicates()
    
    # Ensure IDs are integers and drop rows with missing IDs to avoid FK violations
    for col in df_filtered.columns:
        if 'id' in col.lower():
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')
            # Drop rows where critical IDs became NaN
            df_filtered = df_filtered.dropna(subset=[col])
            df_filtered[col] = df_filtered[col].astype(int)
    
    # Final duplicate check after ID conversion
    df_filtered = df_filtered.drop_duplicates()

    df_filtered.to_sql(table_name, connection, if_exists='append', index=False)
    print(f"Table {table_name} imported: {len(df_filtered)} rows.")

db_name = "movies_database.db"
if os.path.exists(db_name):
    os.remove(db_name)
    print(f"Old database deleted.")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# IMPORTANT: Disable foreign key constraints for the duration of the import
conn.execute("PRAGMA foreign_keys = OFF;")

# Execute Schema
with open('schema.sql', 'r', encoding='utf8') as f:
    cursor.executescript(f.read())

# Processing keywords (Memory efficient handling)
keyword_set = set() 
movie_keyword_pairs = set() 

try:
    with open('dataset/keywords.csv', encoding="utf8", newline="") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            if not row: continue
            movie_id = int(row[0])
            data = ast.literal_eval(row[1])
            for item in data:
                keyword_set.add((item['id'], item['name']))
                movie_keyword_pairs.add((movie_id, item['id']))
except FileNotFoundError:
    print("Keywords CSV not found. Skipping...")

print("Importing data...")

# Load Parent Tables
safe_to_sql(pd.read_csv('dataset/movie.csv'), 'movie', conn)
safe_to_sql(pd.read_csv('dataset/genre.csv'), 'genre', conn)
safe_to_sql(pd.read_csv('dataset/productioncompany.csv'), 'productioncompany', conn)
safe_to_sql(pd.read_csv('dataset/collection.csv'), 'collection', conn)
pd.DataFrame(list(keyword_set), columns=['id', 'name']).to_sql('keyword', conn, if_exists='append', index=False)

# Load Dependent Tables
pd.DataFrame(list(movie_keyword_pairs), columns=['movie_id', 'keyword_id']).to_sql('haskeyword', conn, if_exists='append', index=False)
safe_to_sql(pd.read_csv('dataset/movie_cast.csv'), 'movie_cast', conn)
safe_to_sql(pd.read_csv('dataset/movie_crew.csv'), 'movie_crew', conn)
safe_to_sql(pd.read_csv('dataset/ratings.csv'), 'ratings', conn)
safe_to_sql(pd.read_csv('dataset/belongsTocollection.csv'), 'belongsTocollection', conn)
safe_to_sql(pd.read_csv('dataset/hasProductioncompany.csv'), 'hasProductioncompany', conn)
safe_to_sql(pd.read_csv('dataset/hasGenre.csv'), 'hasGenre', conn)

# IMPORTANT: Re-enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON;")

conn.close()
print("Database created successfully.")