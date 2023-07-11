import base64
import streamlit as st
from streamlit import components
st.set_page_config(layout="wide") 
                #    initial_sidebar_state="collapsed")
import os
import plotly.express as px
import pandas as pd

@st.cache_data  
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img1 = get_img_as_base64(os.path.join('images', "intro.jpg"))
img2 = get_img_as_base64(os.path.join('images', "sidebar.jpg"))
img3 = get_img_as_base64(os.path.join('images', "sidebar1.jpg"))
# #deploy

# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("data:image/png;base64,{img1}");
# background-size: 110%;
# background-position: center;
# background-repeat: no-repeat;
# background-attachment: local;
# }}

# [data-testid="stSidebar"] > div:first-child {{
# background-image: url("data:image/png;base64,{img3}");
# background-size: 500%;
# background-position: middle;
# background-repeat: no-repeat;
# background-attachment: local;
# }}

page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img1}");
background-size: 120%;
background-position: top-right;
background-repeat: no-repeat;
background-attachment: local;
}}

[id="tabs-bui3-tab-0"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-1"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-2"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-3"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-4"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-5"]{{
background-color: rgba(0, 0, 0, 0);
}}

[id="tabs-bui3-tab-6"]{{
background-color: rgba(0, 0, 0, 0);
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img3}");
background-size: 300%;
background-position: middle;
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# from streamlit import config
# config.set_option('theme', 'blue')

import pandas as pd
import plotly.express as px
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

# import seaborn as sns

# Reading yaml
import yaml
with open(os.path.join('data', 'nations.yaml'), 'r') as file:
    origin_mapping = yaml.safe_load(file)

# Load the countries.json file
import json
with open(os.path.join('data', 'countries.json')) as f:
    countries_data = json.load(f)

# """ Reading Dataframe """
df = pd.read_csv(os.path.join('data', 'TravelerData.csv'))
df.rename(columns={"id": "ID",
                   'Country' : 'DestinationCountry',
                   "destination": "DestinationCity",
                   "sday": "DepartureDay",
                   "SMT": "DepartureMonthString",
                   "syear": "DepartureYear",
                   "duration": "Duration",
                   "name": "CustomerName",
                   "age": "Age",
                   "gender": "Gender",
                   "nationality": "Nationality",
                   "accomtype": "AccommodationType",
                   "accomcost": "AccommodationCost",
                   "transtype": "TransportationType",
                   "transcost": "TransportationCost",
                   "season": "Season",
                   "totalcost": "Revenue",
                   'smonth' : 'DepartureMonth',
                   'sdate' : 'DepartureDate'},
          inplace=True)

df['DepartureDate'] = pd.to_datetime(df['DepartureDate']).dt.date
df['LeaveDate'] = pd.to_datetime(df['DepartureDate']) + pd.to_timedelta(df['Duration'])

df['Nationality'] = df['Nationality'].replace({'UK' : 'British',
                                               'Greece' : 'Greek',
                                               'United Arab Emirates' : 'Emirati',
                                               'Cambodia' : 'Cambodian'})
df['DestinationCountry'] = df['DestinationCountry'].replace({'UK' : 'United Kingdom',
                                                             'USA' : 'United States',
                                                             'Hawaii' : 'United States'})
df['Nationality'] = df['Nationality'].str.replace(' ', '_')
df['DepartureCountry'] = df['Nationality'].map(origin_mapping)
df['Nationality'] = df['Nationality'].str.replace('_', ' ')
df['DepartureCountry'] = df['DepartureCountry'].str.replace('_', ' ')
# Add country code
def get_origin_code(country_name):
    for country in countries_data:
        if country['name']['common'] == country_name:
            return country['cca2']
    return None
df['DepartureCountryCode'] = df['DepartureCountry'].apply(get_origin_code)
df['DestinationCountryCode'] = df['DestinationCountry'].apply(get_origin_code)
# add holidays
import holidays
def has_holiday(row, col):
    country_code = str(row[col])
    if country_code == 'None': return
    try:
        country_holidays = holidays.CountryHoliday(country_code)
    except:
        return
    holidays_list = [country_holidays.get(date) for date in pd.date_range(row['DepartureDate'], row['LeaveDate'], freq='D')]
    return len(holidays_list) > 0 and holidays_list != [None]
df['DepartureHoliday'] = df.apply(lambda row: has_holiday(row, 'DepartureCountryCode'), axis=1)
df['DestinationHoliday'] = df.apply(lambda row: has_holiday(row, 'DestinationCountryCode'), axis=1)
# print(df)


# """ Introduction """
title = st.markdown("<h1 style='text-align: center;font-size: 100px;'>TRAVELER DATA</h1>", unsafe_allow_html=True)


# create a placeholder for the divider below the header  
divider_placeholder = st.empty()
with divider_placeholder.container():
    st.divider()

subtitle = st.title('Introduction')
col1, col2= st.columns(2)
with col1:
    # basicinformation = st.markdown('**Welcome to the company’s database. Here you will find all the necessary information you will need to study tourists’ behaviors, ranging from expenditure of services to discovering the most popular destinations and exploring spending patterns among many others. Hopefully, our data will help you understand what we are doing here as a travelling/tourism company.**')
    basicinformation = st.markdown('<div style="text-align: justify;">Welcome to the company’s database. Here you will find all the necessary information you will need to study tourists’ behaviors, ranging from expenditure of services to discovering the most popular destinations and exploring spending patterns among many others. Hopefully, our data will help you understand what we are doing here as a travelling/tourism company.</div>', unsafe_allow_html=True)

# """ Add Session State """
if 'clicked' not in st.session_state:
    st.session_state['clicked'] = False

# """ Add Button to Proceed """
placeholder = st.empty()
with placeholder.container():
    button_style = """
<div style="display: flex; justify-content: center;">
    <style>
        .hover-button {
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 10000;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 200;
            color: inherit;
            width: 15000px;
            user-select: none;
            background-color: rgb(19, 23, 32);
            border: 1px solid rgba(250, 250, 250, 0.2);
            font-size: 10000px;
            transition-duration: 0.4s;
        }
        .hover-button:hover {
            border: 1px solid red;
            color: red;
        }
    </style>
    <button class="hover-button">Center Aligned Button</button>
</div>
"""
    thebutton = st.button("Let's get started")
    if thebutton:
            st.session_state.clicked = True



def filtration(df:pd.DataFrame, 
               label:str, 
               options:list, 
               default:str='All', 
               all_in_options:bool=True) -> pd.DataFrame:
    if all_in_options: 
        if 'all' not in options:
            options = [default, *sorted(options)]
    choosen = st.multiselect(label=re.sub(r'(?<=\w)([A-Z])', r' \1', label).strip(),
                             options=options,
                             key=label)  
    if 'all' in choosen or len(choosen) == 0: choosen = df[label].unique()
    return df[df[label].isin(choosen)]

# SIDEBAR
if st.session_state.clicked:
    page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img2}");
background-size: 340%;
background-position: top-right;
background-repeat: no-repeat;
background-attachment: local;
}}
    </style>
"""
                
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.sidebar.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)
    st.sidebar.markdown('<p class="big-font">CATEGORIES</p>', unsafe_allow_html=True)
    #####st.beta_set_page_config(menu=['Home', 'About', 'Settings'])

    # """ Delete Intro, Button and Divider """
    divider_placeholder.empty()
    placeholder.empty()
    title.empty()
    subtitle.empty()
    basicinformation.empty()

    # print(age)
    
    age = st.sidebar.select_slider(label='**AGE RANGE**', 
                                   options=list(range(131)),
                                   value=(20, 40),
                                   key='Age')
    df = df.loc[(df['Age'] >= age[0]) & (df['Age'] <= age[1])]

# """ Add Dropdowns for Columns """
    # Sidebar: personal information
    with st.sidebar.expander("**PERSONAL INFORMATION**"):
       
        # Select Gender """
        selectedGender = st.radio("Gender",('All', *df['Gender'].unique()), key='Gender')
        if 'All' in selectedGender or len(selectedGender) == 0: selectedGender = df['Gender'].unique()
        else: selectedGender = [selectedGender]
        df = df[df['Gender'].isin(selectedGender)]
        # print('dasdasdasdasd')
        # print (gender)
        # if 'Gender' not in st.session_state:
        #     st.session_state.Gender = []
        # selectedGender = st.data_editor(
        #     pd.DataFrame({
        #         "Gender": ["All", "Female", "Male"],
        #         "Click to choose": [False, False, False],
        #         }
        #     ),
        #     column_config={"Click to choose": st.column_config.CheckboxColumn(default=False)},
        #     disabled=["Gender"],
        #     hide_index=True,
        # )
        # selectedGender = [ele[0] for ele in selectedGender.values.tolist() if ele[1]]
        # st.session_state.Gender = selectedGender
        # if 'All' in st.session_state.Gender or len(st.session_state.Gender) == 0: st.session_state.Gender = df['Gender'].unique()
        # df = df[df['Gender'].isin(st.session_state.Gender)]
        df.reset_index(inplace=True, drop=True)

        # Select Nationality """
        for c in ['Nationality']:
            df = filtration(df=df, label=c, options=df[c].unique()) 

        df.reset_index(inplace=True, drop=True)

    # # Sidebar: Departure
    # with st.sidebar.expander("Departure"):
    #     for c in ['DepartureMonth', 'DepartureYear']:
    #         df = filtration(df=df, label=c, options=df[c].unique()) 

    #     df.reset_index(inplace=True, drop=True)

    # Sidebar: Destination
    with st.sidebar.expander("**DESTINATION**"):
        for c in ['Continent', 'DestinationCountry']:
            df = filtration(df=df, label=c, options=df[c].unique()) 

        df.reset_index(inplace=True, drop=True)

    # # Sidebar: Transportation
    # with st.sidebar.expander("Transportation and Accommodation"):
    #     for c in ['TransportationType', 'AccommodationType']:
    #         df = filtration(df=df, label=c, options=df[c].unique()) 
    #     df.reset_index(inplace=True, drop=True)


    # # """ Delete Intro, Button and Divider """
    # divider_placeholder.empty()
    # placeholder.empty()
    # title.empty()
    # subtitle.empty()
    # basicinformation.empty() 

    # """ Add New Tabs """
    tab0, tab2, tab3, tab4 = st.tabs(['**REVENUE**', "**CUSTOMER TREND**", "**TRANSPORTATION - ACCOMMODATION**", "**DATA FRAME**"])
    
    # # # """ Display Dataframe for each Tab """
    # st.title('The Frame')
    # # df.drop(['ID', 'DepartureDay', 'DepartureYear', 'DepartureMonth', 'Season', 'DepartureMonthString', 'Revenue', 'CustomerName'], axis='columns', inplace=True)
    # st.dataframe(data=df[['Age', 'Gender', 'Nationality', 'DepartureDate', 'Duration', 'DestinationCountry', 'TransportationType', 'AccommodationType', 'Revenue']], width=1500, use_container_width=True)
    # # st.dataframe(data=df.style.format({'DepartureYear': lambda x : f'{x}'}))
    
    # Data to display
    sales = df.groupby(pd.Grouper(key='LeaveDate', freq='M')).sum()['Revenue'].to_frame().reset_index()
    sales['RevenueLM'] = sales['Revenue'].shift(1)
    sales['RevenueGrowthMonth'] = (sales['Revenue'] - sales['RevenueLM']) / (sales['RevenueLM'] + 1e3) * 100
    
    def clear_multi():
        st.session_state.Gender = 'All'
        st.session_state.Age = (20, 40)
        st.session_state.Nationality = []
        st.session_state.DepartureDay = []
        st.session_state.DepartureMonth = []
        st.session_state.DepartureYear = []
        st.session_state.Duration = []
        st.session_state.DestinationCity = []
        st.session_state.DestinationCountry = []
        st.session_state.Continent = []
        st.session_state.AccommodationType = []
        st.session_state.TransportationType = []

        return
    reset = st.sidebar.button('Reset', on_click=clear_multi)
    
    with tab0:
        st.markdown('<span style="font-family: SVN-Gilroy; font-size: 32px; font-weight: bold;">REVENUE</span>', unsafe_allow_html=True)
        from datetime import date
        from datetime import datetime
        # d, penetration = 
        # with d:
        # d = st.date_input(label='Today', value=date.today())
        # print(d, datetime.min.time())
        # d = datetime.combine(d, datetime.min.time())
        
        

        # with penetration:
        #     st.write()
        # print(df['DepartureDate'].min().year, df['DepartureDate'].max())

        year, e = st.columns([4,5])
        with year:
            min_year = df['DepartureDate'].min().year
            max_year = df['DepartureDate'].max().year
            if min_year == max_year: min_year -= 1

            year = st.slider(label="**SELECT YEAR**",
                             min_value=min_year, 
                             value=date.today().year, 
                             max_value=max_year)
        with e:
            st.write()
        

        # Month slider
        month, f = st.columns([4,5])
        with month:
            month = st.slider(label="**SELECT MONTH**", 
                              min_value=1, 
                              value=date.today().month, 
                              max_value=12)
        with f: 
            st.write()

        d = datetime(year=year, month=month, day=1, hour=0, minute=0, second=0)
        df_one_year = sales[(sales['LeaveDate'] >= (d - pd.DateOffset(years=1))) & (sales['LeaveDate'] <= d)]
        df_one_year['LeaveDate'] = pd.to_datetime(df_one_year['LeaveDate'])

        st.write('(These two elements are used for the "Revenue By Month" graph)')
        # Display selected year and month
        

        col1, col2= st.columns([0.53, 0.47], gap="small")

        # print(df_one_year)
        
        with col1:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots

            # Create subplots with 1 row and 1 column
            fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

            # Bar chart
            fig.add_trace(
                go.Bar(
                    x=df_one_year['LeaveDate'],
                    y=df_one_year['Revenue'],
                    marker_color='rgb(155, 205, 210)',
                    marker_line_color='black',
                    marker_line_width=1.5,
                    name='Revenue'
                ),
                row=1, col=1
            )

            fig.update_xaxes(title_text='LeaveDate', row=1, col=1)
            fig.update_yaxes(title_text='Revenue', row=1, col=1)

            # Line chart
            fig.add_trace(
                go.Scatter(
                    x=df_one_year['LeaveDate'],
                    y=df_one_year['RevenueGrowthMonth'],
                    mode='lines+markers',
                    marker_color='rgb(179, 19, 18)', 
                    name='LTM Revenue'
                ),
                row=1, col=1, secondary_y=True
            )

            fig.update_yaxes(title_text='LTM Revenue', row=1, col=1, secondary_y=True)
            fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
                              xaxis=dict(title="Leave Day",
                                         title_font=dict(family="SVN-Gilroy",size=14)),
                              yaxis=dict(title="Revenue",
                                         title_font=dict(family="SVN-Gilroy",size=14)),
                              legend=dict(title="",
                                          title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=14)),
                              font=dict(family="SVN-Gilroy",size=14), 
                              width=500, height=500,
                              paper_bgcolor="rgba(255,255,255,0)",plot_bgcolor='rgba(255,255,255,0)')

            fig.update_layout(legend=dict(orientation="h",
                                          entrywidth=80,
                                          yanchor="bottom",
                                          y=1.02,
                                          xanchor="right",
                                          x=1
                                          ))
  
            # fig.update_layout(title='Revenue by Month')

            st.plotly_chart(fig)
            # st.markdown('*Revenue By Month*')
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">REVENUE BY MONTH</span>', unsafe_allow_html=True)
            # txt = st.text_area('', '''
            #    The graph above displays both Revenue and LTM Revenue the company obtained between August 2022 and July 2023, a period of one full year.

            #     ''')
            st.write('**The graph above displays both Revenue and LTM Revenue the company obtained between August 2022 and July 2023, a period of one full year.**')

        with col2:
            threshold=3600
            r = df.groupby('DepartureCountry').sum()['Revenue'].to_frame().reset_index()
            f = r[r['Revenue'] >= threshold]
            f = f.append({'DepartureCountry': 'Other',
                          'Revenue': r[r['Revenue'] < threshold]['Revenue'].sum()}, ignore_index=True)
            fig = px.pie(f, values='Revenue', names='DepartureCountry', width=660, height=440)    
            fig.update_layout(showlegend=True,
                              title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
                              xaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),
                              yaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),
                              legend=dict(title="COUNTRIES",title_font=dict(family="SVN-Gilroy",size=14),
                                          font=dict(family="SVN-Gilroy",size=14)),font=dict(family="SVN-Gilroy",size=14),
                              width=500, height=500,
                              paper_bgcolor="rgba(255,255,255,0)",plot_bgcolor='rgba(255,255,255,0)')

            fig.update_traces(marker=dict(line=dict(color='black', width=1.5)))
            st.plotly_chart(fig)
            # st.markdown('*Revenue By Departure Country*')
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">REVENUE BY DEPARTURE COUNTRY</span>', unsafe_allow_html=True)
            fig.update_layout(title= {'text':'REVENUE BY DEPARTURE COUNTRY','font':{'family':'SVN-Gilroy','size':20}},xaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),yaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),legend=dict(title="COUNTRIES",title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=14)),font=dict(family="SVN-Gilroy",size=14))
            st.write('**The following pie chart displays different shares of departure revenue that top tourist countries receive throughout the observed period.**')
       

    # """ Add Content Tab Gender """
    with tab2:
        st.markdown('<span style="font-family: SVN-Gilroy; font-size: 32px; font-weight: bold;">CUSTOMER TREND</span>', unsafe_allow_html=True)
        col1, col2= st.columns([0.54, 0.46], gap="small")
        from plotly import graph_objects as go
        with col1:
            fig = go.Figure(go.Funnel(
            y = ["Total Customers", "First Time", "Second Time", "Third Time", "Fourth Time","Sixth Time"],
            x = [109, 95, 8, 2, 2, 2],
            textposition = ["inside","inside","inside","outside","outside","outside"],
            textinfo = "value+percent initial",
            opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
            "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
            connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )
            fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
                              xaxis=dict(title="AGE",title_font=dict(family="SVN-Gilroy",size=14)),
                              yaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),
                              legend=dict(title="GENDER",title_font=dict(family="SVN-Gilroy",size=14),
                                          font=dict(family="SVN-Gilroy",size=14)),
                              width=500, height=500,
                              paper_bgcolor='rgba(255, 255, 255, 0)', plot_bgcolor='rgba(255, 255, 255, 0)')
            # fig.update_layout(width=930, height=620)
            st.plotly_chart(fig)
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">FUNNEL CHART ILLUSTRATES THE NUMBER OF CUSTOMERS USING THE SERVICE</span>', unsafe_allow_html=True)
            st.write('**The provided funnel chart depicts the customers’ demographic over how frequently they use the service. A total of 100 customers were observed.**')     
    #  fig = go.Figure(go.Funnel(
    #         y = ["Total Customers", "First Time", "Second Time", "Third Time", "Fourth Time","Sixth Time"],
    #         x = [109, 95, 8, 2, 2, 2],
    #         textposition = "outside",
    #         textinfo = "value+percent initial",
    #         opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    #         "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
    #         connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    # )
    #         fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
    #                           xaxis=dict(title="AGE",title_font=dict(family="SVN-Gilroy",size=14)),
    #                           yaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),
    #                           legend=dict(title="GENDER",title_font=dict(family="SVN-Gilroy",size=14),
    #                                       font=dict(family="SVN-Gilroy",size=14)),
    #                           width=500, height=500)
    #         # fig.update_layout(width=930, height=620)
    #         st.plotly_chart(fig)
    #         st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">FUNNEL CHART ILLUSTRATES THE NUMBER OF CUSTOMERS USING THE SERVICE</span>', unsafe_allow_html=True)
        with col2:
            fig = px.scatter(df, x='Age', y='Revenue',color="Gender", symbol="Gender",width=500, height=500, marginal_x="histogram", marginal_y="histogram")
            fig.update_layout(title= {'text':'<b>TRAVEL INSIGHTS TOTAL COST AND AGE ANALYSIS</b>','font':{'family':'SVN-Gilroy'}},xaxis=dict(title="<b>AGE</b>",title_font=dict(family="SVN-Gilroy")),yaxis=dict(title="<b>TOTAL COST</b>",title_font=dict(family="SVN-Gilroy")),legend=dict(title="COUNTRY",title_font=dict(family="SVN-Gilroy"),font=dict(family="SVN-Gilroy")),font=dict(family="SVN-Gilroy"),paper_bgcolor="rgba(255,255,255,0)",plot_bgcolor='rgba(255,255,255,0)')
            fig.update_traces(marker=dict(size=7, line=dict(width=1,color='DarkSlateGrey')),selector=dict(mode='markers'))
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            st.plotly_chart(fig)
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">TRAVEL INSIGHTS DURATION, TOTAL COST, AND AGE ANALYSIS</span>', unsafe_allow_html=True)
            st.write('**This 3D plot provides insight into the spread of durations and how it relates to total cost and ages. Here we can observe potential patterns, indicated by the plot’s many clusters of data points.**')
    # display dataframe + pie transportation
    with tab3:
        st.markdown('<span style="font-family: SVN-Gilroy; font-size: 32px; font-weight: bold;">ACCOMMODATION-TRANSPORTATION</span>', unsafe_allow_html=True)
        col1, col2= st.columns([0.54, 0.46], gap="small")
        with col1:
            fig = px.box(df, x='AccommodationType', y='AccommodationCost', color='AccommodationType', color_discrete_sequence=px.colors.qualitative.Prism, width=930, height=620)
            fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
                              xaxis=dict(title="<b>TYPES OF ACCOMMODATION</b>",title_font=dict(family="SVN-Gilroy",size=14)),
                              yaxis=dict(title="<b>COST OF ACCOMMODATION</b>",title_font=dict(family="SVN-Gilroy",size=14)),
                              legend=dict(title="<b>GENDER</b>",title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=14)),
                              font=dict(family="SVN-Gilroy",size=14),
                              paper_bgcolor='rgba(255, 255, 255, 0)',
                              plot_bgcolor='rgba(255, 255, 255, 0.1)',
                              width=450, height=450)
            fig.update_traces(showlegend=False)
            st.plotly_chart(fig)
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">BOXPLOT ILLUSTRATES THE PRICE OF ACCOMMODATIONS</span>', unsafe_allow_html=True)
        
        with col2:
            fig = px.box(df, x='TransportationType', y='TransportationCost', color='TransportationType', color_discrete_sequence=px.colors.qualitative.Prism, width=930, height=620)
            fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
                              xaxis=dict(title="<b>TYPES OF TRANSPORTATION</b>",title_font=dict(family="SVN-Gilroy", size=14)),
                              yaxis=dict(title="<b>COST OF TRANSPORTATION</b>",title_font=dict(family="SVN-Gilroy",size=14)),
                              legend=dict(title="GENDER",title_font=dict(family="SVN-Gilroy", size=14),font=dict(family="SVN-Gilroy",size=14)),
                              font=dict(family="SVN-Gilroy",size=14),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0.1)',
                              width=450, height=450)
            fig.update_traces(showlegend=False)
            st.plotly_chart(fig)
            st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">BOXPLOT ILLUSTRATES THE PRICE OF TRANSPORTATIONS</span>', unsafe_allow_html=True)
        st.write('**The following pie chart illustrates various modes of transportation/types of accommodation and their popularity among tourists/travelers.**')

    with tab4:
        # # """ Display Dataframe for each Tab """
        st.title('The Frame')
    # df.drop(['ID', 'DepartureDay', 'DepartureYear', 'DepartureMonth', 'Season', 'DepartureMonthString', 'Revenue', 'CustomerName'], axis='columns', inplace=True)
        st.dataframe(data=df[['Age', 'Gender', 'Nationality', 'DepartureDate', 'Duration', 'DestinationCountry', 'TransportationType', 'AccommodationType', 'Revenue']], width=1500, use_container_width=True)
    # st.dataframe(data=df.style.format({'DepartureYear': lambda x : f'{x}'}))
    
        # with col1:
        #     small_data = df[['TransportationType']]
        #     # print(small_data)

        #     gg = small_data.groupby(['TransportationType']).size().reset_index(name='count')
        #     # print(gg)

        #     fig = px.pie(gg,values="count", names='TransportationType', color_discrete_sequence=['rgb(250, 112, 112)','rgb(161, 194, 152)','rgb(198, 235, 197)','rgb(251, 242, 207)','rgb(165, 241, 233)','rgb(127, 188, 210)'], width=660, height=440)
        #     fig.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.8)
        #     fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
        #                       legend=dict(title="TRANSPORTATION TYPE",title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=13)),
        #                       font=dict(family="SVN-Gilroy",size=14),
        #                       width=500, height=500)
        #     st.plotly_chart(fig)
        #     st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">BARCHART ILLUSTRATES TRAVELLERS CHOICE OF TRANSPORTATION</span>', unsafe_allow_html=True)
        # with col2:
        #     small_data = df[['AccommodationType']]
        #     # print(small_data)

        #     gg = small_data.groupby(['AccommodationType']).size().reset_index(name='count')
        #     # print(gg)

        #     fig = px.pie(gg,values="count", names='AccommodationType', color_discrete_sequence=px.colors.qualitative.Prism, width=660, height=440)
        #     fig.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.8)
        #     fig.update_layout(title= {'text':'','font':{'family':'SVN-Gilroy','size':20}},
        #                       legend=dict(title = "ACCOMMODATION TYPE",title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=13)),
        #                       font=dict(family="SVN-Gilroy",size=14),
        #                       width=500, height=500)
        #     st.plotly_chart(fig)
        #     st.markdown('<span style="font-family: SVN-Gilroy; font-size: 20px; font-weight: bold;">BARCHART ILLUSTRATES TRAVELLERS CHOICE OF TRANSPORTATION</span>', unsafe_allow_html=True)
        # st.write('The following pie chart illustrates various modes of transportation/types of accommodation and their popularity among tourists/travelers.')






#     with tab0:
       
#         from datetime import date
#         from datetime import datetime
# #         st.markdown(
# #     """
# #     <style>
# #     .input-container input {
# #         width: 400px;
# #         font-size: 16px;
# #     }
# #     </style>
# #     """,
# #     unsafe_allow_html=True
# # )
#         d, penetration = st.columns([4, 25])
#         with d:
#             d = st.date_input(label='Today', value=date.today())
#             d = datetime.combine(d, datetime.min.time())
#             df_one_year = sales[(sales['LeaveDate'] >= (d - pd.DateOffset(years=1))) & (sales['LeaveDate'] <= d)]
#             df_one_year['LeaveDate'] = pd.to_datetime(df_one_year['LeaveDate'])
#         with penetration:
#             st.write()

#         col1, col2= st.columns([0.5, 0.5], gap="small")
#         # print(df_one_year)
        
#         with col1:
#             import plotly.graph_objects as go
#             from plotly.subplots import make_subplots

#             # Create subplots with 1 row and 1 column
#             fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

#             # Bar chart
#             fig.add_trace(
#                 go.Bar(
#                     x=df_one_year['LeaveDate'],
#                     y=df_one_year['Revenue'],
#                     marker_color='deepskyblue',
#                     name='Revenue'
#                 ),
#                 row=1, col=1
#             )

#             fig.update_xaxes(title_text='LeaveDate', row=1, col=1)
#             fig.update_yaxes(title_text='Revenue', row=1, col=1)

#             # Line chart
#             fig.add_trace(
#                 go.Scatter(
#                     x=df_one_year['LeaveDate'],
#                     y=df_one_year['RevenueGrowthMonth'],
#                     mode='lines+markers',
#                     marker_color='yellow', 
#                     name='Revenue Last 12 Months'
#                 ),
#                 row=1, col=1, secondary_y=True
#             )

#             fig.update_yaxes(title_text='Revenue Last 12 Months', row=1, col=1, secondary_y=True)
#             fig.update_layout(width=720, height=450)
#             # fig.update_layout(title='Revenue by Month')

#             st.plotly_chart(fig)
#             st.markdown('**Revenue By Month**')

#             # fig, ax1 = plt.subplots()
#             # ax1.bar(df_one_year['LeaveDate'], df_one_year['Revenue'], color='blue')
#             # ax1.set_xlabel('LeaveDate')
#             # ax1.set_ylabel('Revenue')
#             # ax1.set_title('Revenue by Month')
#             # ax2 = ax1.twinx()
#             # ax2.plot(df_one_year['LeaveDate'], df_one_year['RevenueGrowthMonth'], color='red', marker='o')
#             # ax2.set_ylabel('Sales Revenue Last 12 Months')
#             # st.pyplot(fig)

#         with col2:
#             threshold=3000
#             r = df.groupby('DepartureCountry').sum()['Revenue'].to_frame().reset_index()
#             f = r[r['Revenue'] >= threshold]
#             f = f.append({'DepartureCountry': 'Other',
#                           'Revenue': r[r['Revenue'] < threshold]['Revenue'].sum()}, ignore_index=True)
#             fig = px.pie(f, values='Revenue', names='DepartureCountry')    
#             fig.update_layout(showlegend=True, plot_bgcolor="white")
#             st.plotly_chart(fig)
#             st.markdown('**Revenue By Departure Country**')

#         # Add hover to the chart
      
#         # fig = go.Figure(data=[go.Pie(labels=df['Country'], values=df['Revenue'], textinfo=None,
#         #                      insidetextorientation='radial'
#         #                     )])
#         # st.plotly_chart(fig)

#         # df['Percentage'] = df['Revenue'] / df['Revenue'].sum() * 100
#         # import plotly.graph_objects as go
#         # fig = go.Figure(data=[go.Pie(labels=df['Country'], values=df['Percentage'])])
#         # visibility = [fig.update_traces(visible='legendonly') if value < 1 else fig.update_traces(visible=True) for value in df['Percentage']]
#         # fig.update_layout(title='Revenue by Country', showlegend=True)
#         # st.plotly_chart(fig)

#     # """ Add Content Tab Gender """
#     with tab2:
#         from plotly import graph_objects as go

#         fig = go.Figure(go.Funnel(
#         y = ["Total Customers", "First Time", "Second Time", "Third Time", "Fourth Time","Sixth Time"],
#         x = [109, 95, 8, 2, 2, 2],
#         textposition = "outside",
#         textinfo = "value+percent initial",
#         opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
#         "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
#         connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
#     )
#         fig.update_layout(title= {'text':'FUNNEL CHART ILLUSTRATES THE NUMBER OF CUSTOMERS USING THE SERVICE','font':{'family':'SVN-Gilroy','size':20}},xaxis=dict(title="AGE",title_font=dict(family="SVN-Gilroy",size=14)),yaxis=dict(title="",title_font=dict(family="SVN-Gilroy",size=14)),legend=dict(title="GENDER",title_font=dict(family="SVN-Gilroy",size=14),font=dict(family="SVN-Gilroy",size=14)),font=dict(family="SVN-Gilroy",size=14))
#         fig.update_layout(width=1080, height=720)
#         st.plotly_chart(fig)

#     # display dataframe + pie transportation
#     with tab3:
#         st.title('Transporstation')
#         transtype_count = df['TransportationType'].value_counts()
#         fig = px.pie(values=transtype_count.tolist(), 
#                     names=transtype_count.index.tolist(),
#                     title='By transportation')
#         st.plotly_chart(fig)



#     # scatter plot + dataframe
#     with tab4:
#         st.title('Duration, Cost and Age')
    
#         st.title('Travel Insights: Duration, Total Cost, and Age Analysis.')
#         st.markdown(' - The spread of durations and how it relates to total costs and age.')
#         st.markdown(' - Any potential patterns or clusters of data points based on the variables.')
#         st.markdown(' - The concentration or dispersion of data points in different regions of the plot, indicating relationships or trends.')
#         fig = px.scatter_3d(df, x='Duration', y='Revenue', z='Age', color='Gender')\
#                 .update_layout(
#                     scene=dict(
#                     xaxis_title="Duration",
#                     yaxis_title="Total Cost",
#                     zaxis_title="Age"
#                     )
#                     )
#         st.plotly_chart(fig)

#     # Destination
#     with tab5:
        
#         st.title('Destination')
#         transtype_count = df['TransportationType'].value_counts()
        
#         result = df.groupby('DestinationCity').size().reset_index(name='count')
#         result = result.sort_values('count', ascending=True)
        
#         import plotly.express as px
#         fig = px.bar(result,x="count", y="DestinationCity", color="DestinationCity", color_discrete_sequence=px.colors.sequential.Viridis, width=1080, height=720, text_auto= True)
#         fig.update_traces(marker_line_color='rgb(0,0,0)',
#                         marker_line_width=1.5, opacity=0.7)
#         fig.update_layout(title= {'text':'BARCHART ABOUT DESTINATIONS HAVE THE MOST VISITS','font':{'family':'Times New Roman'}},xaxis=dict(title="DestinationCity",title_font=dict(family="Times New Roman")),yaxis=dict(title="Count",title_font=dict(family="Times New Roman")),legend=dict(title="DestinationCity",title_font=dict(family="Times New Roman"),font=dict(family="Times New Roman")),font=dict(family="Times New Roman"))
#         st.plotly_chart(fig)

#     # Continent
#     with tab6:
#         st.title('Continent')
#         continent_count = df['Continent'].value_counts()
        
#         result = df.groupby('Continent').size().reset_index(name='count')
#         result = result.sort_values('count', ascending=False)

#         import plotly.express as px
#         fig = px.bar(result,x="Continent", y="count", color="Continent", width=1080, height=720, text_auto= True, color_discrete_sequence=px.colors.qualitative.Prism)
#         fig.update_traces(marker_line_color='rgb(0,0,0)',
#                           marker_line_width=1.5, opacity=0.7)
#         fig.update_layout(title= {'text':'BARCHART ABOUT CONTINENT','font':{'family':'Times New Roman'}},xaxis=dict(title="DestinationCity",title_font=dict(family="Times New Roman")),yaxis=dict(title="Count",title_font=dict(family="Times New Roman")),legend=dict(title="DestinationCity",title_font=dict(family="Times New Roman"),font=dict(family="Times New Roman")),font=dict(family="Times New Roman"))
#         st.plotly_chart(fig)

#     # Scatterplot
#     # with tab7:
