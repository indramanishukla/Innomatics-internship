# from sqlalchemy import literal
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import expr, lit, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType


def compare_df(df1, df2, primary_key:list, sample_size:int=50, decimal_precision:int=20):
    """This function gives 50 or more primary keys from the varibles where there is mis-match while doing the comparision of two dataFrames"""

    primary_key = primary_key
    decimal_precision = 10**(-decimal_precision)

    cols = list(set(df1.columns)-set(primary_key))
    df2_matched_cols = df2[df1.columns]

    # Join Indicators adding suffix _x to the columns in left datafram and _y in right dataframe
    df1 = df1.toDF(*primary_key+[i+'_x' for i in df1.columns if i not in primary_key])
    df2_matched_cols = df2_matched_cols.toDF(*primary_key+[i+'_y' for i in df2_matched_cols.columns if i not in primary_key])

    # Left join on primary key
    df = df1.join(df2_matched_cols, on= primary_key, how='left')

    # Create empty dataframe
    primary_key_info = [(i, StringType()) for i in primary_key] # Primary_Key schema info for empty dataframe
    column_info = [("Var_Name", StringType())]+primary_key_info+[("Base", StringType()), 
                                                            ("Sample", StringType()), 
                                                            ("Diff", FloatType()),
                                                            ("Diff_Abs", FloatType())] # all columns schema info
    schema = StructType([StructField(name, dtype, True) for name, dtype in column_info]) # schema for empty dataframe
    empty_df = spark.createDataFrame([], schema=schema)

    for i in range(len(cols)):
        size = sample_size
        df3 = df[primary_key + [cols[i]+'_x', cols[i]+'_y']] # selecting a pair of column one by one 
        df3 = df3.toDF(*primary_key + ['Base', 'Sample']) # renaming it to Base and Sample
        df3 = df3[df3.Base!=df3.Sample] # filtering if sample not equal to base 
        df3 = df3.withColumn("Var_Name", lit(cols[i])) # assigning the name of variable which is being compared, in column Var_Name
        
        # if the Base variable is numerical then calculate the difference, 
            # filter the precision and sort by Absolute differenc in desc order, 
        # if the column is not numerical then create Diff and Diff_Abs variable with None
        if df3[['Base']].dtypes[0][1] in ['int','double']:
            df3 = df3.withColumn("Diff", df3.Base - df3.Sample)
            df3 = df3[(df3['Diff']>decimal_precision) | (df3['Diff']<=-decimal_precision)]
            df3 = df3.withColumn("Diff_Abs", expr("abs(Diff)"))
            df3 = df3.orderBy(col("Diff_Abs").desc())
        else:
            df3 = df3.withColumn("Diff", lit(None).cast(FloatType()))
            df3 = df3.withColumn("Diff_Abs", expr("abs(Diff)"))

        # limit the number of records 
        if df3.count()<sample_size:
            size = df3.count()
        df3 = df3.limit(size)

        # append to the empty dataframe
        empty_df = empty_df.union(df3.select(['Var_Name']+ primary_key + ['Base', 'Sample', 'Diff', 'Diff_Abs']))
    return empty_df


if __name__=="__main__":
# Initialize Spark session
    spark = SparkSession.builder \
        .appName("Create DataFrames") \
        .getOrCreate()

    # Your dictionaries
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Ind', 'Naman'],
        'Age': [25.0, 36.0, 35.0, 40.0, 24.0, 20.0],  # Floats
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Sydney'],
        'Date': ['2023-01-01', '2023-02-15', '2023-03-10', '2023-04-22', '2023-05-05', '2023-06-30']  # Sample dates
    }

    data2 = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Naman'],
        'Age': [26.0, 30.0, 35.0, 41.0, 28.0, 20.0001],  # Floats
        'City': ['New York', 'San Francisco', 'Chicago', 'Dallas', 'Phoenix', 'Tokyo'],
        'Date': ['2023-01-02', '2023-02-16', '2023-03-11', '2023-04-23', '2023-05-06', '2023-06-29']  # Sample dates
    }

    # Create DataFrames from dictionaries
    df1 = spark.createDataFrame(list(zip(*data1.values())), schema=list(data1.keys()))
    df2 = spark.createDataFrame(list(zip(*data2.values())), schema=list(data2.keys()))

    df1 = df1.withColumn("Age", expr("cast(age as int)"))
    df1 = df1.withColumn("Date", expr("to_date(Date) as Date"))
    df2 = df2.withColumn("Date", expr("to_date(Date) as Date"))

    # # Show DataFrames
    print(df1.show())
    print(df2.show())

    empty_df = compare_df(df1, df2, ['Name'])
    print(empty_df.show())



