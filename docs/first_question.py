import pandas as pd

# Define the chunk size for pandas to process at a time
chunk_size = 10000
# Create a pandas file reader object to read the CSV file in chunks
df = pd.read_csv('File1.csv', chunksize=chunk_size)

# Initialize a dataframe to store the total number of plays for each song and date
total_plays_df = pd.DataFrame(columns=['Song', 'Date', 'Total Number of Plays for Date'])

for chunk in df:
    chunk['Date'] = pd.to_datetime(chunk['Date'], yearfirst=True) 
    df_sum = chunk.groupby(['Song', 'Date']).sum()
    df_sum = df_sum.reset_index()
    df_sum.rename(columns={'Number of Plays': 'Total Number of Plays for Date'}, inplace=True)

    # Update the total number of plays for each song and date
    total_plays_chunk = df_sum.groupby(['Song', 'Date'])['Total Number of Plays for Date'].sum().reset_index()
    total_plays_df = total_plays_df.append(total_plays_chunk, ignore_index=True)

# Group the total plays dataframe by song and date and compute the sum
total_plays_df = total_plays_df.groupby(['Song', 'Date']).sum().reset_index()

# Export the total number of plays DataFrame to a new CSV file
total_plays_df.to_csv('answer.csv', index=False)