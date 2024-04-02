import pandas as pd

mock_df1 = pd.DataFrame(
    [
        ["State1", "Question1", 10],
        ["State1", "Question1", 245],
        ["State1", "Question2", 12],
        ["State2", "Question1", 15],
        ["State2", "Question1", 22],
        ["State2", "Question2", 8],
    ],
    columns=["LocationDesc", "Question", "Data_Value"],
)

mock_df2 = pd.DataFrame(
    [
        ["State1", "Question1", 10],
        ["State1", "Question1", 245],
        ["State1", "Question2", 12],
        ["State2", "Question1", 15],
        ["State2", "Question1", 22],
        ["State2", "Question2", 8],
        ["State3", "Question1", 43],
        ["State3", "Question1", 542],
        ["State3", "Question2", 532],
        ["State4", "Question1", 643],
        ["State4", "Question1", 22],
        ["State4", "Question2", 543],
        ["State5", "Question1", 43],
        ["State5", "Question1", 332],
        ["State5", "Question2", 23],
        ["State6", "Question1", 21],
        ["State6", "Question1", 277],
        ["State6", "Question2", 1],
    ],
    columns=["LocationDesc", "Question", "Data_Value"],
)

mock_df3 = pd.DataFrame(
    [
        ["State1", "Question1", "Category1", "SubCategory1", 10],
        ["State1", "Question1", "Category1", "SubCategory1", 245],
        ["State1", "Question1", "Category1", "SubCategory2", 10],
        ["State1", "Question1", "Category2", "SubCategory3", 12],
        ["State1", "Question2", "Category1", "SubCategory1", 103],
        ["State2", "Question1", "Category1", "SubCategory1", 43],
        ["State2", "Question1", "Category1", "SubCategory1", 455],
        ["State2", "Question1", "Category1", "SubCategory2", 3],
    ],
    columns=["LocationDesc", "Question", "StratificationCategory1", "Stratification1", "Data_Value"],
)

mock_question = "Percent of adults aged 18 years and older who have an overweight classification"