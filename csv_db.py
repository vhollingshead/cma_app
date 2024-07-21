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
        print("Match on first try")
        return filtered_df.iloc[0]["Established_Response_Tagalog"]
    else:
        # Check for substring match in 'Sub_Topic_Question'
        filtered_df_check = df[(df['Main_Topic'] == level1) & (df['Sub_Topic'] == level2)]
        
        # Get the first 100 characters of the level3 question
        level3_substring = level3[:50]
        
        # Find rows where 'Sub_Topic_Question' contains the substring
        substring_match_df = filtered_df_check[filtered_df_check['Sub_Topic_Question'].str.contains(level3_substring, na=False)]
        
        if not substring_match_df.empty:
            print("Match on second try")

            return substring_match_df.iloc[0]["Established_Response_Tagalog"]
        
        print("No Match")
        print("Here is the Main Topic", level1)
        print("Here is the Sub Topic", level2)
        print('Here is the Sub Topic Question:', level3)
        print('Here is the Sub Topic substring:', level3_substring)
        filtered_df_check_check = df[(df['Main_Topic'] == level1) & (df['Sub_Topic'] == level2)]
        print("The size of this df is:", filtered_df_check_check['Sub_Topic_Question'].size)
        for question in filtered_df_check_check.iloc[:]['Sub_Topic_Question']:
            print(question)
        return "Ako ay humihingi ng paumanhin. Hindi ko masagot ang tanong na iyon mangyaring sumangguni sa Center for Migrant Advocacy Direct Assistance para sa tulong: https://www.facebook.com/centerformigrantadvocacyph/"
