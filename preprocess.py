import re
import pandas as pd

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}(?:\s(?:AM|PM))?\s[-–]\s'
    messages=re.split(pattern,data)[1:]
    
    dates=re.findall(pattern,data)
    df = pd.DataFrame({
        'user_messages': messages,
        'message_dates': dates
    })


    # df['message_dates'] = df['message_dates'].str.replace(' -', '', regex=False)

    # df['message_dates'] = (
    # df['message_dates']
    # .astype(str)
    # .str.replace('\ufeff', '', regex=False)   # remove BOM
    # .str.replace('\xa0', ' ', regex=False)    # non-breaking space
    # .str.replace('–', '-', regex=False)       # en-dash
    # .str.replace(' -', '', regex=False)       # trailing dash
    # .str.strip()
    # )

    print(df['message_dates'])
    
    df['dates'] = pd.to_datetime(
        df['message_dates'],
        format='%d/%m/%Y, %H:%M - ',
        dayfirst=True,
        errors='coerce'
    )
    print(df['dates'])

    df.drop(columns='message_dates', inplace=True)
    users = []
    messages = []

    for i in df['user_messages']:
        entry = re.split(r'^([^:]+):\s', i, maxsplit=1)
        
        if len(entry) == 3:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['messages'] = messages


    df.drop(columns='user_messages',inplace=True)
    df['year']=df['dates'].dt.year
    df['month']=df['dates'].dt.month_name()
    df['day']=df['dates'].dt.day
    df['hour']=df['dates'].dt.hour
    df['minute']=df['dates'].dt.minute
    df['month_num']=df['dates'].dt.month
    return df

# f=open('WhatsApp Chat with Aiml_unofficial.txt','r',encoding='utf-8')
# data=f.read()
# df=preprocess(data)
# print(df)