

import pandas as pd
from IPython.display import HTML

result_df = pd.read_csv("sem_4_avg.csv")

result_df["TOTAL"] = result_df["SEM 1"] + result_df["SEM 2"] + result_df["SEM 3"] + result_df["SEM 4"]
result_df["AVG"] = result_df["TOTAL"] / 4
result_df = result_df.sort_values(by='AVG', ascending=False, na_position='last')
result_df.reset_index(drop = True, inplace = True)
result_df.to_csv("final.csv", na_rep='NaN', index = False)
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
