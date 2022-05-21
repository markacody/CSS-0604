'''
Read csv files(s) and create tables for display on the UI.
'''
#Import pandas, numpy, and humanize.
import pandas as pd
import numpy as np
import humanize

#Open course.csv
course_data = pd.read_csv('../data/course.csv')

#COURSE UI TABLE
def write_course_ui_table(df):
    df['duration'] = pd.to_timedelta(df['duration'])
    df['date'] = pd.to_datetime(df['date'])
    return (df
            .pivot_table(values=['passed', 'failed', 'initialized', 'terminated','duration','date','dayName'], 
                       index=['actor.name'],
                       aggfunc={'passed': np.sum,
                             'failed': np.sum,
                             'initialized': np.sum,
                             'terminated': np.sum,
                             'duration': np.max,
                             'date': np.max,
                             'dayName': np.max})
            .reset_index()
            .rename(columns = {
              'actor.name':'learner',
              'dayName': 'day',
          })
  )

#ROUTINE
# Step 1. Create the pivot table
result = write_course_ui_table(course_data)
# Step 2. Humanize the time delta
result['duration'] = result['duration'].apply(humanize.naturaldelta)
# Step 3. Separate first and last name
result[['given_name','family_name']] = result['learner'].str.split(pat = ' ', n = 2, expand = True)
# Step 4 . Resequence the columns
result = result[['learner', 'given_name', 'family_name', 'day','date', 'duration', 'passed', 'failed', 'initialized','terminated']]
# Step 5. Write the dataframe to csv
result.to_csv('../data/course_ui_table.csv',encoding='utf-8', index=True)