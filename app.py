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


@st.cache_data
def get_projets():
    projects = []
    for project_key in client.list_project_keys():
        if project_key.startswith("SIA") or project_key.startswith("SPIDER") or project_key.startswith("GROUP_DATA_SHARING"):
            projects.append(project_key)
    return projects

            
@st.cache_data
def print_jobs(jobs):
    for job in jobs:
        st.write(f"- {job["def"]["name"]}")


@st.fragment(run_every=2)
def get_jobs(project):
    jobs = [job for job in project.list_jobs() if not job["stableState"]]
    print_jobs(jobs)

client = get_dataiku_client()
projects = get_projets()

for project_key in projects:
    project = client.get_project(project_key)
    st.write(f"#### {project_key}")
    get_jobs(project)
    