###################################################
# Author: Dheeraj Vittal Shenoy
# Filename: comp_average_sem.py
# Date: 10-18-2023
# Computes the average SGPA from given files and displays the result in a sorted manner
###################################################

import pandas as pd
from IPython.display import HTML

files = ["sem1.csv", "sem2.csv", "sem3.csv"]
colnames = ["USN", "Name", "SGPA"]
dfs = [] # store dataframes

for i in range(len(files)):
    dfs.append(pd.read_csv(files[i], header = 0))

result_df = pd.merge(dfs[0], dfs[1], on='USN', how='left')
result_df = result_df.drop(columns='Name_y')
result_df = pd.merge(result_df, dfs[2], on='USN', how='left')
result_df = result_df.drop(columns='Name')

result_df.rename(columns={"SGPA_x" : "SEM 1",
                          "SGPA_y" : "SEM 2",
                          "SGPA" : "SEM 3",
                          "Name_x" : "Name"}, inplace=True)

result_df["TOTAL"] = result_df["SEM 1"] + result_df["SEM 2"] + result_df["SEM 3"]
result_df["AVG"] = result_df["TOTAL"] / 3
result_df = result_df.sort_values(by='AVG', ascending=False, na_position='last')
result_df.reset_index(drop = True, inplace = True)
result_df.drop(columns={"SEM 1", "SEM 2", "SEM 3", "TOTAL"}, inplace = True)
result_df.to_csv("sem_3_avg.csv", na_rep='NaN', index = False)
print(result_df)
html_table = result_df.to_html(index=False)

def style_dataframe(df):
    return df.style \
             .set_properties(**{'font-size': '12pt', 'border-collapse': 'collapse'}) \
             .set_table_styles([{'selector': 'thead', 'props': 'color: #333; background-color: #f2f2f2;'},
                                {'selector': 'tbody', 'props': 'border-bottom: 1px solid #ddd;'},
                                {'selector': 'th, td', 'props': 'padding: 5px; text-align: left; border-bottom: 1px solid #ddd;'},
                                {'selector': 'th', 'props': 'background-color: #4CAF50; color: white;'}])


result_df = style_dataframe(result_df)
result_df.to_html('output_table.html', index=False)
