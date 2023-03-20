import streamlit as st
import pandas as pd
from io import StringIO
from xml.etree import ElementTree
import csv
import os

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
with st.container():
   st.write("Bitte Meldungsdatei einfügen")
   xml_file = st.file_uploader("Insert XML")


if xml_file is not None:
    new_file_name = xml_file.name

    # PARSE XML
    xml = ElementTree.parse(xml_file)

    # CREATE CSV FILE
    csvfile = open("data.csv",'w',encoding='utf-8')
    csvfile_writer = csv.writer(csvfile)

    # ADD THE HEADER TO CSV FILE
    csvfile_writer.writerow(["nummer","text"])

    # FOR EACH EMPLOYEE
    for message in xml.findall("context/message"):
    
        if(message):
            # EXTRACT EMPLOYEE DETAILS  
            nummer = message.find("source")
            text = message.find("translation")
            csv_line = [nummer.text.replace('/PLC/PMC', ''), text.text]
            # ADD A NEW ROW TO CSV FILE
            csvfile_writer.writerow(csv_line)
            
    csvfile.close()  

if xml_file is None:
    file = 'data.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)

if os.path.isfile("data.csv") == True:

    csv1 = pd.read_csv('main.csv')
    csv2 = pd.read_csv('data.csv')
    merged = csv1.merge(csv2, on='nummer')
    merged.to_csv("output.csv", index=False)


    with col1:
        df_csv = pd.read_csv("data.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
        st.title("Rohformat: XML Datei")  # add a title
        st.write(df_csv)

    with col2:   
        df_new = pd.read_csv("output.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
        st.title("Generierte CSV Datei")  # add a title
        st.write(df_new)

    my_large_df = pd.read_csv('output.csv') #This is your 'my_large_df'

    @st.cache_data
    def convert_df_to_csv(df):
     #  IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    st.download_button(
        label="Download generierte CSV", 
        data=convert_df_to_csv(my_large_df), 
        file_name=f'{new_file_name}.csv',
        mime='text/csv',
    )
