import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly_express as px
import json
import requests
from PIL import Image


#dataframe creation

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database = "phonepe"
)

mycursor = mydb.cursor()

#aggre_transaction_DF

mycursor.execute("SELECT * FROM aggregated_transaction")

table_1 = mycursor.fetchall()
mydb.commit()

Aggregated_transaction = pd.DataFrame(table_1,columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))



#aggre_user_DF

mycursor.execute("SELECT * FROM aggregated_user")

table_2 = mycursor.fetchall()
mydb.commit()

Aggregated_user = pd.DataFrame(table_2,columns=("States", "Years", "Quarter", "Brands","Transaction_count","Percentage"))



#Map_transaction_DF

mycursor.execute("SELECT * FROM map_transaction")

table_3 = mycursor.fetchall()
mydb.commit()

Map_transaction = pd.DataFrame(table_3,columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


#Map_user_DF

mycursor.execute("SELECT * FROM map_user")

table_4 = mycursor.fetchall()
mydb.commit()

Map_user = pd.DataFrame(table_4,columns=("States", "Years", "Quarter", "District", "registeredUsers", "appOpens"))


#top_transaction_DF

mycursor.execute("SELECT * FROM top_transaction")

table_5 = mycursor.fetchall()
mydb.commit()

top_transaction = pd.DataFrame(table_5,columns=("States", "Years", "Quarter", "Pincode", "Transaction_count", "Transaction_amount"))


#top_user_DF

mycursor.execute("SELECT * FROM top_user")

table_6 = mycursor.fetchall()
mydb.commit()

top_user = pd.DataFrame(table_6,columns=("States", "Years", "Quarter", "Pincodes", "registeredUsers"))




def Transaction_count_amount(df,year):

    Tran_Amount_Count_Year = df[df["Years"] == year]

    Tran_Amount_Count_Year.reset_index(drop= True, inplace=True)

    Tran_Amount_Count_Year_group = Tran_Amount_Count_Year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Amount_Count_Year_group.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        fig_amount = px.bar(Tran_Amount_Count_Year_group, x ="States", y = "Transaction_amount", 
                        title=f"{year} TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Redor_r,
                        height=650,width=650)
        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count = px.bar(Tran_Amount_Count_Year_group, x ="States", y = "Transaction_count", 
                            title=f"{year} TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Blugrn,
                            height=650,width=650)
        st.plotly_chart(fig_count)


    
    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)

        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()


        fig_india_1 = px.choropleth(Tran_Amount_Count_Year_group, geojson = data1, locations="States",featureidkey="properties.ST_NM", color= "Transaction_amount",
                                    color_continuous_scale="Rainbow", range_color=(Tran_Amount_Count_Year_group["Transaction_amount"].min(),Tran_Amount_Count_Year_group["Transaction_amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",height=650,width=650)


        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(Tran_Amount_Count_Year_group, geojson = data1, locations="States",featureidkey="properties.ST_NM", color= "Transaction_count",
                                    color_continuous_scale="Rainbow", range_color=(Tran_Amount_Count_Year_group["Transaction_count"].min(),Tran_Amount_Count_Year_group["Transaction_count"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",height=650,width=650)


        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)

        return Tran_Amount_Count_Year


def Transaction_count_amount_Quarter(df,Quarter):
    Tran_Amount_Count_Year = df[df["Quarter"] == Quarter]
    Tran_Amount_Count_Year.reset_index(drop= True, inplace=True)

    Tran_Amount_Count_Year_group = Tran_Amount_Count_Year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Amount_Count_Year_group.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(Tran_Amount_Count_Year_group, x ="States", y = "Transaction_amount", 
                            title=f"{transaction_A_C['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Redor_r,height=650,width=650)
        st.plotly_chart(fig_amount)

    with col2 :
        fig_amount = px.bar(Tran_Amount_Count_Year_group, x ="States", y = "Transaction_count", 
                            title=f"{transaction_A_C['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Blugrn,height=650,width=650)
        st.plotly_chart(fig_amount)


    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)

        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()


        fig_india_1 = px.choropleth(Tran_Amount_Count_Year_group, geojson = data1, locations="States",featureidkey="properties.ST_NM", color= "Transaction_amount",
                                    color_continuous_scale="Rainbow", range_color=(Tran_Amount_Count_Year_group["Transaction_amount"].min(),Tran_Amount_Count_Year_group["Transaction_amount"].max()),
                                    hover_name="States", title=f"{transaction_A_C['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",height=650,width=650)


        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)


    with col2:
        fig_india_2 = px.choropleth(Tran_Amount_Count_Year_group, geojson = data1, locations="States",featureidkey="properties.ST_NM", color= "Transaction_count",
                                        color_continuous_scale="Rainbow", range_color=(Tran_Amount_Count_Year_group["Transaction_count"].min(),Tran_Amount_Count_Year_group["Transaction_count"].max()),
                                        hover_name="States", title=f"{transaction_A_C['Years'].min()} YEAR {Quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",height=650,width=650)
        fig_india_2.update_geos(visible =False)
        st.plotly_chart(fig_india_2)

    return Tran_Amount_Count_Year


def Aggre_tran_type(df,state):

    Tran_Amount_Count_Year = df[df["States"] == state]
    Tran_Amount_Count_Year.reset_index(drop = True, inplace=True)

    Tran_Amount_Count_Year_group = Tran_Amount_Count_Year.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Amount_Count_Year_group.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fif_pie_1 = px.pie(data_frame=Tran_Amount_Count_Year_group,names="Transaction_type", values = "Transaction_amount",
                        width = 650, title = f"{state.upper()} TRANSACTION_AMOUNT",hole = 0.3)

        st.plotly_chart(fif_pie_1)

    with col2:
        fif_pie_2 = px.pie(data_frame=Tran_Amount_Count_Year_group,names="Transaction_type", values = "Transaction_count",
                        width = 650, title = f"{state.upper()} TRANSACTION_COUNT",hole = 0.3)

        st.plotly_chart(fif_pie_2)


# aggre user analysis
def Aggre_user_plot1(df,year):

    Agg_user_year = df[df["Years"] == year]
    Agg_user_year.reset_index(drop=True , inplace=True)
    

    Agg_user_year_group = Agg_user_year.groupby("Brands")[["Transaction_count"]].sum()
    Agg_user_year_group.reset_index(inplace=True)

    fig_bar_1 = px.bar(Agg_user_year_group,x='Brands',y='Transaction_count',title=f"{year} BRAND AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.haline_r,hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return Agg_user_year


#Aggre_user_analysis_2

def Aggre_user_plot2(df,quarter):

    Agg_user_year_quarter = df[df["Quarter"] == quarter]
    Agg_user_year_quarter.reset_index(drop=True , inplace=True)


    Agg_user_year_quarter_group = Agg_user_year_quarter.groupby("Brands")[["Transaction_count"]].sum()
    Agg_user_year_quarter_group.reset_index(inplace=True)


    fig_bar_1 = px.bar(Agg_user_year_quarter_group, x='Brands', y='Transaction_count',title= f"{quarter} QUARTER BRAND AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.Magenta_r,hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return Agg_user_year_quarter


#aggregated user analysis 3
def Aggre_user_plot3(df,state):

    Agg_user_year_quarter_state = df[df["States"] == state]
    Agg_user_year_quarter_state.reset_index(drop=True , inplace = True)

    fig_line_1 = px.line(Agg_user_year_quarter_state, x= "Brands", y = "Transaction_count" , hover_data= "Percentage",
                    title = f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width = 1000 , markers = True)

    st.plotly_chart(fig_line_1)



#map_transaction_district

def Map_tran_District(df,state):

    Tran_Amount_Count_Year = df[df["States"] == state]
    Tran_Amount_Count_Year.reset_index(drop = True, inplace=True)

    Tran_Amount_Count_Year_group = Tran_Amount_Count_Year.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Amount_Count_Year_group.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fif_bar_1 = px.bar(Tran_Amount_Count_Year_group, x= "Transaction_amount", y="District", orientation= "h", height = 800,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Mint_r)

        st.plotly_chart(fif_bar_1)

    with col2:
        fif_bar_2 = px.bar(Tran_Amount_Count_Year_group, x= "Transaction_count", y="District", orientation= "h", height = 800,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Mint)

        st.plotly_chart(fif_bar_2)


#Map user analysis 1

def map_user_plot1(df, year):
    map_user_year = df[df["Years"] == year]
    map_user_year.reset_index(drop=True , inplace=True)

    map_user_year_group = map_user_year.groupby("States")[["registeredUsers", "appOpens"]].sum()
    map_user_year_group.reset_index(inplace=True)


    fig_line_1 = px.line(map_user_year_group, x= "States", y = ["registeredUsers", "appOpens"] ,
                    title = f"{year} REGISTERUSER & APPOPENS", width = 1000, height = 800 , markers = True)

    st.plotly_chart(fig_line_1)

    return map_user_year


#Map user analysis 2

def map_user_plot2(df, quarter):
    map_user_year_quarter = df[df["Quarter"] == quarter]
    map_user_year_quarter.reset_index(drop=True , inplace=True)

    map_user_year_quarter_group = map_user_year_quarter.groupby("States")[["registeredUsers", "appOpens"]].sum()
    map_user_year_quarter_group.reset_index(inplace=True)


    fig_line_1 = px.line(map_user_year_quarter_group, x= "States", y = ["registeredUsers", "appOpens"] ,
                    title = f"{df["Years"].min()} {quarter}  QUARTER REGISTERUSER & APPOPENS", width = 1000, height = 800 , markers = True,
                    color_discrete_sequence = px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_line_1)

    return map_user_year_quarter



#Map user analysis 3

def map_user_plot3(df, state):
    map_user_year_quarter_state = df[df["States"] == state]
    map_user_year_quarter_state.reset_index(drop=True , inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(map_user_year_quarter_state, x= "registeredUsers", y = "District" , orientation= "h",
                        title = f"{state.upper()} REGISTERUSER", width = 1000, height = 800,
                        color_discrete_sequence = px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(map_user_year_quarter_state, x= "appOpens", y = "District" , orientation= "h",
                        title = f"{state.upper()} APPOPENS", width = 1000, height = 800,
                        color_discrete_sequence = px.colors.sequential.Rainbow)

        st.plotly_chart(fig_bar_2)



# top transaction plot 1
def top_transaction_plot1(df,state):
        
    top_transaction_year_state = df[df["States"] == state]
    top_transaction_year_state.reset_index(drop=True , inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(top_transaction_year_state, x= "Quarter", y = "Transaction_amount" , hover_data= "Pincode",
                        title = " TRANSACTION AMOUNT", width = 1000, height = 800,
                        color_discrete_sequence = px.colors.sequential.Mint)

        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(top_transaction_year_state, x= "Quarter", y = "Transaction_count" , hover_data= "Pincode",
                        title = " TRANSACTION COUNT", width = 1000, height = 800,
                        color_discrete_sequence = px.colors.sequential.Agsunset_r)

        st.plotly_chart(fig_bar_2)




# top user plot 1
def top_user_plot1(df,year):

    top_user_year = df[df["Years"] == year]
    top_user_year.reset_index(drop=True , inplace=True)

    top_user_year_group = top_user_year.groupby(["States", "Quarter"])[["registeredUsers"]].sum()
    top_user_year_group.reset_index(inplace=True)

    fig_bar_1 = px.bar(top_user_year_group,x='States', y='registeredUsers',color= "Quarter", width = 1000,
                    height = 800, color_discrete_sequence = px.colors.sequential.haline_r, hover_name = "States",
                    title = f"{year} REGISTERED USER")

    st.plotly_chart(fig_bar_1)

    return top_user_year


#top user plot 2

def top_user_plot2(df, States):

    top_user_year_state = df[df["States"] == States]
    top_user_year_state.reset_index(drop=True , inplace=True)

    fig_bar_1 = px.bar(top_user_year_state, x= "Quarter", y = "registeredUsers" ,
                    title = f"{States} REGISTERUSE, PINCODES, QUARTERS ", width = 650,
                    height = 650 , color = "registeredUsers" , hover_data = "Pincodes",
                    color_continuous_scale = px.colors.sequential.Magenta)

    st.plotly_chart(fig_bar_1)




#dataframe creation

def Top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database = "phonepe"
    )

    mycursor = mydb.cursor()




    #plot 1
    query_1 = f'''SELECT States, SUM(Transaction_amount) as Transaction_amount
                From {table_name}
                GROUP BY States
                order by Transaction_amount DESC
                LIMIT 10;'''

    mycursor.execute(query_1)

    table_1 = mycursor.fetchall()

    df_1 =pd.DataFrame(table_1, columns=["States", "Transaction_amount"])

    col1,col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(df_1, x= "States", y = "Transaction_amount" ,title =  "TOP 10 TRANSACTION AMOUNT ", width = 600,height = 650 ,
                        hover_name = "States", color_discrete_sequence = px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_bar_1)



    query_2 = f'''SELECT States, SUM(Transaction_amount) as Transaction_amount
                From {table_name}
                GROUP BY States
                order by Transaction_amount 
                LIMIT 10;'''

    mycursor.execute(query_2)

    table_2 = mycursor.fetchall()

    df_2 =pd.DataFrame(table_2, columns=["States", "Transaction_amount"])


    with col2:
    #plot 2

        fig_bar_2 = px.bar(df_2, x= "States", y = "Transaction_amount" ,title =  "LAST 10 TRANSACTION AMOUNT ", width = 600,
                        hover_name = "States", height = 650 ,color_discrete_sequence = px.colors.sequential.Blues)

        st.plotly_chart(fig_bar_2)




    #plot 3
    query_3 = f'''select States, avg(Transaction_amount) as Transaction_amount
                From {table_name}
                GROUP BY States
                order by Transaction_amount'''

    mycursor.execute(query_3)

    table_3 = mycursor.fetchall()

    df_3 =pd.DataFrame(table_3, columns=["States", "Transaction_amount"])

    fig_bar_3 = px.bar(df_3, y = "States", x = "Transaction_amount" ,title =  "AVERAGE TRANSACTION AMOUNT ", width = 1000,height = 800 ,orientation="h",
                    hover_name = "States", color_discrete_sequence = px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_3)




#dataframe creation

def Top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database = "phonepe"
    )

    mycursor = mydb.cursor()

    #plot 1
    query_1 = f'''SELECT States, SUM(Transaction_count) as Transaction_count
                From {table_name}
                GROUP BY States
                order by Transaction_count DESC
                LIMIT 10;'''

    mycursor.execute(query_1)

    table_1 = mycursor.fetchall()

    col1, col2 = st.columns(2)

    with col1:
        df_1 =pd.DataFrame(table_1, columns=["States", "Transaction_count"])

        fig_bar_1 = px.bar(df_1, x= "States", y = "Transaction_count" ,title =  "TOP 10 TRANSACTION COUNT ", width = 600,
                        hover_name = "States", height = 650 ,color_discrete_sequence = px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_bar_1)

    #plot 2
    query_2 = f'''SELECT States, SUM(Transaction_count) as Transaction_count
                From {table_name}
                GROUP BY States
                order by Transaction_count 
                LIMIT 10;'''

    mycursor.execute(query_2)

    table_2 = mycursor.fetchall()

    with col2:
        df_2 =pd.DataFrame(table_2, columns=["States", "Transaction_count"])

        fig_bar_2 = px.bar(df_2, x= "States", y = "Transaction_count" ,title =  "LAST 10 TRANSACTION COUNT ", width = 600,
                        hover_name = "States", height = 650 ,color_discrete_sequence = px.colors.sequential.Blues)

        st.plotly_chart(fig_bar_2)



    #plot 3
    query_3 = f'''select States, avg(Transaction_count) as Transaction_count
                From {table_name}
                GROUP BY States
                order by Transaction_count'''

    mycursor.execute(query_3)

    table_3 = mycursor.fetchall()

    df_3 =pd.DataFrame(table_3, columns=["States", "Transaction_count"])

    fig_bar_3 = px.bar(df_3, y = "States", x = "Transaction_count" ,title =  "AVERAGE TRANSACTION COUNT ", width = 1000,orientation="h",
                    hover_name = "States", height = 800 ,color_discrete_sequence = px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_3)




#dataframe creation

def Top_chart_registered_user(table_name , state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database = "phonepe"
    )

    mycursor = mydb.cursor()

    #plot 1
    query_1 = f'''select District, sum(registeredUsers) as registeredusers
                from {table_name}
                where States = '{state}'
                group by District
                order by registeredUsers desc
                limit 10'''

    mycursor.execute(query_1)

    table_1 = mycursor.fetchall()

    df_1 =pd.DataFrame(table_1, columns=["District", "registeredUsers"])

    col1,col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(df_1, x= "District", y = "registeredUsers" ,title =  "TOP 10 REGISTERED USER District", width = 600,
                        hover_name = "District", height = 650 ,color_discrete_sequence = px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_bar_1)

    #plot 2
    query_2 = f'''select District, sum(registeredUsers) as registeredUsers
                    from {table_name}
                    where States = '{state}'
                    group by District
                    order by registeredUsers
                    limit 10;'''

    mycursor.execute(query_2)

    table_2 = mycursor.fetchall()

    with col2:
        df_2 =pd.DataFrame(table_2, columns=["District", "registeredUsers"])

        fig_bar_2 = px.bar(df_2, x= "District", y = "registeredUsers" ,title =  "LAST 10 REGISTERED USER District", width = 600,
                        hover_name = "District", height = 650 ,color_discrete_sequence = px.colors.sequential.Blues)

        st.plotly_chart(fig_bar_2)



    #plot 3
    query_3 = f'''select District, avg(registeredUsers) as registeredUsers
                from {table_name}
                where States = '{state}'
                group by District
                order by registeredUsers;'''

    mycursor.execute(query_3)

    table_3 = mycursor.fetchall()

    df_3 =pd.DataFrame(table_3, columns=["District", "registeredUsers"])

    fig_bar_3 = px.bar(df_3, y = "District", x = "registeredUsers" ,title =  "AVERAGE 10 REGISTERED USER District", width = 1000,orientation="h",
                    hover_name = "District", height = 800 ,color_discrete_sequence = px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_3)



#dataframe creation

def Top_chart_appopens(table_name , state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database = "phonepe"
    )

    mycursor = mydb.cursor()

    #plot 1
    query_1 = f'''select District, sum(appOpens) as appOpens
                from {table_name}
                where States = '{state}'
                group by District
                order by appOpens desc
                limit 10'''

    mycursor.execute(query_1)

    table_1 = mycursor.fetchall()

    col1,col2 = st.columns(2)

    with col1:
        df_1 =pd.DataFrame(table_1, columns=["District", "appOpens"])

        fig_bar_1 = px.bar(df_1, x= "District", y = "appOpens" ,title =  "TOP 10 APPOPENS", width = 600,
                        hover_name = "District", height = 650 ,color_discrete_sequence = px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_bar_1)

    #plot 2
    query_2 = f'''select District, sum(appOpens) as appOpens
                    from {table_name}
                    where States = '{state}'
                    group by District
                    order by appOpens
                    limit 10;'''

    mycursor.execute(query_2)

    table_2 = mycursor.fetchall()

    with col2:

        df_2 =pd.DataFrame(table_2, columns=["District", "appOpens"])

        fig_bar_2 = px.bar(df_2, x= "District", y = "appOpens" ,title =  "LAST 10 APPOPENS", width = 600,
                        hover_name = "District", height = 650 ,color_discrete_sequence = px.colors.sequential.Blues)

        st.plotly_chart(fig_bar_2)



    #plot 3
    query_3 = f'''select District, avg(appOpens) as appOpens
                from {table_name}
                where States = '{state}'
                group by District
                order by appOpens;'''

    mycursor.execute(query_3)

    table_3 = mycursor.fetchall()

    df_3 =pd.DataFrame(table_3, columns=["District", "appOpens"])

    fig_bar_3 = px.bar(df_3, y = "District", x = "appOpens" ,title =  "AVERAGE 10 APPOPENS", width = 1000,orientation="h",
                    hover_name = "District", height = 800 ,color_discrete_sequence = px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_3)



#dataframe creation

def Top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database = "phonepe"
    )

    mycursor = mydb.cursor()

    #plot 1
    query_1 = f'''select States, sum(registeredUsers) as registeredUsers
                from {table_name}
                group by States
                order by registeredUsers desc
                limit 10;'''

    mycursor.execute(query_1)

    table_1 = mycursor.fetchall()

    df_1 =pd.DataFrame(table_1, columns=["States", "registeredUsers"])

    col1,col2 = st.columns(2)

    with col1:
        fig_bar_1 = px.bar(df_1, x= "States", y = "registeredUsers" ,title =  "TOP 10 REGISTERED USERS", width = 600,
                        hover_name = "States", height = 650 ,color_discrete_sequence = px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_bar_1)

    #plot 2
    query_2 = f'''select States, sum(registeredUsers) as registeredUsers
                from {table_name}
                group by States
                order by registeredUsers
                limit 10;'''

    mycursor.execute(query_2)

    table_2 = mycursor.fetchall()

    df_2 =pd.DataFrame(table_2, columns=["States", "registeredUsers"])


    with col2:

        fig_bar_2 = px.bar(df_2, x= "States", y = "registeredUsers" ,title =  "LAST 10 REGISTERED USERS", width = 600,
                        hover_name = "States", height = 650 ,color_discrete_sequence = px.colors.sequential.Blues)

        st.plotly_chart(fig_bar_2)



    #plot 3
    query_3 = f'''select States, avg(registeredUsers) as registeredUsers
                    from {table_name}
                    group by States
                    order by registeredUsers ;'''

    mycursor.execute(query_3)

    table_3 = mycursor.fetchall()

    df_3 =pd.DataFrame(table_3, columns=["States", "registeredUsers"])

    fig_bar_3 = px.bar(df_3, y = "States", x = "registeredUsers" ,title =  "AVERAGE 10 REGISTERED USERS", width = 1000,orientation="h",
                    hover_name = "States", height = 800 ,color_discrete_sequence = px.colors.sequential.Bluered_r)

    st.plotly_chart(fig_bar_3)








############################

#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:

    select = option_menu("Dashboard",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME" :

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        
        st.image("C:/Users/prade/OneDrive/Desktop/phonepe project/Untitled.jpg")






elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method_1 = st.radio("Select The Method",["Aggregated Transaction Analysis", "Aggregated User Analysis"])

        if method_1 == "Aggregated Transaction Analysis":

            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:

                years = st.selectbox("SELECT THE YEARS",Aggregated_transaction["Years"].unique())
            transaction_A_C = Transaction_count_amount(Aggregated_transaction,years)


            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE", transaction_A_C["States"].unique())
            Aggre_tran_type(transaction_A_C,states)

            
            col1,col2 = st.columns(2)

            with col1:
                Quarter = st.slider("SELECT THE QUARTER",transaction_A_C["Quarter"].min(),transaction_A_C["Quarter"].max())
            transaction_A_C_Q = Transaction_count_amount_Quarter(transaction_A_C,Quarter)

            
            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE_TY", transaction_A_C_Q["States"].unique())
            Aggre_tran_type(transaction_A_C_Q,states)

        elif method_1 == "Aggregated User Analysis":

            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:

                years = st.selectbox("SELECT THE YEARS",Aggregated_user["Years"].unique())
            Aggregated_user_year = Aggre_user_plot1(Aggregated_user, years)
            
            col1,col2 = st.columns(2)

            with col1:

                Quarter = st.slider("SELECT THE QUARTER",Aggregated_user_year["Quarter"].min(),Aggregated_user_year["Quarter"].max())
            transaction_A_C_Q = Aggre_user_plot2(Aggregated_user_year,Quarter)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE_TY", transaction_A_C_Q["States"].unique())
            Aggre_user_plot3(transaction_A_C_Q,states)           

    
####################################
    with tab2:
        
        method_2 = st.radio("Select The Method",["Map Transaction Analysis", "Map User Analysis"])

        if method_2 == "Map Transaction Analysis":

            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:

                years = st.selectbox("SELECT THE YEARS MAP TRANSACTION",Map_transaction["Years"].unique())
            Map_transaction_A_C = Transaction_count_amount(Map_transaction,years)
                       

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE MAP TRANSACTION", Map_transaction_A_C["States"].unique())
            Map_tran_District(Map_transaction_A_C, states)

            col1,col2 = st.columns(2)
 
            with col1:
                Quarters = st.slider("SELECT THE QUARTERS MAP TRANSACTION",Map_transaction_A_C["Quarter"].min(),Map_transaction_A_C["Quarter"].max())
            MAP_transaction_A_C_Q = Transaction_count_amount_Quarter(Map_transaction_A_C ,Quarters)

            
            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE MAP TRANSACTION", MAP_transaction_A_C_Q["States"].unique(), key="select_state_map_transaction_q")
            Map_tran_District(MAP_transaction_A_C_Q, states) 



        elif method_2 == "Map User Analysis":
            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:

                years = st.selectbox("SELECT THE YEARS MAP USER",Map_user["Years"].unique())   
            MAP_user_year = map_user_plot1(Map_user, years)


            col1,col2 = st.columns(2)

            with col1:

                Quarter = st.slider("SELECT THE QUARTER MAP USER",MAP_user_year["Quarter"].min(),MAP_user_year["Quarter"].max())
            MAP_user_year_quarter = map_user_plot2(MAP_user_year, Quarter)


            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE MAP USER", MAP_user_year_quarter["States"].unique())
            map_user_plot3(MAP_user_year_quarter,states)       


#################################




    with tab3:
        method_3 = st.radio("Select The Method",["Top Transaction Analysis", "Top User Analysis"])

        if method_3 == "Top Transaction Analysis":
            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:

                years = st.selectbox("SELECT THE YEARS TOP TRANSACTION",top_transaction["Years"].unique())
            Top_transaction_year = Transaction_count_amount(top_transaction, years)
                   
            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE TOP TRANSACTION", Top_transaction_year["States"].unique())
            top_transaction_plot1(Top_transaction_year, states)  


            col1,col2 = st.columns(2)
            with col1:

                Quarter = st.slider("SELECT THE QUARTER TOP TRANSACTION",Top_transaction_year["Quarter"].min(),Top_transaction_year["Quarter"].max())
            top_transaction_A_C_Q = Transaction_count_amount_Quarter(Top_transaction_year ,Quarter)

            

        elif method_3 == "Top User Analysis":

            col1,col2,col3,col4,col5,col6 = st.columns(6)

            with col1:
                years = st.selectbox("SELECT THE YEARS TOP USER",top_user["Years"].unique())   
            top_user_year = top_user_plot1(top_user,years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("SELECT THE STATE TOP USER", top_user_year["States"].unique())
            top_user_plot2(top_user_year, states) 
            





###################


elif select == "TOP CHARTS":
    
    question = st.selectbox("select the Question", ["1. Transaction Amount and Count of Aggregated Transaction",
                            
                            "2. Transaction Amount and Count of Map transaction",

                            "3. Transaction count of Top Transaction",

                            "4. Transaction count of Aggregated user ",

                            "5. Registered Users of Map User",

                            "6. App oppens of Map User",

                            "7. Registered User of Top User"])


    if question == "1. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_transaction")


        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_transaction")


    elif question == "2. Transaction Amount and Count of Map transaction":

        st.subheader("MAP AMOUNT")
        Top_chart_transaction_amount("map_transaction")


        st.subheader("MAP COUNT")
        Top_chart_transaction_count("map_transaction")

    
    elif question == "3. Transaction count of Top Transaction":

        st.subheader("TOP AMOUNT")
        Top_chart_transaction_amount("top_transaction")


        st.subheader("TOP COUNT")
        Top_chart_transaction_count("top_transaction")


    elif question == "4. Transaction count of Aggregated user ":

        st.subheader("TOP COUNT")
        Top_chart_transaction_count("aggregated_transaction")


    elif question == "5. Registered Users of Map User":

        state = st.selectbox("Select the state", Map_user["States"].unique()) 
        st.subheader("TOP AMOUNT")
        Top_chart_registered_user("map_user",state)



    elif question == "6. App oppens of Map User":

        state = st.selectbox("Select the state", Map_user["States"].unique()) 
        st.subheader("TOP AMOUNT")
        Top_chart_appopens("map_user",state)



    elif question == "7. Registered User of Top User":

        st.subheader("REGISTERED USERS")
        Top_chart_registered_users("top_user")







        