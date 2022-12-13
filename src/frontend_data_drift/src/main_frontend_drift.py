import streamlit as st

import sender
import pandas as pd
import json

import time
import datetime

st.set_page_config(
    page_title="Red Wine Data Drift",
    page_icon="🍸",
    layout="wide"
)

path_image = "wallpaper.jpg"

st.image(path_image, use_column_width=True, caption="Alcohol abuse is dangerous for health")

st.title("Red Wine Data Drift")

last_AUC = None
date = None
chart_data = None

def get_drift(new=False):
    if new:
        y = sender.new_drift()
    else:
        y = sender.refresh_drift()
        
    if not y["status"]:
        st.error(f"Error during checking data drift: {y['message']}")
        return None
    else:
        d = json.loads(y["data"])
        return pd.DataFrame(d).drop(columns=["Unnamed: 0"])
    
def get_data_drift(from_date, to_date):
    y = sender.downloader(int(from_date), int(to_date))
    
    if not y["status"]:
        st.error(f"Error during checking data drift: {y['message']}")
        return None
    else:
        d = json.loads(y["data"])
        return pd.DataFrame(d)
    
def update_auc(data):
    if data is not None and len(data) != 0:
        last = data.iloc[-1]
        return last[0], last[1]
    
    return None, None

data = get_drift()
date, last_AUC = update_auc(data)
chart_data = data

st.write(f"""
         ###
         ## Last AUC ({date}): {last_AUC}
         ###
         """)

if st.button("Refresh"):
    data = get_drift()
    date, last_AUC = update_auc(data)
    chart_data = data
    
period = st.number_input("Number of periods", min_value=-1, value=20)

st.write("###")

if chart_data is not None:
    if period != -1:
        chart_data = chart_data.iloc[-period:]
    
    st.line_chart(chart_data, x="Date", y="AUC")

st.write("##")

if st.button("Test New Entries"):
    data = get_drift(True)
    date, last_AUC = update_auc(data)
    chart_data = data

st.write("## Select a period to download the data")

st1, st2 = st.columns(2)

if chart_data is not None and len(chart_data) != 0:
    start_date = chart_data.iloc[0][0]
    end_date = chart_data.iloc[-1][0]
   
    from_date, to_date = st.select_slider("Select a range of dates",
                                          options=chart_data["Date"].tolist(),
                                          value=(start_date, end_date))

    if st.button("Overview"):
        # ISO format
        iso_format = "%Y-%m-%d %H:%M:%S"
        from_date = int(time.mktime(datetime.datetime.strptime(from_date, iso_format).timetuple()))
        to_date = int(time.mktime(datetime.datetime.strptime(to_date, iso_format).timetuple()))
       
        data = get_data_drift(from_date, to_date)
        if data is not None:
            st.dataframe(data.head(50))
            
            
        st.download_button(label="Download data to csv",
                           data=data.to_csv().encode('utf-8'),
                           file_name=f"data_drift_{from_date}_{to_date}.csv",
                           mime="text/csv")
            
        
        