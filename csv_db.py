import pandas as pd
basic_qa_csv_file_path = "repository/translated_responses.csv"

def get_value_from_csv(level1, level2, level3, csv_file=basic_qa_csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter the DataFrame based on the provided levels
    filtered_df = df[(df['Main_Topic'] == level1) & (df['Sub_Topic'] == level2) & (df['Sub_Topic_Question'] == level3)]
    
    # Check if we have any matching rows
    if not filtered_df.empty:
        # Return the value from the first matching row
        return filtered_df.iloc[0]["Established_Response_Tagalog"]
    else:
        return "Ako ay humihingi ng paumanhin. Hindi ko masagot ang tanong na iyon mangyaring sumangguni sa Center for Migrant Advocacy Direct Assistance para sa tulong: https://www.facebook.com/centerformigrantadvocacyph/"





