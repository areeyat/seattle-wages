import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.title("City of Seattle Wage Data")
st.caption("Data last updated 4/2/2026")
#st.set_page_config(layout='wide')
wages = pd.read_csv("City_of_Seattle_Wage_Data_20260402.csv")
num_depts = len(wages['Department'].unique())


# cache? 
wages = wages.rename(columns={"Hourly Rate ": "Hourly Rate"})
#wages = wages.rename(str.lower, axis=1)
wages['Hourly Rate'] = wages['Hourly Rate'].str.strip("$")
wages['Hourly Rate'] = wages['Hourly Rate'].astype("float64")
median_wage = wages['Hourly Rate'].median()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Departments", num_depts, border=True)
col2.metric("Employee Wages", len(wages), help="Number of employee wages recorded. Employees may be repeated across rows if their wages, role, or department changed.",border=True)
col3.metric("Unique Jobs", len(wages['Job Title'].unique()), border=True)
col4.metric("Median Hourly Wage",median_wage, border=True, format="dollar")

emp_counts = """<iframe src='https://flo.uri.sh/visualisation/28839282/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe>"""
wage_scatter = """<iframe src='https://flo.uri.sh/visualisation/28840029/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe>"""

tab1, tab2 = st.tabs(["Departments by size", "Individual wages"])

with tab1:
    """Hover over bubbles to get employee counts for each department."""
    st.iframe(emp_counts, height=620)

with tab2:
    """Hover over points for more details on individual employees."""
    st.iframe(wage_scatter,height=600)



dept_median = wages[['Department','Hourly Rate']].groupby('Department').median().rename(columns={'Hourly Rate':'Median Hourly Rate'})


dept_mean = wages[['Department','Hourly Rate']].groupby('Department').mean().rename(columns={"Hourly Rate":"Avg Hourly Rate"})

dept_count = wages[['Department',"Hourly Rate"]].groupby('Department').count().rename(columns={'Hourly Rate':"Number of Employees"})

dept_stats = dept_mean.join([dept_median,dept_count])

top_10_count = dept_stats.sort_values('Number of Employees', ascending=False).head(10)
num_employees = px.bar(top_10_count,x='Number of Employees',y=top_10_count.index)#,color=top_10_count.index)
num_employees.update_layout(showlegend=False)

top_wage_mean = dept_stats.sort_values('Avg Hourly Rate', ascending=False).head(6)
wage_mean = px.bar(top_wage_mean,x=top_wage_mean.index,y="Avg Hourly Rate")#,color=top_wage_mean.index)

top_wage_med = dept_stats.sort_values('Median Hourly Rate', ascending=False).head(6)
wage_med = px.bar(top_wage_mean,x=top_wage_med.index,y="Median Hourly Rate")#,color=top_wage_mean.index)


#st.html('<div class="flourish-embed flourish-hierarchy" data-src="visualisation/28839282"><script src="https://public.flourish.studio/resources/embed.js"></script><noscript><img src="https://public.flourish.studio/visualisation/28839282/thumbnail" width="100%" alt="hierarchy visualization" /></noscript></div>')





# which department has the most work training? 
# which department has the most interns? 
# wages vs median income in seattle
# number of unique job titles
