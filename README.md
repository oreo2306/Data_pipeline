# Data Cleaning Pipeline

This Flask application provides endpoints to perform data quality checks on uploaded Excel files, specifically for checking duplicate data and missing values. This framework can be reused to add more tasks. 

## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Postman (for testing the API)
- Visual Studio Code (for running the script)
- The Source file that you want to pass into the pipeline
- The configurable dq_config file(shared as sample in files folder) where you would list the configurable values
  
## Installation

1. Clone the repository
3. **Install dependencies:**
    Make sure you have a `requirements.txt` file and run the following command in bash:
    ```
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the Flask app:**
    ```bash
    python app.py
    ```
    The application will start on `http://127.0.0.1:5000`.

## API Endpoints

### `/run_script`

- **Method:** `POST`
- **Description:** Processes the raw and DQ Excel files to perform data quality checks for duplicates and missing values.

#### Request Body

- `raw_file_path`: Path to the raw Excel file.
- `dq_file_path`: Path to the DQ_Config Excel file.

#### Example Request with Postman

1. Open Postman and create a new `POST` request.
2. Set the URL to `http://127.0.0.1:5000/run_script`.
3. Go to the `Body` tab, select `raw`, and choose `JSON` from the dropdown.
4. Add the following JSON:
    ```json
    {
        "raw_file_path": "path/to/raw_file.xlsx",
        "dq_file_path": "path/to/dq_file.xlsx"
    }
    ```
5. Click `Send` to execute the request.
6. If successful, a CSV file named `data_quality_check_results.csv` will be downloaded.

#### Example Response

- **Success:** A CSV file with the data quality check results will be downloaded.
- **Error:** A JSON response with the error message.

```json
{
    "error": "Error message"
}
```

## Code Explanation

- **app.py**: This is the main file containing the Flask application.
- **duplicate_dqm**: This function checks for complete duplicates or duplicate data in the specified list of columns in the provided dataframe.
- **missing_val_dqm**: This function checks for missing values with the configurable parameters (columns, Accepted threshold of the missing values)

- Both DQM functions return the results as a list of dictionaries.
## Error Handling

If any error occurs during the processing, the API will return a JSON response with the error message and a 400 status code.

```json
{
    "error": "Detailed error message"
}
```

## Conclusion

This Flask application allows you to perform data quality checks on Excel files. Following the installation and usage instructions, you can easily set up and test the API using Postman.

## Sample Snippet
![image](https://github.com/user-attachments/assets/ef1f73e8-9b2c-4e0c-bf98-42350b57b1b7)

