def concatenate_dataframes(dataframes):
    """
    Concatenate a list of DataFrames horizontally based on the 'date' column.
    """
    if not dataframes:
        return None

    # Start with the first DataFrame
    merged_df = dataframes[0]

    # Iterate over the remaining DataFrames and perform left joins on the 'date' column
    for df in dataframes[1:]:
        merged_df = merged_df.join(df, on="date", how="left")

    return merged_df
