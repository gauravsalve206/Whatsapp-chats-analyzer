from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


f=open('stop_hinglish.txt','r')
stop_words=f.read()

def remove_stop(msg):
    y=[]
    for i in msg.lower().split():
        if i not in stop_words:
            y.append(i)
    return " ".join(y)


def fetch_stats(user,df):
    
    if user != "overall":
        df=df[df['user']==user]
    
    num_messages=df.shape[0]   
    #extracting urls
    extractor=URLExtract()
    links=[]

    for i in df['messages']:
        links.extend(extractor.find_urls(i))

    words=[]
    num_media=df[df['messages']=="<Media omitted>\n"].shape[0]
    for i in df['messages']:
        words.extend(i)
    return num_messages,len(words),num_media,len(links)

def fetch_busy_user(df):
    x=df['user'].value_counts().head()
    busy_user=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"Name","user":"Percentage"}).head(10)
    return x,busy_user

def fetch_wordcloud(user,df):
    if user!="overall":
        df=df[df['user']==user]
    new_df=df[df['messages']!="<Media omitted>\n"]
    new_df=new_df[new_df['messages']!="group_notification"]
    
    new_df['messages']=new_df['messages'].apply(remove_stop)
    if new_df.empty != True:
        wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
        df_wc=wc.generate(new_df['messages'].str.cat(sep=" "))
        return df_wc
    else:
        return "null"
    
def most_common_words(user,df):
    
    if user!="overall":
        df=df[df['user']==user]
        
    new_df=df[df['messages']!="<Media omitted>\n"]
    new_df=new_df[new_df['messages']!="group_notification"]


    words=[]
    for i in new_df['messages']:
        for w in i.lower().split():
            if w not in stop_words:
                words.append(w)
    
    
    most_common=pd.DataFrame(Counter(words).most_common(20))
    print(words)
    return most_common

    
def emoji_analyzer(user,df):
    if user!="overall":
        df=df[df['user']==user]
        
    emojis=[]

    for i in df['messages']:
        for c in i:
            if emoji.is_emoji(c):
                emojis.extend(c)
                
    emoji_df=pd.DataFrame(Counter(emojis).most_common(20))
    
    return emoji_df

def monthly_timeline(user,df):
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline