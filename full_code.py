import uuid
import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
import asyncio

# Define the chunk size for pandas to process at a time
chunk_size = 10000

# Data Processing section 
async def process_csv(file: UploadFile) -> BytesIO:
    # Read CSV file into pandas dataframe
    df = pd.read_csv(file.file, chunksize=chunk_size)

    buffer = BytesIO()

    # Initialize a dataframe to store the total number of plays for each song and date
    total_plays_df = pd.DataFrame(columns=['Song', 'Date', 'Total Number of Plays'])

    for chunk in df:
        chunk['Date'] = pd.to_datetime(chunk['Date'], yearfirst=True) 
        df_sum = chunk.groupby(['Song', 'Date']).sum()
        df_sum = df_sum.reset_index()
        df_sum.rename(columns={'Number of Plays': 'Total Number of Plays'}, inplace=True)
        # Update the total number of plays for each song and date
        total_plays_chunk = df_sum.groupby(['Song', 'Date'])['Total Number of Plays'].sum().reset_index()
        total_plays_df = total_plays_df.append(total_plays_chunk, ignore_index=True)

    # Group the total plays dataframe by song and date and compute the sum
    total_plays_df = total_plays_df.groupby(['Song', 'Date']).sum().reset_index()

    # Export the total number of plays DataFrame to a new CSV file
    total_plays_df.to_csv(buffer, index=False, header=not buffer.tell())

    # Write processed data to buffer
    buffer.seek(0)
    return buffer

app = FastAPI()
tasks = {}

# Endpoint 1 Schedule file to processing
@app.post("/process_csv/")
async def schedule_csv(file: UploadFile):
    task_id = str(uuid.uuid4())
    tasks[task_id] = asyncio.create_task(process_csv(file))
    return {"task_id": task_id}

# Endpoint 2 Download the result 
@app.get("/download_csv/{task_id}")
async def download_csv (task_id: str):
    task = tasks[task_id]
    buffer = await task
    return StreamingResponse(buffer, media_type='text/csv', headers={'Content-Disposition': 'attachment; filename="answer.csv"'})
    del tasks[task_id]
