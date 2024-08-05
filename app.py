# from flask import Flask, request, jsonify, send_file
# import pandas as pd

# app = Flask(__name__)

# def perform_dqm_check(df_raw, df_dq, dqm_cd, dqm_type, check_function):
#     results = []
#     df_dq_selected = df_dq[df_dq['DQM_CD'] == dqm_cd]
#     selected_columns = df_dq_selected['Column_Name'].tolist()

#     for column in selected_columns:
#         if column in df_raw.columns:
#             count, threshold, status = check_function(df_raw, column, df_dq_selected)
#             results.append({
#                 "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
#                 "DQM_CD": dqm_cd,
#                 "DQM_Type": dqm_type,
#                 "Column_Name": column,
#                 "Threshhold": threshold,
#                 "Status": status,
#                 "Count": count
#             })
#         else:
#             results.append({
#                 "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
#                 "DQM_CD": dqm_cd,
#                 "DQM_Type": dqm_type,
#                 "Column_Name": column,
#                 "Threshhold": df_dq_selected[df_dq_selected['Column_Name'] == column]['Threshhold'].values[0],
#                 "Status": "Fail",
#                 "Count": None
#             })

#     return results

# def duplicate_check(df_raw, column, df_dq_selected):
#     duplicate_count = df_raw[column].duplicated().sum()
#     status = "Fail" if duplicate_count > 0 else "Pass"
#     return duplicate_count, 0, status

# def missing_value_check(df_raw, column, df_dq_selected):
#     missing_count = df_raw[column].isnull().sum()
#     threshold = df_dq_selected[df_dq_selected['Column_Name'] == column]['Threshhold'].iloc[0]
#     status = "Fail" if missing_count > threshold else "Pass"
#     return missing_count, threshold, status

# @app.route('/run_script', methods=['POST'])
# def run_script():
#     try:
#         raw_file_path = request.json.get('raw_file_path')
#         dq_file_path = request.json.get('dq_file_path')

#         df_raw = pd.read_excel(raw_file_path)
#         df_dq = pd.read_excel(dq_file_path)

#         duplicate_check_results = perform_dqm_check(df_raw, df_dq, 1, "Duplicate Check", duplicate_check)
#         missing_value_check_results = perform_dqm_check(df_raw, df_dq, 2, "Null Check", missing_value_check)

#         all_results = duplicate_check_results + missing_value_check_results
#         results_df = pd.DataFrame(all_results)

#         output_file_path = 'data_quality_check_results.csv'
#         results_df.to_csv(output_file_path, index=False)

#         return send_file(output_file_path, as_attachment=True)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

def duplicate_dqm(df_raw, df_dq):
    results = []
    df_dq_selected = df_dq[df_dq['DQM_CD'] == 1]
    selected_columns = df_dq_selected['Column_Name'].tolist()
    duplicate_count = df_raw.duplicated().sum()
    status = "Duplicates Found" if duplicate_count > 0 else "No Duplicate Found in Data"
    results.append({
                "File_Name": df_dq_selected['File_Name'].values[0],
                "DQM_CD": 0,
                "DQM_Type": "Duplicate Data Check",
                "Column_Name": "",
                "Threshhold": 0,
                "Status": status,
                "Count": duplicate_count
            })
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
    results = []
    df_dq_selected = df_dq[df_dq['DQM_CD'] == 2]
    selected_columns = df_dq_selected['Column_Name'].tolist()

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
            results.append({
                "File_Name": df_dq_selected[df_dq_selected['Column_Name'] == column]['File_Name'].values[0],
                "DQM_CD": 2,
                "DQM_Type": "Null Check",
                "Column_Name": column,
                "Threshhold": df_dq_selected[df_dq_selected['Column_Name'] == column]['Threshhold'].values[0],
                "Status": "Fail",
                "Count": missing_count
            })
    
    return results

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        raw_file_path = request.json.get('raw_file_path')
        dq_file_path = request.json.get('dq_file_path')

        df_raw = pd.read_excel(raw_file_path)
        df_dq = pd.read_excel(dq_file_path)

        duplicate_check_results = duplicate_dqm(df_raw, df_dq)
        missing_value_check_results = missing_val_dqm(df_raw, df_dq)

        # Combine all results
        all_results = duplicate_check_results + missing_value_check_results
        results_df = pd.DataFrame(all_results)

        output_file_path = 'data_quality_check_results.csv'
        results_df.to_csv(output_file_path, index=False)

        return send_file(output_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)