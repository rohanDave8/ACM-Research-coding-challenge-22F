import pandas as pd
from re import sub
import numpy as np
import scipy.stats as st
import plotly.express as px
import matplotlib.pyplot as plt
    
rawdf = pd.read_csv("cars_raw.csv")

statePricesJSON = {}

for i in rawdf.index:
    if len(rawdf['State'][i]) == 2 and rawdf['Price'][i][0] == '$':
        if rawdf['State'][i] not in statePricesJSON:
            statePricesJSON[rawdf['State'][i]] = [sub(r'[^\d.]', '', rawdf['Price'][i])]
        else:
            statePricesJSON[rawdf['State'][i]].append(sub(r'[^\d.]', '', rawdf['Price'][i]))

df = pd.DataFrame(columns = ['State', 'Mean Price ($)', 'CILow', 'CIHigh'])

for i in statePricesJSON:
    stateList = [eval(j) for j in statePricesJSON[i]]
    dfRow = [i, np.mean(stateList), 'degree of freedom = 0', 'degree of freedom = 0']
    if len(stateList) > 1:
        stateCI = st.norm.interval(confidence=0.90, loc=np.mean(stateList), scale=st.sem(stateList))
        dfRow[2] = stateCI[0]
        dfRow[3] = stateCI[1]
        df.loc[len(df.index)] = dfRow

print (df)

usmap = px.choropleth(df,
                    locations='State', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='Mean Price ($)',
                    color_continuous_scale="burgyl", 
                    )
usmap.update_layout(
      title_text = 'Mean Car Sales Price by State',
      title_font_family="Times New Roman",
      title_font_size = 22,
      title_font_color="black", 
      title_x=0.45, 
         )
usmap.show()

plt.errorbar( df['State'], df['Mean Price ($)'], yerr=df['CIHigh'] - df['CILow'], fmt='o', color='Black', elinewidth=3,capthick=3,errorevery=1, alpha=1, ms=4, capsize = 5)
plt.bar(df['State'], df['Mean Price ($)'],tick_label = df['State'])##Bar plot
plt.xlabel('State') ## Label on X axis
plt.ylabel('Price') ##Label on Y axis
plt.show()