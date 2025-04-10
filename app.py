
import streamlit as st
import numpy as np
import cvxpy as cp
import plotly.express as px

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

page=st.sidebar.selectbox(label="Navigation", options=["Overview", "Optimization", "Risk Analysis"])
if page=="Overview":
    from application_pages.Overview import main
    main() 
elif page=="Optimization":
    from application_pages.Optimization import main
    main()
elif page=="Risk Analysis":
    from application_pages.Risk_Analysis import main
    main()
    


st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity.")