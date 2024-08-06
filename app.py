from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

def duplicate_dqm(df_raw, df_dq):
    # Initialize an empty list to store the results
    results = []
    
    # Filter the DQ dataframe to get rows where DQM_CD is 1
    df_dq_selected = df_dq[df_dq['DQM_CD'] == 1]
    
    # Get the list of columns to check for duplicates
    selected_columns = df_dq_selected['Column_Name'].tolist()
    
    # Check for duplicates in the entire dataframe
    duplicate_count = df_raw.duplicated().sum()
    status = "Duplicates Found" if duplicate_count > 0 else "No Duplicate Found in Data"
    
    # Append the overall duplicate check result to the results list
    results.append({
        "File_Name": df_dq_selected['File_Name'].values[0],
        "DQM_CD": 0,
        "DQM_Type": "Duplicate Data Check",
        "Column_Name": "",
        "Threshhold": 0,
        "Status": status,
        "Count": duplicate_count
    })
    
    # Check for duplicates in each specified column
    for column in selected_columns:
        if column in df_raw.columns:
            duplicate_count = df_raw[column].duplicated().sum()
            status = "Fail" if duplicate_count > 0 else "Pass"
            results.append({
                "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
                "DQM_CD": 1,
                "DQM_Type": "Duplicate Check",
                "Column_Name": column,
                "Threshhold": 0,
                "Status": status,
                "Count": duplicate_count
            })
        else:
            # If the column does not exist in the raw dataframe
            results.append({
                "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
                "DQM_CD": 1,
                "DQM_Type": "Duplicate Check",
                "Column_Name": column,
                "Threshhold": 0,
                "Status": "Fail",
                "Count": duplicate_count
            })
    
    return results

def missing_val_dqm(df_raw, df_dq):
    # Initialize an empty list to store the results
    results = []
    
    # Filter the DQ dataframe to get rows where DQM_CD is 2
    df_dq_selected = df_dq[df_dq['DQM_CD'] == 2]
    
    # Get the list of columns to check for missing values
    selected_columns = df_dq_selected['Column_Name'].tolist()
    
    # Check for missing values in each specified column
    for column in selected_columns:
        if column in df_raw.columns:
            missing_count = df_raw[column].isnull().sum()
            threshold = df_dq_selected[df_dq_selected['Column_Name'] == column]['Threshhold'].iloc[0]
            status = "Fail" if missing_count > threshold else "Pass"
            results.append({
                "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
                "DQM_CD": 2,
                "DQM_Type": "Null Check",
                "Column_Name": column,
                "Threshhold": threshold,
                "Status": status,
                "Count": missing_count
            })
        else:
            # If the column does not exist in the raw dataframe
            results.append({
                "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
                "DQM_CD": 2,
                "DQM_Type": "Null Check",
                "Column_Name": column,
                "Threshhold": df_dq_selected[df_dq_selected['Column_Name'] == column]['Threshhold'].values[0],
                "Status": "Column Does Not Exist",
                "Count": 0
            })
    
    return results

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # Get file paths from the POST request
        raw_file_path = request.json.get('raw_file_path')
        dq_file_path = request.json.get('dq_file_path')

        # Read the Excel files into DataFrames
        df_raw = pd.read_excel(raw_file_path)
        df_dq = pd.read_excel(dq_file_path)

        # Perform duplicate and missing value checks
        duplicate_check_results = duplicate_dqm(df_raw, df_dq)
        missing_value_check_results = missing_val_dqm(df_raw, df_dq)

        # Combine all results into a single DataFrame
        all_results = duplicate_check_results + missing_value_check_results
        results_df = pd.DataFrame(all_results)

        # Save the results to a CSV file
        output_file_path = 'data_quality_check_results.csv'
        results_df.to_csv(output_file_path, index=False)

        # Send the CSV file as a downloadable attachment
        return send_file(output_file_path, as_attachment=True)

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
