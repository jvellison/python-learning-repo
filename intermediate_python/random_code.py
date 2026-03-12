# #grouped = dfs['header'].groupby('ETHNICITY').count() # not that useful
# grouped = dfs['header'].groupby('ETHNICITY').size() # easier to use
# #grouped = grouped.to_frame('Count').reset_index()
# grouped = grouped.to_frame('Header - Ethnicities - Count').reset_index()
# grouped = grouped.rename(columns={'ETHNICITY':'Ethnicity'})

# grouped['Header - Ethnicities - Percentage'] = (grouped['Header - Ethnicities - Count'] / 
#                                                 grouped['Header - Ethnicities - Count'].sum()) * 100

# # can also use .upper(), .lower(), .capitalise()
# # df.columns = df.capitalise()

# print(grouped)
# print(grouped['Header - Ethnicities - Percentage'].sum())