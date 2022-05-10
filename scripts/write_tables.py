'''
Read statements.json and create tables.
'''
#Import tincan and json.
import json
import pandas as pd

#Open statements.json
with open('../data/statements.json', 'r',   encoding='utf-8') as f:
    data = json.loads(f.read())

#Normalize json and store dataframe in variable
data_df = pd.json_normalize(data, record_path=['statements'])
data_df.to_csv('../data/master.csv')

def write_course_table(df):
    return (
        df[df['object.id']=='http://id.tincanapi.com/activity/tincan-prototypes/golf-example']
        .drop(columns=['context.contextActivities.category',
                       'context.contextActivities.grouping',
                       'context.contextActivities.parent',
                       'result.response',
                       'object.definition.correctResponsesPattern',
                       'object.definition.choices', 
                       'object.definition.interactionType']
              )
        .assign(timestamp = pd.to_datetime(df.timestamp),
                stored = pd.to_datetime(df.stored),
                duration = pd.to_timedelta(df['result.duration']),
                )
        .reset_index(drop=True) 
        .to_csv('../data/course.csv', encoding='utf-8', index=True)
  )

def write_quiz_table(df):
    return (
        df[df['object.id']=='http://id.tincanapi.com/activity/tincan-prototypes/golf-example/GolfAssessment']
        .drop(columns=['context.contextActivities.category',
                       'context.contextActivities.grouping',
                       'context.contextActivities.parent',
                       'authority.name',
                       'authority.objectType',
                       'authority.account.name',
                       'authority.account.homePage',
                       'result.response',
                       'object.definition.correctResponsesPattern',
                       'object.definition.choices', 
                       'object.definition.interactionType']
              )
        .assign(timestamp = pd.to_datetime(df.timestamp),
                stored = pd.to_datetime(df.stored),
                duration = pd.to_timedelta(df['result.duration']),
                )
        .reset_index(drop=True) 
        .to_csv('../data/quiz.csv', encoding='utf-8', index=True)
    )

def write_questions_table(df):
    return (
        df[df['object.definition.type']=='http://adlnet.gov/expapi/activities/cmi.interaction']
        .drop(columns=['context.contextActivities.category',
                       'context.contextActivities.grouping',
                       'context.contextActivities.parent',
                       'object.definition.name.en-US',
                       'authority.name',
                       'authority.objectType',
                       'authority.account.name',
                       'authority.account.homePage',
                       'result.duration',
                       'result.score.scaled',
                       'result.score.raw',
                       'result.score.min',
                       'result.score.max',
                       'result.completion'
                       ]
              )
        .assign(timestamp = pd.to_datetime(df.timestamp),
                stored = pd.to_datetime(df.stored),
                )
        .reset_index(drop=True) 
        .to_csv('../data/questions.csv', encoding='utf-8', index=True)
    )
def write_usage_table(df):
    launched = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/launched']
    resumed = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/resumed']
    initialized = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/initialized']
    terminated = df[df['verb.id'] == 'http://adlnet.gov/expapi/verbs/terminated']
    
    return (pd.concat([launched, resumed, initialized, terminated], axis=0)
    .drop(columns=['version',
                'actor.objectType',
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
                stored = pd.to_datetime(df.stored),
                )
        .reset_index(drop=True) 
        .to_csv('../data/usage.csv', encoding='utf-8', index=True)
)
#ROUTINE
write_course_table(data_df)
write_quiz_table(data_df)
write_questions_table(data_df)
write_usage_table(data_df)
