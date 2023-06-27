import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

conn=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="Kavidhina@5566",
                      port=5432,
                      database="phonepe_pulse")
cursor=conn.cursor()

st.header("PhonePe Pulse")

with st.sidebar:
    st.header("Sidebar")
    options = ['User', 'Transaction']
    selected_option = st.selectbox('Type', options)
    year = [2018, 2019, 2020, 2021, 2022]
    selected_year = st.selectbox('Select the year', year)

    quarter = ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (July-Sep)', 'Q4 (Oct-Dec)']
    selected_quarter = st.selectbox('Select the quarter', quarter)

def format_amount_inr(amount):
    crore_amount = amount / 10000000  # Divide by 10,000,000 to convert to Crore
    rounded_crore_amount = round(crore_amount)  # Round off the Crore amount
    formatted_amount = '₹{:,.0f} Cr'.format(rounded_crore_amount)
    return formatted_amount



  
col1,col2=st.columns([2.5,1])

with col2:
        if selected_option == 'Transaction' :
            if selected_year and selected_quarter:
                    
                tab1,tab2 = st.tabs(["Total_Amoun","Total_Transaction"])


   
                with col1:
                    
                    #1 Transaction user According To year and Quarter
                    
                    query1 = f"SELECT * FROM aggre_trans_state_wise WHERE quarter = '{selected_quarter[:2]}' AND year = '{selected_year}'"
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    
                    # Create the initial figure with count as the default value
                    fig = go.Figure(data=[go.Bar(x=df1["state"], y=df1["count"], name="Count")])
                    fig.update_layout(title='Transaction count & amount According To year and Quarter')
                    
                    # Create the dropdown buttons
                    buttons = [
                        dict(label="Count", method="update", args=[{"y": [df1["count"]], "name": ["Count"]}]),
                        dict(label="Amount", method="update", args=[{"y": [df1["amount"]], "name": ["Amount"]}])
                    ]
                    
                    # Add the dropdown menu to the figure layout
                    fig.update_layout(
                        updatemenus=[
                            dict(
                                active=0,
                                buttons=buttons,
                                x=0.8,
                                y=1.5,
                                xanchor="left",
                                yanchor="top",
                                direction="down",
                                showactive=True,
                                bordercolor="gray",
                                font=dict(color="pink"),
                            ),
                        ]
                    )
                    
                    # Update the color of the bars to Magenta color scale
                    fig.update_traces(marker=dict(color=df1["count"], coloraxis="coloraxis"))
                    
                    # Set the color scale to Magenta
                    fig.update_layout(coloraxis=dict(colorscale="Magenta"))
                    
                    # Display the plotly chart
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #2 Transaction Count According To year and Quarter                  
                    query1 = f"SELECT * FROM aggre_trans_year_wise WHERE quarter='{selected_quarter[:2]}' AND year='{selected_year}'"
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                                      
                    # Create the initial figure with count as the default value
                    fig = go.Figure(data=[go.Bar(x=df1["categories"], y=df1["count"], name="Count")])
                    fig.update_layout(title='Transaction count & amount According To year and Quarter')
                    # Create the dropdown buttons
                    buttons = [
                        dict(label="Count", method="update", args=[{"y": [df1["count"]], "name": ["Count"]}]),
                        dict(label="Amount", method="update", args=[{"y": [df1["amount"]], "name": ["Amount"]}])
                    ]
                    
                    # Add the dropdown menu to the figure layout
                    fig.update_layout(
                        updatemenus=[
                            dict(
                                active=0,
                                buttons=buttons,
                                x=0.8,
                                y=1.2,
                                xanchor="left",
                                yanchor="top",
                                direction="down",
                                showactive=True,
                                bordercolor="gray",
                                font=dict(color="pink")
                            ),
                        ]
                    )
                    
                    # Update the color of the bars to the selected variable
                    fig.update_traces(marker=dict(color=df1["count"], coloraxis="coloraxis"))
                    
                    # Set the color scale to Magenta
                    fig.update_layout(coloraxis=dict(colorscale="Magenta"))
                    
                    # Display the plotly chart
                    st.plotly_chart(fig, use_container_width=True)

                
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
                    styled_text = "<p style='font-size: 20px; font-weight: bold;'>Avg. Transaction Value</p>"
                    styled_text += f"<p style='font-size: 25px;font-weight: bold;color: purple;'>{formatted_result3}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                    
            queries = [
                f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Merchant payments'",
                f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Peer-to-peer payments'",
                f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Recharge & bill payments'",
                f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Financial Services'",
                f"select sum(count) from aggre_trans_state_wise where quarter='{selected_quarter[0:2]}' and year='{selected_year}' and categories='Others'"
                ]
            st.subheader('Categories :')
            # Execute each query and fetch the results
            categories = ['Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments', 'Financial Services', 'Others']
            for query in range(len(queries)):
                cursor.execute(queries[query])
                result = int(cursor.fetchone()[0])
                formatted_result = '{:,}'.format(result)  # Format the result with commas
                styled_text = f"<span style='font-size: 20px; font-weight: bold;'>{categories[query]}  :          </span> <span style='font-size: 25px; font-weight: bold; color: purple;'>{formatted_result}</span>"
                st.markdown(styled_text, unsafe_allow_html=True)
        elif selected_option == 'User' :
            if selected_year and selected_quarter:
                with col1:
                    query1=f"select distinct(registered_user),state,app_open from aggre_user_state_wise where quarter='{selected_quarter[:2]}' and year='{selected_year}'"
                    cursor.execute(query1)
                    result1=cursor.fetchall()
                    df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                    
                    # Create the dropdown options
                    dropdown_options = [
                        {'label': 'Registered User', 'value': 'registered_user'},
                        {'label': 'App Open', 'value': 'app_open'}
                    ]
                    
                    # Create the figure
                    fig = go.Figure()
                    
                    # Add the bar trace for registered_user
                    fig.add_trace(
                        go.Bar(
                            x=df1['state'],
                            y=df1['registered_user'],
                            name='Registered User',
                            marker_color="pink",
                            hovertemplate='Registered User: %{y}<extra></extra>'
                        )
                    )
                    
                    # Add the bar trace for app_open
                    fig.add_trace(
                        go.Bar(
                            x=df1['state'],
                            y=df1['app_open'],
                            name='App Open',
                            hovertemplate='App Open: %{y}<extra></extra>'
                        )
                    )
                    
                    # Configure the layout
                    fig.update_layout(
                        title='Transaction Users by State',
                        xaxis_title='State',
                        yaxis_title='Count',
                        barmode='group',
                        updatemenus=[
                            {
                                'buttons': [
                                    {
                                        'method': 'restyle',
                                        'args': [{'visible': [True, False]}, {'title': 'Registered User'}],
                                        'label': 'Registered User'
                                    },
                                    {
                                        'method': 'restyle',
                                        'args': [{'visible': [False, True]}, {'title': 'App Open'}],
                                        'label': 'App Open'
                                    }
                                ],
                                'direction': 'down',
                                'showactive': True,
                                 'x':0.8,
                                 'y':1.5,
                                 'xanchor':"left",
                                 'yanchor':"top"
                                                             }
                        ]
                    )
                    # Update the color of the bars to the selected variable
                    fig.update_traces(marker=dict(color=df1["registered_user"], coloraxis="coloraxis"))
                    
                    # Set the color scale to Magenta
                    fig.update_layout(coloraxis=dict(colorscale="Magenta"))
                    # Show the Plotly chart
                    st.plotly_chart(fig, use_container_width=True)

                st.subheader('Users :')
                queries=[f"select sum(distinct(registered_user)) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"
                         ,f"select sum(app_open) from aggre_user_year_wise where quarter= '{selected_quarter[0:2]}' and year='{selected_year}'"]
                list=["Registered PhonePe users till","PhonePe app opens in"]
                for query in range(len(queries)):
                    cursor.execute(queries[query])
                    result1=int(cursor.fetchone()[0])
                    formatted_amount1 = '{:,}'.format(result1)
                    if formatted_amount1 == '0' :
                        formatted_amount1 = 'Unavailable'
                    styled_text = f"<p style='font-size: 20px; font-weight: bold;'>{list[query]} {selected_quarter[0:2]} {selected_year} </p>"
                    styled_text += f"<p style='font-size: 35px;font-weight: bold;color: purple;'>{formatted_amount1}</p>"
                    st.markdown(styled_text, unsafe_allow_html=True)
                st.subheader("Top 10")
                col3,col4,col5=st.columns([1,1,1])
                
                with col3:
                    b1=st.button("States")
                with col4:
                    b2=st.button("Districts")
                with col5:
                    b3=st.button("Pincode")
                
                if b1:
                    st.subheader('Top 10 states')
                    query=f"SELECT state,state_registered_user FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order BY state_registered_user DESC LIMIT 10"
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
                        y="state_registered_user",
                        orientation='v',
                        color='state_registered_user',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=True)

                if b2:
                    st.subheader('Top 10 Districts')
                    query=f"SELECT district,district_registered_users FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order BY district_registered_users DESC LIMIT 10"
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
                        y="district_registered_users",
                        orientation='v',
                        color='district_registered_users',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=True)
                        
                    
                if b3:
                    st.subheader('Top 10 Pinocdes')
                    query=f"SELECT pincode,pincode_registered_users FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order BY pincode_registered_users DESC LIMIT 10"
                    cursor.execute(query)
                    val=cursor.fetchall()
                    df=pd.DataFrame(val,index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],columns=[des[0] for des in cursor.description])
                    st.dataframe(df)
                    with col1:
                        query=f"SELECT distinct(pincode),pincode_registered_users FROM public.top_user_year_wise where quarter = '{selected_quarter[0:2]}' and year = '{selected_year}' order BY pincode_registered_users DESC LIMIT 10"
                        cursor.execute(query)
                        result1=cursor.fetchall()
                        df1 = pd.DataFrame(result1, columns=[des[0] for des in cursor.description])
                        fig = px.bar(df1,
                        title='Top 10 districts According To year and Quarter' ,
                        x=str("pincode"),
                        y="pincode_registered_users",
                        orientation='h',
                        color='pincode_registered_users',
                        color_continuous_scale=px.colors.sequential.Magenta)
                        fig.update_layout(xaxis={'categoryorder':'total descending'})
                        st.plotly_chart(fig,use_container_width=True)



