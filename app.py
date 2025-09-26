import streamlit as st
import dataikuapi
import urllib3
import time
from dotenv import dotenv_values


config = dotenv_values(".env")


@st.cache_resource
def get_dataiku_client():
    HOST = config["HOST"]
    API_KEY = config["API_KEY"]
    urllib3.disable_warnings()
    client = dataikuapi.DSSClient(HOST, API_KEY, insecure_tls=True)
    return client

