# FastAPI and Pandas Data Processing Example

This project is a simple example of using FastAPI and Pandas to create a web API for processing data. The API provides endpoints for uploading CSV files, performing data analysis, and returning the results in csv format as a new file. The purpose of this project is to showcase my skills with FastAPI and data processing with Pandas.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/juanmunozar/processing-csv-file-using-fastAPI
cd your_project
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

2. Upload a CSV file using the `/upload` endpoint:

```bash
curl -X POST -F "file=@data.csv" http://localhost:8000/upload
```

3. The file is going to be processed asynchroniousnly, so you can upload several files at a time 

4. Download the results as a new csv file with the `/download` endpoint.

## API Endpoints

### `POST /upload`

This endpoint accepts a CSV file and saves it to the server for processing. The file must be sent as a multipart/form-data POST request.

### `GET /download`

This endpoint performs data analysis on the uploaded CSV file and returns the results in csv format as a new file.

## Contributing

If you would like to contribute to this project, please submit a pull request or open an issue.
