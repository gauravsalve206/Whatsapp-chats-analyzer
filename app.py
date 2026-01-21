import streamlit as st 
import preprocess,helper
import matplotlib.pyplot as plt




st.set_page_config(
page_title="Whatsapp Chats Visualizer",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
"Get Help": "https://myapp.com/help",
"Report a bug": "mailto:support@myapp.com",
"About": "# My Dashboard\nAn awesome analytics tool."
}
)









uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess.preprocess(data)
    
    st.write(df)
    
    user=df['user'].unique().tolist()
    user.sort()
    user.remove('group_notification')
    user.insert(0,"overall")
        
    selected_user=st.sidebar.selectbox("select user for chat analysis",user)
    if st.sidebar.button("show Analysis"):
        st.title("Top Stats")
        col1,col2,col3,col4=st.columns(4)
        num_messages,num_words,num_media,num_url=helper.fetch_stats(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_url)
        
        st.title("Monthly Timeline")
        
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        if selected_user=="overall":
            st.title("Most busy users:")
            col1,col2=st.columns(2)
            x,busy_user=helper.fetch_busy_user(df)
            fig,ax=plt.subplots()

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(busy_user)
        
        st.title("Most Frequently Used Words")
        df_wc=helper.fetch_wordcloud(selected_user,df)
        
        if df_wc!="null":
            fig,ax=plt.subplots()
            ax=plt.imshow(df_wc)
            st.pyplot(fig)
        else:
            st.write("user sent no messages")
            
        
        #most common words
        st.title("Most Common Words Bar Graph")
        most_common=helper.most_common_words(selected_user,df)
        if most_common.empty!=True:
            fig,ax=plt.subplots()
            ax.barh(most_common[0],most_common[1])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.write("User sent no messages")
        
        #emoji analysis
        col1,col2=st.columns(2)
        
        with col1:
            st.title("Emoji Anylisis")
            emoji_df=helper.emoji_analyzer(selected_user,df)
            st.dataframe(emoji_df)
            
        with col2:
            st.title("Emoji Pie Chart")
            emoji_df=helper.emoji_analyzer(selected_user,df)
            if emoji_df.empty!=True:
                
                fig,ax=plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            else:
                st.write("NO emoji used")
    