import pandas as pd
import numpy as np

def compare_df(df1: pd.DataFrame, df2: pd.DataFrame, primary_key:list, sample_size:int=50, decimal_precision:int=20):
    """This function gives 50 or more primary keys from the varibles where there is mis-match while doing the comparision of two dataFrames"""
    primary_key = primary_key
    decimal_precision = 10**(-decimal_precision)

    cols = list(set(df1.columns)-set(primary_key))
    df2_matched_cols = df2[df1.columns]

    # Left join on primary key
    df = df1.merge(df2_matched_cols, on= primary_key, how='left')

    empty_df = pd.DataFrame()

    for i in range(len(cols)):
        size = sample_size
        df3 = df[primary_key + [cols[i]+'_x', cols[i]+'_y']] # selecting a pair of column one by one 
        df3.columns = primary_key + ['Base', 'Sample'] # renaming it to Base and Sample
        df3 = df3[df3.Base!=df3.Sample] # filtering if sample not equal to base
        df3['Var_Name'] = cols[i]  # assigning the name of variable which is being compared, in column Var_Name
        
        # if the Base variable is numerical then calculate the difference, 
            # filter the precision and sort by Absolute differenc in desc order, 
        # if the column is not numerical then create Diff and Diff_Abs variable with None
        if pd.api.types.is_any_real_numeric_dtype(df3['Base']):
            df3['Diff'] = df3.Base - df3.Sample
            df3 = df3[(df3['Diff']>decimal_precision) | (df3['Diff']<=-decimal_precision)]
            df3['Diff_Abs'] = np.abs(df3['Diff'])
            df3 = df3.sort_values(by=['Diff_Abs'], ascending=[False])
        else:
            df3['Diff'] = np.nan
            df3['Diff_Abs'] = np.abs(df3['Diff'])

        # limit the number of records 
        if df3.shape[0]<sample_size:
            size = df3.shape[0]
        df3 = df3.head(size)

        # append to the empty dataframe
        empty_df = pd.concat([empty_df,df3], axis=0)
        empty_df = empty_df[['Var_Name']+ primary_key + ['Base', 'Sample', 'Diff', 'Diff_Abs']]
    return empty_df.reset_index(drop=True)


if __name__=="__main__":
    
    # Example DataFrames
    data1 = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Ind', 'Naman'],
    'Age': [25.0, 30.0, 35.0, 40.0, 28.0, 20.0],  # Floats
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Sydney'],
    'Date': ['2023-01-01', '2023-02-15', '2023-03-10', '2023-04-22', '2023-05-05', '2023-06-29']  # Sample dates
}

    data2 = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Naman'],
    'Age': [26.0, 30.0, 35.0, 44.0, 28.0, 20.0001],  # Floats
    'City': ['New York', 'San Francisco', 'Chicago', 'Dallas', 'Phoenix', 'Tokyo'],
    'Date': ['2023-01-02', '2023-02-16', '2023-03-11', '2023-04-23', '2023-05-06', '2023-06-29']  # Sample dates
}

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    import datetime as dt

    # df1['Date'] = df1.apply(lambda x: dt.datetime.strptime(x.Date, "%Y-%m-%d").date(), axis=1)
    # df2['Date'] = df2.apply(lambda x: dt.datetime.strptime(x.Date, "%Y-%m-%d").date(), axis=1)
    

    # sample size is default set to 50 whereas decimal_precision is 20 by default 
    empty_df = compare_df(df1, df2, ['Name'], sample_size=20, decimal_precision=6)
    empty_df2 = compare_df(df1, df2, ['Name'])

    print(empty_df)
    # print(df)