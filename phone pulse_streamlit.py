import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px


conn=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="Kavidhina@5566",
                      port=5432,
                      database="phonepe_pulse")
cursor=conn.cursor()

styled_text = "<p style='font-size: 40px; font-weight: bold;color:magenta;'>Phonepe Pulse Data Visualization and Exploration:</p>"
st.markdown(styled_text, unsafe_allow_html=True)


with st.sidebar:
    
    page=['About','Data Exploration','State & District wise',"Overall Stats"]
    select_page=st.selectbox('select the page',page)
    


def format_amount_inr(amount):
    crore_amount = amount / 10000000  # Divide by 10,000,000 to convert to Crore
    rounded_crore_amount = round(crore_amount)  # Round off the Crore amount
    formatted_amount = '₹{:,.0f} Cr'.format(rounded_crore_amount)
    return formatted_amount

if select_page =='About':
    st.write("The Phonepe pulse Github repository contains a large amount of data related to"
            "various metrics and statistics. The goal is to extract this data and process it to obtain"
           " insights and information that can be visualized in a user-friendly manner.")
    st.write("The solution must be secure, efficient, and user-friendly. The dashboard must be"
             "easily accessible and provide valuable insights and information about the data in the"
             "Phonepe pulse Github repository.")
    st.write("Users will be able to access the dashboard from a web browser and easily navigate"
             "the different visualizations and facts and figures displayed. The dashboard will"
             "provide valuable insights and information about the data in the Phonepe pulse"
            " Github repository, making it a valuable tool for data analysis and decision-making.")
            
    st.write("Overall, the result of this project will be a comprehensive and user-friendly solution"
             "for extracting, transforming, and visualizing data from the Phonepe pulse Github"
             "repository.")
    st.write("Contact Details :")
    st.write(">>Linkedin page: https://www.linkedin.com/in/kaviyarasan-e-906826180/")
    st.write(">>Github repository: https://github.com/kaviyarasanEaswaran/Phonepe-Pulse-Data-Visualization-and-Exploration-/tree/63adabe2d10d7faa4fc4f1ed7fde5899f9e95c98")


    

if select_page == 'Data Exploration':
    with st.sidebar:
        options = ['User', 'Transaction']
        selected_option = st.selectbox('Type', options)
        year = [2018, 2019, 2020, 2021, 2022]
        selected_year = st.selectbox('Select the year', year)
        quarter = ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (July-Sep)', 'Q4 (Oct-Dec)']
        selected_quarter = st.selectbox('Select the quarter', quarter)
    if selected_option == 'Transaction':
        tab1, tab2 = st.tabs(["Total_Transaction_Count", "Total_Transaction_Amount"])
        if selected_year and selected_quarter:
            with tab1:
                col1, col2 = st.columns([2.5, 1]) 
                with col1:
                    #1 Transaction user According To year and Quarter Statewise bar plot
                    query1 = f"SELECT state ,sum(count) as count FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' group by state order by count desc"
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    fig = px.bar(df1,
                    title='Total_Transaction  According To year and Quarter Statewise' ,
                    x="state",
                    y="count",
                    orientation='v',
                    color='count',
                    color_continuous_scale='Blues')
                    st.plotly_chart(fig,use_container_width=True)
                   
                    #2 Transaction user According To year and Quarter Category wise bar plot
                    query1 = f"SELECT categories,sum(count) as count FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' group by categories order by count desc "
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    fig = px.bar(df1,
                    title='Total_Transaction  According To year and Quarter Category wise' ,
                    x="categories",
                    y="count",
                    orientation='v',
                    color='count',
                    color_continuous_scale=px.colors.sequential.Magenta)
                    st.plotly_chart(fig,use_container_width=True)
    
                with col2:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.subheader('Transactions :')
                    query1=f"select sum(count) from aggre_trans_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                    cursor.execute(query1)
                    result1=int(cursor.fetchone()[0])
                    formatted_amount1 = '{:,}'.format(result1)
                    styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe transactions (UPI + Cards + Wallets)</p>"
                    styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    col2_a,col2_b=st.columns([1,1])
                    with col2_a:
                        query2=f"select sum(amount) from aggre_trans_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                        cursor.execute(query2)
                        result2=int(cursor.fetchone()[0])
                        formatted_result2 = format_amount_inr(result2)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All payment Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result2}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    with col2_b:
                        result3 = round(result2/result1)
                        formatted_result3 = '₹{:,}'.format(result3)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>Avg. Trans. Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result3}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                        
                    st.subheader('Categories :')
                    query = f"select Categories, count from aggre_trans_year_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' " 
                    cursor.execute(query)
                    result=cursor.fetchall()
                    # Execute each query and fetch the results
                    df =pd.DataFrame(result,columns=['Categories','count'])
                    for val in range(len(df['Categories'])):
                        formatted_result = '{:,} '.format(df['count'][val]) # Format the result with commas
                        Categories = df['Categories'][val]
                        styled_text = f"<span style='font-size: 15px; font-weight: bold;'>{Categories}  :          </span> <span style='font-size: 15px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.subheader("Top 10 Toal_Trasaction_Count ")
                    col2_c,col2_d,col2_e=st.columns([1,1,1])
                    
                    with col2_c:
                        b1=st.button("States")
                    with col2_d:
                        b2=st.button("Districts")
                    with col2_e:
                        b3=st.button("Pincode")
                    
                    if b1:
                        st.subheader('Top 10 states')
                        query=f"SELECT state,state_count FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col1:
                            
                            cursor.execute(query)
                            result1=cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.bar(df1,
                            title='Top 10 states According To year and Quarter' ,
                            x="state",
                            y="state_count",
                            orientation='v',
                            color='state_count',
                            color_continuous_scale=px.colors.sequential.Magenta)
                            st.plotly_chart(fig,use_container_width=True)
            
                    if b2:
                        
                        st.subheader('Top 10 Districts')
                        query=f"SELECT district,district_count FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col1:
                            cursor.execute(query)
                            result1=cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.bar(df1,
                            title='Top 10 districts According To year and Quarter' ,
                            x="district",
                            y="district_count",
                            orientation='v',
                            color='district_count',
                            color_continuous_scale=px.colors.sequential.Magenta)
                            st.plotly_chart(fig,use_container_width=True)
                            
                        
                    if b3:
                       
                        st.subheader('Top 10 Pinocdes')
                        query=f"SELECT pincode,pincode_count FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col1:
                            cursor.execute(query)
                            result1 = cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.pie(df1, values='pincode_count', names='pincode', title='Top 10 districts According To year and Quarter brand wise')
                            fig.update_traces(textposition='outside', textinfo='label+percent')
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    with col1:
                         st.write("")
                         st.write("")
                         st.write("")
                         st.write("")
                         st.subheader('Toal_Trasaction_Count in Geo Visualization : ')
                         cursor.execute(f"select state, sum(count) as Total_Transactions_Count from map_trans_state_wise where year = '{selected_year}' and quarter = '{selected_quarter[:2]}' group by state order by state")
                         df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions_Count'])
                         df1['Total_Transactions_Count'] = df1['Total_Transactions_Count'] / 1000000
                         df1['Total_Transactions_Count'] = df1['Total_Transactions_Count'].apply(lambda x: '{:} M'.format(x))
                         df2 = pd.read_csv("D:\Data Science\Datasets\Statenames.csv")
                         df1.State = df2
                         fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                   featureidkey='properties.ST_NM',
                                   locations='State',
                                   color='Total_Transactions_Count',
                                   color_continuous_scale='Magenta')
                         fig.update_geos(fitbounds="locations", visible= False)
                         st.plotly_chart(fig,use_container_width=True)
                   
            with tab2:
                col3, col4 = st.columns([2, 1]) 
                with col3:
                   #1 Transaction amount According To year and Quarter state wise
                   query1 = f"SELECT  state,sum(amount) as amount FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' group by state order by amount desc"
                   cursor.execute(query1)
                   result1 = cursor.fetchall()
                   df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                   fig = px.bar(df1,
                   title='Total_Amount According To year and Quarter state wise' ,
                   x="state",
                   y="amount",
                   orientation='v',
                   color='amount',
                   color_continuous_scale=px.colors.sequential.Magenta)
                   st.plotly_chart(fig,use_container_width=True)
                   
                   #2 Transaction amount According To year and Quarter Category wise
                   query1 = f"SELECT categories,sum(amount) as amount FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' group by categories order by amount desc"
                   cursor.execute(query1)
                   result1 = cursor.fetchall()
                   df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                   fig = px.bar(df1,
                   title='Total_Amount  According To year and Quarter Category wise' ,
                   x="categories",
                   y="amount",
                   orientation='v',
                   color='amount',
                   color_continuous_scale=px.colors.sequential.Magenta)
                   st.plotly_chart(fig,use_container_width=True)
                   
                   
    
                with col4:
                    st.subheader('Transactions :')
                    query1=f"select sum(count) from aggre_trans_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                    cursor.execute(query1)
                    result1=int(cursor.fetchone()[0])
                    formatted_amount1 = '{:,}'.format(result1)
                    styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe transactions (UPI + Cards + Wallets)</p>"
                    styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    col4_a,col4_b=st.columns([1,1])
                    with col4_a:
                        query2=f"select sum(amount) from aggre_trans_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                        cursor.execute(query2)
                        result2=int(cursor.fetchone()[0])
                        formatted_result2 = format_amount_inr(result2)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All payment Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result2}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    with col4_b:
                        result3 = round(result2/result1)
                        formatted_result3 = '₹{:,}'.format(result3)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>Avg. Trans. Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result3}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    
                        
                    
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("") 
                    queries = [
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Merchant payments'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Peer-to-peer payments'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Recharge & bill payments'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Financial Services'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Others'"
                        ]
                    st.subheader('Categories :')
                    # Execute each query and fetch the results
                    categories = ['Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments', 'Financial Services', 'Others']
                    for query in range(len(queries)):
                        cursor.execute(queries[query])
                        result = int(cursor.fetchone()[0])
                        formatted_result = '{:,}'.format(result)  # Format the result with commas
                        styled_text = f"<span style='font-size: 15px; font-weight: bold;'>{categories[query]}  :          </span> <span style='font-size: 15px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                                           
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")                                          
                    st.subheader("Top 10 Total_Trasaction_Amount ")
                    col4_c,col4_d,col4_e=st.columns([1,1,1])
                    
                    with col4_c:
                        b4=st.button("state")
                    with col4_d:
                        b5=st.button("district")
                    with col4_e:
                        b6=st.button("pincode")
                    
                    if b4:
                        st.subheader('Top 10 states')
                        query=f"SELECT state,state_amount FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order by state_amount desc "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col3:
                            cursor.execute(query)
                            result1=cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.bar(df1,
                            title='Top 10 states According To year and Quarter' ,
                            x="state",
                            y="state_amount",
                            orientation='v',
                            color='state_amount',
                            color_continuous_scale=px.colors.sequential.Magenta)
                            st.plotly_chart(fig,use_container_width=True)
            
                    if b5:
                        st.subheader('Top 10 Districts')
                        query=f"SELECT district,district_amount FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}'order by district_amount desc "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col3:
                            cursor.execute(query)
                            result1=cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.bar(df1,
                            title='Top 10 districts According To year and Quarter' ,
                            x="district",
                            y="district_amount",
                            orientation='v',
                            color='district_amount',
                            color_continuous_scale=px.colors.sequential.Magenta)
                            st.plotly_chart(fig,use_container_width=True)
                            
                        
                    if b6:
                        st.subheader('Top 10 Pinocdes')
                        query=f"SELECT pincode,pincode_amount FROM public.top_trans_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                        cursor.execute(query)
                        val=cursor.fetchall()
                        df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                        st.dataframe(df)
                        with col3:
                            cursor.execute(query)
                            result1 = cursor.fetchall()
                            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                            fig = px.pie(df1, values='pincode_amount', names='pincode', title='Top 10 pincodes According To year and Quarter ')
                            fig.update_traces(textposition='outside', textinfo='label+percent')
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    with col3:
                        st.subheader('Toal_Trasaction_Amount in Geo Visualization : ')
                        cursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans_state_wise where year = '{selected_year}' and quarter = '{selected_quarter[:2]}' group by state order by state")
                        df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                        df2 = pd.read_csv("D:\Data Science\Datasets\Statenames.csv")
                        df1.State = df2
                        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                  featureidkey='properties.ST_NM',
                                  locations='State',
                                  color='Total_amount',
                                  color_continuous_scale='Magenta')
                        
                        fig.update_geos(fitbounds="locations", visible= False)
                        st.plotly_chart(fig,use_container_width=True)
              
    elif selected_option == 'User' :
        tab3, tab4 = st.tabs(["Total_Registered_User", "Total_App_Open"])
        if selected_year and selected_quarter:
                with tab3:
                    col5, col6 = st.columns([2.5, 1]) 
                    with col5:
                        #1 Total_Registered_User According To year and Quarter state wise
                        query1=f"select distinct(registered_user),state from aggre_user_state_wise where quarter='{selected_quarter[:2]}' and year='{selected_year}' order by registered_user desc"
                        cursor.execute(query1)
                        result1=cursor.fetchall()
                        df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                        fig = px.bar(df1,
                        title='Total_Registered_User According To year and Quarter  state wise' ,
                        x="state",
                        y="registered_user",
                        orientation='v',
                        color='registered_user',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=True)
                        
                       
                    with col6:
                        
                        #1 All PhonePe users
                        st.subheader('Registered_Users :')
                        query1=f"select sum(registered_user) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                        cursor.execute(query1)
                        result1=int(cursor.fetchone()[0])
                        formatted_amount1 = '{:,}'.format(result1)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe users </p>"
                        styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                                           
                        #2 All PhonePe App_open
                        query1=f"select sum(app_open) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                        cursor.execute(query1)
                        result1=int(cursor.fetchone()[0])
                        formatted_amount1 = '{:,}'.format(result1)
                        if result1== 0:
                            formatted_amount1='Unavailable'
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe App_open </p>"
                        styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)   
                        
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.subheader("Top 10 Total_Registered_User ")
                        selected_option=st.selectbox('select_option',["","states","districts","pincode"])                   
                        if selected_option=='states':
                            st.subheader('Top 10 states')
                            query=f"SELECT state,state_registered_user FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                            cursor.execute(query)
                            val=cursor.fetchall()
                            df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                            st.dataframe(df)
                            with col5:
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                cursor.execute(query)
                                result1=cursor.fetchall()
                                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                                fig = px.bar(df1,
                                title='Top 10 states According To year and Quarter' ,
                                x="state",
                                y="state_registered_user",
                                orientation='v',
                                color='state_registered_user',
                                color_continuous_scale=px.colors.sequential.Magenta)
                                st.plotly_chart(fig,use_container_width=True)
                
                        if selected_option=='districts':
                            st.subheader('Top 10 Districts')
                            query=f"SELECT district,district_registered_users FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                            cursor.execute(query)
                            val=cursor.fetchall()
                            df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                            st.dataframe(df)
                            with col5:
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                cursor.execute(query)
                                result1=cursor.fetchall()
                                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                                fig = px.bar(df1,
                                title='Top 10 districts According To year and Quarter' ,
                                x="district",
                                y="district_registered_users",
                                orientation='v',
                                color='district_registered_users',
                                color_continuous_scale=px.colors.sequential.Magenta)
                                st.plotly_chart(fig,use_container_width=True)
                                
                            
                        if selected_option=='pincode':
                            st.subheader('Top 10 Pinocdes')
                            query=f"SELECT pincode,pincode_registered_users FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' "
                            cursor.execute(query)
                            val=cursor.fetchall()
                            df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                            st.dataframe(df)
                            with col5:
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                st.write("")
                                cursor.execute(query)
                                result1 = cursor.fetchall()
                                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                                fig = px.pie(df1, values='pincode_registered_users', names='pincode', title='Top 10 pincodes According To year and Quarter ')
                                fig.update_traces(textposition='outside', textinfo='label+percent')
                                fig.update_layout(showlegend=False)
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col5:
                             st.subheader('Geo Visualization for Total_Registered_User  : ')
                             cursor.execute(f"select state, sum(registered_user) as Total_Registered_User from map_user_state_wise where year = '{selected_year}' and quarter = '{selected_quarter[:2]}' group by state order by state")
                             df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Registered_User'])
                             df1['Total_Registered_User'] = df1['Total_Registered_User'] / 1000000
                             df1['Total_Registered_User'] = df1['Total_Registered_User'].apply(lambda x: '{:} M'.format(x))
                             df2 = pd.read_csv("D:\Data Science\Datasets\Statenames.csv")
                             df1.State = df2
                             fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                       featureidkey='properties.ST_NM',
                                       locations='State',
                                       color='Total_Registered_User',
                                       color_continuous_scale='Magenta')
                             
                             fig.update_geos(fitbounds="locations", visible= False)
                             st.plotly_chart(fig,use_container_width=True)
                with tab4:
                    col7, col8 = st.columns([2.5, 1]) 
                    with col7:
                        #2 Total_App_Open According To year and Quarter brand wise
                        query1=f"select state,app_open from aggre_user_state_wise where quarter='{selected_quarter[:2]}' and year='{selected_year}' order by app_open desc"
                        cursor.execute(query1)
                        result1=cursor.fetchall()
                        df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                        fig = px.bar(df1,
                        title='Total_App_Open  According To year and Quarter state wise' ,
                        x="state",
                        y="app_open",
                        orientation='v',
                        color='app_open',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=True)
                        
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")
                        
                        #2 Total_Registered_User According To year and Quarter brand wise
                        
                        query1=f"select brand,sum(count) as total_app_open_count   from aggre_user_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' group by brand order by total_app_open_count desc"
                        cursor.execute(query1)
                        result1=cursor.fetchall()
                        df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                        fig = px.bar(df1,
                        title='Total_App_Open_Count According To year and Quarter brand wise' ,
                        x="brand",
                        y="total_app_open_count",
                        orientation='v',
                        color='total_app_open_count',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=True)
                        
                       
                    with col8:
                       #1 All PhonePe users
                       st.subheader('Registered_Users :')
                       query1=f"select sum(registered_user) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                       cursor.execute(query1)
                       result1=int(cursor.fetchone()[0])
                       frmatted_amount1 = '{:,}'.format(result1)
                       styled_text = "<p style='font-size: 20px; font-weight: bold;'>Total PhonePe users </p>"
                       styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                       st.markdown(styled_text, unsafe_allow_html=True)
                       #2 All PhonePe App_open
                       query1=f"select sum(app_open) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                       cursor.execute(query1)
                       result1=int(cursor.fetchone()[0])
                       formatted_amount1 = '{:,}'.format(result1)
                       if result1== 0:
                           formatted_amount1='Unavailable'
                       styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe App_open </p>"
                       styled_text += f"<p style='font-size: 40px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                       st.markdown(styled_text, unsafe_allow_html=True) 
                       cursor.execute( f"select brand,sum(registered_user) as reg_user  from aggre_user_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' group by brand order by reg_user desc")
                       df =pd.DataFrame(cursor.fetchall(),columns=['brand','reg_user'])
                       for val in range(len(df['brand'])):
                            formatted_result = '{:,}'.format(df1['total_app_open_count'][val]) # Format the result with commas
                            brand = df['brand'][val]
                            styled_text = f"<span style='font-size: 15px; font-weight: bold;'>{brand}  :          </span> <span style='font-size: 15px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                            st.markdown(styled_text, unsafe_allow_html=True)
                       
                                          
                         
                       st.subheader("Top 10 Total_App_Open_count")
                       col8_c,col8_d,col8_e=st.columns([1,1,1])
                       
                       with col8_c:
                           b1=st.button("States")
                       with col8_d:
                           b2=st.button("Districts")
                       with col8_e:
                           b3=st.button("brand")
                                        
                       if b1:
                           st.subheader('Top 10 states')
                           query=f"SELECT state,sum(app_open) as app_open_count FROM public.map_user_state_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' group by state order by app_open_count desc limit 10"
                           cursor.execute(query)
                           val=cursor.fetchall()
                           df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                           st.dataframe(df)
                           with col7:
                               query=f"SELECT state,sum(app_open) as app_open_count FROM public.map_user_state_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' group by state order by app_open_count desc limit 10"
                               cursor.execute(query)
                               result1=cursor.fetchall()
                               df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                               fig = px.bar(df1,
                               title='Top 10 states According To year and Quarter' ,
                               x="state",
                               y="app_open_count",
                               orientation='v',
                               color='app_open_count',
                               color_continuous_scale=px.colors.sequential.Magenta)
                               st.plotly_chart(fig,use_container_width=True)
               
                       if b2:
                           st.subheader('Top 10 Districts')
                           query=f"SELECT district,sum(app_open) as app_open_count FROM public.map_user_state_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' group by district order by app_open_count desc limit 10"
                           cursor.execute(query)
                           val=cursor.fetchall()
                           df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                           st.dataframe(df)
                           with col7:
                               cursor.execute(query)
                               result1=cursor.fetchall()
                               df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                               fig = px.bar(df1,
                               title='Top 10 districts According To year and Quarter' ,
                               x="district",
                               y="app_open_count",
                               orientation='v',
                               color='app_open_count',
                               color_continuous_scale=px.colors.sequential.Magenta)
                               st.plotly_chart(fig,use_container_width=True)
                       if b3:
                           st.subheader('Top 10 brands')
                           query=f"SELECT brand,count as app_open_count FROM public.aggre_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order by app_open_count desc limit 10"
                           cursor.execute(query)
                           val=cursor.fetchall()
                           df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                           st.dataframe(df)
                           with col7:
                               cursor.execute(query)
                               result1=cursor.fetchall()
                               df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                               fig = px.bar(df1,
                               title='Top 10 districts According To year and Quarter' ,
                               x="brand",
                               y="app_open_count",
                               orientation='v',
                               color='app_open_count',
                               color_continuous_scale=px.colors.sequential.Magenta)
                               st.plotly_chart(fig,use_container_width=True)
                       with col7:
                              st.subheader('Geo Visualization for Total_App_Open_count : ')
                              cursor.execute(f"select state, sum(app_open) as Total_App_Open from map_user_state_wise where year = '{selected_year}' and quarter = '{selected_quarter[:2]}' group by state order by state")
                              df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_App_Open'])
                              df1['Total_App_Open'] = df1['Total_App_Open'] / 1000000
                              df1['Total_App_Open'] = df1['Total_App_Open'].apply(lambda x: '{:} M'.format(x))
                              df2 = pd.read_csv("D:\Data Science\Datasets\Statenames.csv")
                              df1.State = df2
                              fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                        featureidkey='properties.ST_NM',
                                        locations='State',
                                        color='Total_App_Open',
                                        color_continuous_scale='Magenta')
                              
                              fig.update_geos(fitbounds="locations", visible= False)
                              st.plotly_chart(fig,use_container_width=True)
                               
if select_page == 'State & District wise': 
    with st.sidebar:
        options = ['User', 'Transaction']
        selected_option = st.selectbox('Type', options)
        year = [2018, 2019, 2020, 2021, 2022]
        selected_year = st.selectbox('Select the year', year)

        quarter = ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (July-Sep)', 'Q4 (Oct-Dec)']
        selected_quarter = st.selectbox('Select the quarter', quarter)
    if selected_option == 'Transaction':
        tab1, tab2= st.tabs(["Total_Transaction_Count", "Total_Transaction_Amount"])
        with tab1:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select the state', state_list)
            col1, col2 = st.columns([2.5, 1])
            with col1:
                if selected_state:   
                     query1 = f"SELECT categories,sum(count) as total_count FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' group by categories order by total_count desc"
                     cursor.execute(query1)
                     result1 = cursor.fetchall()
                     df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                     fig = px.bar(df1,
                     title='Total_Transaction_count  According To year and Quarter Category wise' ,
                     x="categories",
                     y="total_count",
                     orientation='v',
                     color='total_count',
                     color_continuous_scale=px.colors.sequential.Magenta)
                     st.plotly_chart(fig,use_container_width=True)
                     
                     fig = px.pie(df1, values='total_count', names='categories', title='Total_Transaction_count  According To year and Quarter Category wise ')
                     fig.update_traces(textposition='outside', textinfo='label+percent')
                     fig.update_layout(showlegend=False)
                     st.plotly_chart(fig, use_container_width=True)
            with col2:
                    styled_text = f"<p style='font-size: 20px; font-weight: bold;'>'{selected_state}'-Total_Transactions_Count:</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    query1=f"select sum(count) from aggre_trans_state_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}' and state='{selected_state}'"
                    cursor.execute(query1)
                    result1=int(cursor.fetchone()[0])
                    formatted_amount1 = '{:,}'.format(result1)
                    styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe transactions (UPI + Cards + Wallets)</p>"
                    styled_text += f"<p style='font-size: 30px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    col2_a,col2_b=st.columns([1,1])
                    with col2_a:
                        query2=f"select sum(amount) from aggre_trans_state_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}' and state='{selected_state}'"
                        cursor.execute(query2)
                        result2=int(cursor.fetchone()[0])
                        formatted_result2 = format_amount_inr(result2)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All payment Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result2}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    with col2_b:
                        result3 = round(result2/result1)
                        formatted_result3 = '₹{:,}'.format(result3)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>Avg. Trans. Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result3}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                        
                    queries = [
                        f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Merchant payments' and state='{selected_state}'",
                        f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Peer-to-peer payments' and state='{selected_state}'",
                        f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Recharge & bill payments' and state='{selected_state}'",
                        f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Financial Services' and state='{selected_state}'",
                        f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Others' and state='{selected_state}'"
                        ]
                    st.subheader('Categories :')
                    # Execute each query and fetch the results
                    categories = ['Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments', 'Financial Services', 'Others']
                    for query in range(len(queries)):
                        cursor.execute(queries[query])
                        result = int(cursor.fetchone()[0])
                        formatted_result = '{:,}'.format(result)  # Format the result with commas
                        styled_text = f"<span style='font-size: 15px; font-weight: bold;'>{categories[query]}  :          </span> <span style='font-size: 20px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                        st.markdown(styled_text, unsafe_allow_html=True)
            
            with col1:              
                    query1 = f"SELECT district,count  FROM map_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' order by count desc"
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    fig = px.bar(df1,
                    title=f"Total_Transaction_count  According To year and Quarter '{selected_state}' district wise" ,
                    x="district",
                    y="count",
                    orientation='v',
                    color='count',
                    color_continuous_scale=px.colors.sequential.Magenta)
                    st.plotly_chart(fig,use_container_width=True)
            with col2:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.subheader(f"Total_Transaction_count   insights of '{selected_state}' district ")
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    st.dataframe(df1)
        with tab2:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state2=st.selectbox('Select the State', state_list)
            col1, col2 = st.columns([2.5, 1])
            with col1:
                if selected_state2:   
                     query1 = f"SELECT categories,sum(amount) as total_amount FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' group by categories order by total_amount desc"
                     cursor.execute(query1)
                     result1 = cursor.fetchall()
                     df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                     fig = px.bar(df1,
                     title='Total_Transaction_Amount  According To year and Quarter Category wise' ,
                     x="categories",
                     y="total_amount",
                     orientation='v',
                     color='total_amount',
                     color_continuous_scale=px.colors.sequential.Magenta)
                     st.plotly_chart(fig,use_container_width=True)
                     
                     fig = px.pie(df1, values='total_amount', names='categories', title='Pie-Chart Category wise ')
                     fig.update_traces(textposition='outside', textinfo='label+percent')
                     fig.update_layout(showlegend=False)
                     st.plotly_chart(fig, use_container_width=True)
            with col2:
                    styled_text = f"<p style='font-size: 20px; font-weight: bold;'>'{selected_state}'-Total_Transactions_Amount:</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    query1=f"select sum(amount) from aggre_trans_state_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}' and state='{selected_state}'"
                    cursor.execute(query1)
                    result1=int(cursor.fetchone()[0])
                    formatted_amount1 = '{:,}'.format(result1)
                    styled_text = "<p style='font-size: 20px; font-weight: bold;'>All PhonePe transactions (UPI + Cards + Wallets)</p>"
                    styled_text += f"<p style='font-size: 30px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    col2_a,col2_b=st.columns([1,1])
                    with col2_a:
                        query2=f"select sum(amount) from aggre_trans_state_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}' and state='{selected_state}'"
                        cursor.execute(query2)
                        result2=int(cursor.fetchone()[0])
                        formatted_result2 = format_amount_inr(result2)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>All payment Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result2}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                    with col2_b:
                        result3 = round(result2/result1)
                        formatted_result3 = '₹{:,}'.format(result3)
                        styled_text = "<p style='font-size: 20px; font-weight: bold;'>Avg. Trans. Value</p>"
                        styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result3}</p>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                        
                    queries = [
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Merchant payments' and state='{selected_state}'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Peer-to-peer payments' and state='{selected_state}'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Recharge & bill payments' and state='{selected_state}'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Financial Services' and state='{selected_state}'",
                        f"select sum(amount) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Others' and state='{selected_state}'"
                        ]
                    st.subheader('Categories :')
                    # Execute each query and fetch the results
                    categories = ['Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments', 'Financial Services', 'Others']
                    for query in range(len(queries)):
                        cursor.execute(queries[query])
                        result = int(cursor.fetchone()[0])
                        formatted_result = '{:,}'.format(result)  # Format the result with commas
                        styled_text = f"<span style='font-size: 15px; font-weight: bold;'>{categories[query]}  :          </span> <span style='font-size: 20px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                        st.markdown(styled_text, unsafe_allow_html=True)
            
            with col1:              
                    query1 = f"SELECT district,amount  FROM map_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' order by amount desc"
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    fig = px.bar(df1,
                    title=f"Total_Transaction_Amount  insights of '{selected_state}' district" ,
                    x="district",
                    y="amount",
                    orientation='v',
                    color='amount',
                    color_continuous_scale=px.colors.sequential.Magenta)
                    st.plotly_chart(fig,use_container_width=True)
            with col2:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.subheader(f"Total_Transaction_Amount insights of '{selected_state}' district")
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    st.dataframe(df1)

            
    if selected_option == 'User':
        tab1, tab2 = st.tabs(["Total_Register_User", "Total_App_Open_Count"])
        with tab1:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select the state', state_list)
            col1, col2 = st.columns([2.5, 1])
            with col1:
                query1 = f"SELECT district,registered_user  FROM map_user_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' order by registered_user desc "
                cursor.execute(query1)
                result1 = cursor.fetchall()
                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                fig = px.bar(df1,
                title=f"Total_registered_user  insights of '{selected_state}' district" ,
                x="district",
                y="registered_user",
                orientation='v',
                color='registered_user',
                color_continuous_scale=px.colors.sequential.Magenta)
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                st.subheader(f"Total_registered_user insights of '{selected_state}' district")
                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                st.dataframe(df1)
        with tab2:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('select the state', state_list)
            col1, col2 = st.columns([2.5, 1])
            with col1:
                query1 = f"SELECT district,app_open  FROM map_user_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}' and state='{selected_state}' order by app_open desc "
                cursor.execute(query1)
                result1 = cursor.fetchall()
                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                fig = px.bar(df1,
                title=f"Total_App_Open_Count  insights of '{selected_state}' district" ,
                x="district",
                y="app_open",
                orientation='v',
                color='app_open',
                color_continuous_scale=px.colors.sequential.Magenta)
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                st.subheader(f"Total_App_Open_Count  insights of '{selected_state}' district")
                df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                st.dataframe(df1)
                
if select_page=="Overall Stats":
    with st.sidebar:
        options = ['User', 'Transaction']
        selected_option = st.selectbox('Type', options)
    if selected_option == 'Transaction':
        tab1, tab2 = st.tabs(["Total_Transaction_Count", "Total_Transaction_Amount"])
        with tab1:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('select the state', state_list)
            query1 = f"SELECT year,sum(count) as trasaction_count FROM map_trans_state_wise WHERE  state='{selected_state}' group by year order by trasaction_count desc"
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Transaction_Count  According To year wise '{selected_state}' " ,
            x="year",
            y="trasaction_count",
            orientation='v',
            color='trasaction_count',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
            
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select the state', state_list)
            
            query=f"select distinct(district) from map_user_state_wise where state='{selected_state}'"
            cursor.execute(query)
            result=cursor.fetchall()
            district_list=[]
            for val in result:
                district_list.append(val[0]) 
            selected_district=st.selectbox('Select the district', district_list)
            
            query1 = f"SELECT year,sum(count) as transaction_count  FROM map_trans_state_wise WHERE  state='{selected_state}' and district ='{selected_district}' group by year order by transaction_count desc "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Transaction_Count  According To year wise '{selected_district}' " ,
            x="year",
            y="transaction_count",
            orientation='v',
            color='transaction_count',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
        with tab2:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select The state', state_list)
            query1 = f"SELECT year,sum(amount) as transaction_amount  FROM map_trans_state_wise WHERE  state='{selected_state}' group by year "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Transaction_Amount  According To year wise '{selected_state}' " ,
            x="year",
            y="transaction_amount",
            orientation='v',
            color='transaction_amount',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
            
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('select The State', state_list)
            
            query=f"select distinct(district) from map_user_state_wise where state='{selected_state}'"
            cursor.execute(query)
            result=cursor.fetchall()
            district_list=[]
            for val in result:
                district_list.append(val[0]) 
            selected_district=st.selectbox('select The district', district_list)
            
            query1 = f"SELECT year,sum(Amount) as trasaction_amount  FROM map_trans_state_wise WHERE  state='{selected_state}' and district ='{selected_district}' group by year "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Transaction_Amount  According To year wise '{selected_district}' " ,
            x="year",
            y="trasaction_amount",
            orientation='v',
            color='trasaction_amount',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
    if selected_option == 'User':
        tab3, tab4 = st.tabs(["Total_Register_User", "Total_app_open_Count"])
        with tab3:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('select the state', state_list)
            query1 = f"SELECT year,sum(registered_user) as registered_user  FROM map_user_state_wise WHERE  state='{selected_state}' group by year"
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Register_User  According To year wise '{selected_state}' " ,
            x="year",
            y="registered_user",
            orientation='v',
            color='registered_user',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
           
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select the State', state_list)
            
            query=f"select distinct(district) from map_user_state_wise where state='{selected_state}'"
            cursor.execute(query)
            result=cursor.fetchall()
            district_list=[]
            for val in result:
                district_list.append(val[0]) 
            selected_district=st.selectbox('select the district', district_list)
            
            query1 = f"SELECT year,sum(registered_user) as registered_user  FROM map_user_state_wise WHERE  state='{selected_state}' and district ='{selected_district}' group by year "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_Register_User  According To year wise '{selected_district}' " ,
            x="year",
            y="registered_user",
            orientation='v',
            color='registered_user',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
        with tab4:
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('Select the state', state_list)
            query1 = f"SELECT year,sum(app_open) as app_open FROM map_user_state_wise WHERE  state='{selected_state}' group by year "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_App_Open_Count  According To year wise '{selected_state}' " ,
            x="year",
            y="app_open",
            orientation='v',
            color='app_open',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
                       
            query="select distinct(state) from map_user_state_wise"
            cursor.execute(query)
            result=cursor.fetchall()
            state_list=[]
            for val in result:
                state_list.append(val[0]) 
            selected_state=st.selectbox('select the State', state_list)
            
            query=f"select distinct(district) from map_user_state_wise where state='{selected_state}'"
            cursor.execute(query)
            result=cursor.fetchall()
            district_list=[]
            for val in result:
                district_list.append(val[0]) 
            selected_district=st.selectbox('select the District', district_list)
            
            query1 = f"SELECT year,sum(app_open) as app_open  FROM map_user_state_wise WHERE  state='{selected_state}' and district ='{selected_district}' group by year "
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
            fig = px.bar(df1,
            title=f"Total_App_Open_Count  According To year wise '{selected_district}' " ,
            x="year",
            y="app_open",
            orientation='v',
            color='app_open',
            color_continuous_scale=px.colors.sequential.Magenta)
            st.plotly_chart(fig,use_container_width=True)
        
    



