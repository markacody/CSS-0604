'''
Read csv files(s) and create tables for display on the UI.
'''
#Import pandas, numpy, and humanize.
import pandas as pd
import numpy as np
import humanize

#Open course.csv and questions.csv
course_data = pd.read_csv('../data/course.csv')
questions_data = pd.read_csv('../data/questions.csv')

#COURSE UI TABLE
def write_course_ui_table(df):
    df['duration'] = pd.to_timedelta(df['duration'])
    df['date'] = pd.to_datetime(df['date'])
    return (df
            .pivot_table(values=['passed', 'failed', 'terminated','duration','date','dayName'], 
                       index=['actor.name'],
                       aggfunc={'passed': np.sum,
                             'failed': np.sum,
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

#COURSE UI TABLE ROUTINE
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

#QUESTIONS UI TABLE
def write_questions_ui_table(df):
    return (df.pivot_table(values=['correct.response',
                              'total',
                              'correct',
                              'incorrect'],
                      index=['question'],
                      aggfunc={
                          'correct.response': np.unique,
                          'total': np.sum,
                          'correct': np.sum,
                          'incorrect': np.sum
                        }
                      )
                .reset_index()
            )

#QUESTIONS UI TABLE ROUTINE
#Step 1. Get the pivot table
questions = write_questions_ui_table(questions_data)
#Step 2. Make the correct response values human-readable.
questions['correct.response'] = questions['correct.response'].replace({
                                "['First']":"First",
                                "['true']": 'true',
                                "['false']":'false',
                                "['0[:]0']":'0',
                                "['1[:]1']":'1',
                                "['2[:]2']":'2',
                                "['3[:]3']":'3',
                                "['18[:]18']":'18',
                                "['eagle']":'eagle',
                                "['USGA-and-Royal-and-Ancient']":'USGA-and-Royal-and-Ancient',
                                '["Out-of-the-player\'s-line-of-sight"]':'Out-of-the-line-of-sight',
                                "['Course-Handicap-=-Handicap-index-*-Slope-Rating-/-113']":'Handicap = Index * Slope Rating / 113',
                              }                                
                            )
#Step 3. Resequence and rename columns
questions = questions[['question','correct.response','total','correct','incorrect']]
questions.rename(columns={'total':'total.responses'}, inplace=True)
#Step 4. Write the questions to csv
questions.to_csv('../data/questions_ui_table.csv',encoding='utf-8', index=True)