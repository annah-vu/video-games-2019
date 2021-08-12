import pandas as pd
import numpy as np

### Acquire ###

def get_video_games():
    '''
    get_video_games will bring in our original .csv into a pandas dataframe
    '''
    df = pd.read_csv('data/vgsales12-4-2019.csv')
    return df

### Prepare ### 


def numerate(df, column, name):
    '''
    takes in the df, the string format of the column name, and a new desired name
    and it will assign each unique value in a column to a number
    '''
    lst = df[column].value_counts().index.to_list()
    for count, value in enumerate(lst):
        df.loc[df[column]==value, name]=count
    df[name] = df[name].astype(int)
    return df

def play_video_games(df):
    '''
    play_video_games will take in our original df, and prepare it for use
    '''
    #clean up column names
    df.columns= df.columns.str.strip().str.lower()
    
    #fill nulls in global_sales with 0
    df['global_sales'] = df['global_sales'].fillna(0)
    
    #fill nulls in total_shipped with 0
    df['total_shipped'] = df['total_shipped'].fillna(0)
    
    #create a total_sales column which is total_shipped plus global_sales
    #I noticed that most columns had either a shipped or a global sales value. 
    #I'm going to just sum them into one column
    df['total_sales'] = df['total_shipped'] + df['global_sales']
    
    #drop the columns we don't need anymore
    df = df.drop(columns=['total_shipped','global_sales','na_sales','pal_sales','jp_sales','other_sales'])
    
    #fill esrb_rating nulls with NR for not rated
    df['esrb_rating'] = df.esrb_rating.fillna('NR')
    
    
    #fill in publishers/developers, yes I looked these up myself
    
    #Gourmet Chef's
    df.loc[10839,'developer'] = 'Ubisoft'
    
    #Wordmaster
    df.loc[12704,'developer'] = 'Destination Software, Inc'

    #SAS: Secure Tomorrow
    df.loc[20694,'developer'] = 'City Interactive'

    #My Baby and Me
    df.loc[21227,'publisher'] = '505 Games'
    df.loc[21227,'developer'] = '505 Games'

    #Abandoner
    df.loc[21724,'developer'] = 'Unknown'

    #Bounty Hunter
    df.loc[25170,'developer'] = 'Unknown'

    #Duludubi Star
    df.loc[29414,'publisher'] = 'Shenzhen Huaqiang'
    df.loc[29414,'developer'] = 'Fantawild'

    #Finkles Adventure
    df.loc[30941,'publisher'] = 'Lexicon'
    df.loc[30941,'developer'] = 'Lexicon'

    #Hidden Mysteries: Buckingham Palace
    df.loc[33465,'publisher'] = 'GameMill'
    df.loc[33465,'developer'] = 'Big Fish'

    #istanbul Beyleri
    df.loc[34414,'developer'] = 'Unknown'

    #Panzer Elite General
    df.loc[40434,'developer'] = 'Unknown'

    #Purrfect Pet Shop
    df.loc[41879,'developer'] = 'eGames'

    #The Enchanted Unicorn
    df.loc[48148,'developer'] = 'Take-Two Interactive'

    #The Orb and the Oracle
    df.loc[48642,'publisher'] = 'GameMill'
    df.loc[48642,'developer'] = 'Big Fish'

    #VIVA Fighter
    df.loc[50781,'developer'] = 'Unknown'

    #My Friend Pedro
    df.loc[54314,'publisher'] = 'Devolver Digital'
    df.loc[54314,'developer'] = 'DeadToast'
    df.loc[54315,'publisher'] = 'Devolver Digital'
    df.loc[54315,'developer'] = 'DeadToast'

    #create a no_critic_rating column, so if critic_score was null, then 1. Else 0.
    df['no_critic_rating']= (df['critic_score'].isnull()==True).astype(int)
    #fill in the nulls with 0.0 (minimum in original df was 1.0)
    df['critic_score'] = df.critic_score.fillna(0.0)
    
    #create a no_user_rating column, so if user_score was null, then 1. Else 0.
    df['no_user_rating']= (df['user_score'].isnull()==True).astype(int)
    #fill in the nulls with 0.0 (minimum in the original df was 2.0)
    df['user_score'] = df.user_score.fillna(0.0)
    
    #make an unknown_release_date column, so if year was null, then 1. Else 0.
    df['unknown_release_date']= (df['year'].isnull()==True).astype(int)
    
    #fill nulls in year column with 1950 (so its out of range), the oldest year in the original df was 1970.
    df['year'] = df.year.fillna(1950)
    
    #turn object columns into machine-learning-friendly columns
    numerate(df, 'esrb_rating', 'esrb_num')
    numerate(df, 'genre', 'genre_num')
    numerate(df, 'platform', 'platform_num')
    numerate(df, 'publisher', 'publisher_num')
    numerate(df, 'developer', 'dev_num')
    
    return df