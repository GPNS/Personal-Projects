"""
Code used to solve Demographic Data Analyser in FreeCodeCamp Data Analysis Course. Completed 08/06/2022
"""

import pandas as pd
def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    print(df.columns)
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    average_age_men = df[(df["sex"] == 'Male')]["age"].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df["education"].value_counts()["Bachelors"] / df["education"].size * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`

    higher_education = ("Bachelors" , "Masters" , "Doctorate")
    salary_split = (">50K" , "<=50K")
    education_rich = 0
    education_poor = 0
    number_high_edu = 0

    for edu in higher_education:
        number_high_edu = number_high_edu + df[(df["education"] == edu)]["education"].size
        education_rich = education_rich + df[(df["education"] == edu) & (df["salary"] == ">50K")]["education"].size

        education_poor = education_poor + df[(df["education"] == edu) & (df["salary"] == "<=50K")]["education"].size

    number_rich = df[(df["salary"] == ">50K")]["education"].size
    no_education_rich = number_rich - education_rich

    length_df = df["education"].size
    number_low_edu = length_df - number_high_edu
    higher_education = number_high_edu
    lower_education = number_low_edu

    # percentage with salary >50K
    higher_education_rich = round(education_rich / number_high_edu * 100,1)
    lower_education_rich = round(no_education_rich / number_low_edu * 100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?

    num_min_workers = len(df[df["hours-per-week"] == min_work_hours])

    rich_percentage = round(len(df[(df["hours-per-week"] == min_work_hours) & (df["salary"] == ">50K")].index)/num_min_workers * 100,1)

    # What country has the highest percentage of people that earn >50K?
    tmp = df["native-country"].value_counts()
    tmp = df[['native-country', 'salary']].value_counts()
    print(tmp.to_frame()[0])
    df_tmp = tmp.to_frame()[0]
    print(df_tmp['Mexico'][0])
    highest_earning_country_percentage = 0
    highest_earning_country = None
    for unique in df['native-country'].unique():
        try:
            rich_number = df_tmp[unique]['>50K']
            poor_number = df_tmp[unique]['<=50K']
        except:
            continue
        total = poor_number+rich_number

        temporary = round(rich_number/total*100,1)
        if temporary > highest_earning_country_percentage:
            highest_earning_country_percentage = temporary
            highest_earning_country = unique

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df["native-country"] == 'India') & (df["salary"] == ">50K")]["occupation"].value_counts().to_frame().idxmax()[0]

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)
    return 0
A = calculate_demographic_data()