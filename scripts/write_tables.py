'''
Read statements.json and create primary tables.
'''
#Import json, pandas, and numpy.
import json
import pandas as pd
import numpy as np

#Open statements.json
with open('../data/statements.json', 'r',   encoding='utf-8') as f:
    data = json.loads(f.read())

#Normalize json and store dataframe in variable
data_df = pd.json_normalize(data, record_path=['statements'])
data_df.to_csv('../data/master.csv')

#COURSE
def write_course_table(df):
    df = df[df['object.id']=='http://id.tincanapi.com/activity/tincan-prototypes/golf-example']
    return (df        
            .drop(columns=['stored',
                        'version',
                        'actor.account.name',
                        'actor.objectType',
                        'authority.objectType',
                        'authority.account.name',
                        'actor.account.homePage',
                        'authority.account.homePage',
                        'context.contextActivities.category',
                        'context.contextActivities.grouping',
                        'context.contextActivities.parent',
                        'result.response',
                        'object.definition.correctResponsesPattern',
                        'object.definition.choices', 
                        'object.definition.interactionType',
                        'verb.display.en']
              )
            .assign(timestamp = pd.to_datetime(df.timestamp),
                verb = df['verb.display.en-US'].fillna('launched'),
                date = pd.to_datetime(df['timestamp']).dt.date,
                year = pd.to_datetime(df['timestamp']).dt.year,
                month = pd.to_datetime(df['timestamp']).dt.month,
                day = pd.to_datetime(df['timestamp']).dt.day,
                dayName = pd.to_datetime(df['timestamp']).dt.day_name(),
                hour = pd.to_datetime(df['timestamp']).dt.hour,            
                duration = pd.to_timedelta(df['result.duration']),
                passed = np.where(df['verb.display.en-US']=='passed',1,0),
                failed = np.where(df['verb.display.en-US']=='failed',1,0),
                initialized = np.where(df['verb.display.en-US']=='initialized',1,0),
                terminated = np.where(df['verb.display.en-US']=='terminated',1,0),
                )
            .drop(columns = ['verb.display.en-US'])
            .reset_index(drop=True) 
            .to_csv('../data/course.csv', encoding='utf-8', index=True)
    )

#QUIZ
def write_quiz_table(df):
    df = df[df['object.id']=='http://id.tincanapi.com/activity/tincan-prototypes/golf-example/GolfAssessment']
    return (df
            .drop(columns=['stored',
                        'version',
                        'actor.objectType',
                        'actor.account.name',
                        'actor.account.homePage',
                        'context.contextActivities.category',
                        'context.contextActivities.grouping',
                        'context.contextActivities.parent',
                        'authority.name',
                        'authority.objectType',
                        'authority.account.name',
                        'authority.account.homePage',
                        'result.response',
                        'verb.display.en',
                        'object.objectType',
                        'object.definition.correctResponsesPattern',
                        'object.definition.choices', 
                        'object.definition.interactionType']
            )
            .assign(timestamp = pd.to_datetime(df.timestamp),
                    date = pd.to_datetime(df['timestamp']).dt.date,
                    year = pd.to_datetime(df['timestamp']).dt.year,
                    month = pd.to_datetime(df['timestamp']).dt.month,
                    day = pd.to_datetime(df['timestamp']).dt.day,
                    dayName = pd.to_datetime(df['timestamp']).dt.day_name(),
                    hour = pd.to_datetime(df['timestamp']).dt.hour, 
                    duration = pd.to_timedelta(df['result.duration']),
                    passed = np.where(df['verb.display.en-US']=='passed',1,0),
                    failed = np.where(df['verb.display.en-US']=='failed',1,0),
                    attempted = np.where(df['verb.display.en-US']=='attempted',1,0),
            )
            .reset_index(drop=True) 
            .to_csv('../data/quiz.csv', encoding='utf-8', index=True)
    )

#QUESTIONS
def write_questions_table(df):
    df = df[df['object.definition.type']=='http://adlnet.gov/expapi/activities/cmi.interaction']
    return (df        
            .drop(columns=['stored',
                        'version',
                        'actor.objectType',
                        'actor.account.name',
                        'actor.account.homePage',
                        'context.contextActivities.category',
                        'context.contextActivities.grouping',
                        'context.contextActivities.parent',
                        'object.definition.name.en-US',
                        'object.objectType',
                        'authority.name',
                        'authority.objectType',
                        'authority.account.name',
                        'authority.account.homePage',
                        'result.duration',
                        'result.score.scaled',
                        'result.score.raw',
                        'result.score.min',
                        'result.score.max',
                        'result.completion',
                        'verb.display.en'
                       ]
            )
            .assign(timestamp = pd.to_datetime(df.timestamp),
                total = np.where(df['verb.display.en-US']=='answered',1,0),
                correct = np.where(df['result.success']==True,1,0),
                incorrect = np.where(df['result.success']==False,1,0)
            )
            .rename(columns = {
                'object.definition.description.en-US':'question',
                'object.definition.correctResponsesPattern':'correct.response',
                'object.definition.choices':'choices',
                'verb.display.en-US': 'answered'
            })
            .reset_index(drop=True) 
            .to_csv('../data/questions.csv', encoding='utf-8', index=True)
    )

#USAGE
def write_usage_table(df):
    launched = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/launched']
    resumed = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/resumed']
    initialized = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/initialized']
    terminated = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/terminated']
    df = pd.concat([launched, resumed, initialized, terminated], axis=0)
    
    return (df
            .drop(columns=['version',
                'stored',
                'actor.objectType',
                'actor.account.name',
                'actor.account.homePage',
                'context.contextActivities.category',
                'context.contextActivities.category',
                'context.contextActivities.grouping', 
                'authority.name',
                'authority.objectType',
                'authority.account.name',
                'authority.account.homePage',
                'object.definition.name.en-US', 
                'object.definition.description.en-US',
                'object.definition.type', 
                'object.objectType', 
                'result.duration',
                'context.contextActivities.parent', 
                'result.score.scaled',
                'result.score.raw', 
                'result.score.min', 
                'result.score.max',
                'result.success', 
                'result.completion', 
                'result.response',
                'object.definition.correctResponsesPattern',
                'object.definition.choices', 
                'object.definition.interactionType'
              ])
            .assign(timestamp = pd.to_datetime(df.timestamp),
                verb = np.where(df['verb.id']=='http://adlnet.gov/expapi/verbs/launched','launched',df['verb.display.en-US']),
                launched = np.where(df['verb.id']=='http://adlnet.gov/expapi/verbs/launched',1,0),
                resumed = np.where(df['verb.id']=='http://adlnet.gov/expapi/verbs/resumed',1,0),
                terminated = np.where(df['verb.id']=='http://adlnet.gov/expapi/verbs/terminated',1,0),
                initialized = np.where(df['verb.id']=='http://adlnet.gov/expapi/verbs/initialized',1,0),
                verbID = df['verb.id'].astype('category'),
                date = pd.to_datetime(df['timestamp']).dt.date,
                year = pd.to_datetime(df['timestamp']).dt.year,
                month = pd.to_datetime(df['timestamp']).dt.month,
                day = pd.to_datetime(df['timestamp']).dt.day,
                dayName = pd.to_datetime(df['timestamp']).dt.day_name(),
                hour = pd.to_datetime(df['timestamp']).dt.hour
                )
            .drop(columns = ['verb.id','verb.display.en-US','verb.display.en'])
            .reset_index(drop=True)
            .to_csv('../data/usage.csv', encoding='utf-8', index=True)
)
#ROUTINE
write_course_table(data_df)
write_quiz_table(data_df)
write_questions_table(data_df)
write_usage_table(data_df)
