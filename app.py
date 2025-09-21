import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.colors as pc

from visual import bar ,line, treemap, pie




conn = sqlite3.connect("chinook.db")


st.title("🎵 Chinook Dashboard")
st.subheader("Customer Distribution by Country")

# 1. Top Customers by Spending
query_cutomer_df  = """
Select 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.country,
    ROUND(SUM(i.total) , 1) AS total_spent

FROM customer c
JOIN invoice i ON c.customer_id = i.customer_id
GROUP BY c.customer_id , customer_name, c.country

ORDER BY total_spent DESC
LIMIT 5;

""" 
top_customers = pd.read_sql_query(query_cutomer_df, conn)



# 2. Customers by Country
query_customers_country  = """
Select 
    c.country,  c.city ,c.state,
    COUNT(customer_id) AS customer_count
    
FROM customer c
GROUP BY country 
ORDER BY customer_count DESC;

""" 
# DESC = descinding
customers_country_distribution = pd.read_sql_query(query_customers_country, conn)


# 3. Monthly Sales Trend
query_invoice_df = "SELECT invoice_date,Round(total,1) AS total  FROM invoice"
invoice_df = pd.read_sql_query(query_invoice_df, conn)

invoice_df["invoice_date"]=  pd.to_datetime(invoice_df["invoice_date"])
invoice_df['year_month'] = invoice_df['invoice_date'].dt.to_period('M')

monthly_sales = invoice_df.groupby("year_month")["total"].sum().reset_index()  # to be DF
monthly_sales["year_month"] = monthly_sales["year_month"].astype(str)   # needed to plt

# 4. Top Genres by Revenue:

query_name_revenue = """
Select  Round(SUM(il.unit_price * il.quantity),1) as revenue , 
        g.name ,
      
        t.album_id , t.unit_price , al.title AS album

FROM  invoice_line  il

JOIN  track t  ON il.track_id = t.track_id
JOIN  genre  g ON t.genre_id = g.genre_id
Join  album al ON al.album_id = t.album_id

GROUP BY g.name
ORDER BY revenue DESC

"""
top_genres_revenue = pd.read_sql_query(query_name_revenue, conn)




# 5. Top Tracks by Quantity Sold
query_invoice_line = """
SELECT   SUM(il.quantity) AS total ,
        il.track_id ,
        t.name, al.title AS album
        
FROM invoice_line il

JOIN track t ON il.track_id = t.track_id
Join  album al ON al.album_id = t.album_id

GROUP BY  t.name
ORDER BY total DESC

"""

invoice_line_df = pd.read_sql_query(query_invoice_line, conn)


Top_Tracks_by_Quantity = invoice_line_df.groupby(["name","track_id", "album"])["total"].sum()
Top_Tracks_by_Quantity = Top_Tracks_by_Quantity.sort_values(ascending= False ).head(10).reset_index()


# 6. Top Artists by Number of Tracks: 

query_artist_tracks = """
SELECT ar.name AS artist_name ,
       count(t.name) AS track_count ,
       al.title as album

FROM track t

JOIN album  al ON t.album_id  = al.album_id
JOIN artist ar ON al.artist_id  =  ar.artist_id

GROUP BY ar.name
ORDER BY track_count DESC
"""

artist_tracks = pd.read_sql_query(query_artist_tracks , conn)
Top_artist_tracks = artist_tracks.head(10)


################################################


#################################################

#f1
fig1 = bar(top_customers ,"customer_name" , "total_spent" , "Top Customers by Spending", 12, "country")

#f2
fig2 = treemap(
    customers_country_distribution,
    path=["country",  "city"],  
    values="customer_count",
    color="customer_count",
    color_continuous_scale="Blues",
    title="Customer Distribution by Country, State, City",
)



#f3
fig3 = line(
    monthly_sales, 
    x="year_month", 
    y="total", 
    title="Monthly Sales Trend",
    text= "total",
    n= 12
)

#f4
fig4 = bar(top_genres_revenue,  "name" , "revenue","Top Genres by Revenue" ,30 , "unit_price","album"  )


#f5
fig5 = bar(
    invoice_line_df.head(10),
    x="name",
    y="total",
    title="Top_Tracks_by_Quantity",
    n=15,
    hover="album"  
)

#f6
fig6 = pie( Top_artist_tracks , "artist_name", "track_count" , "Top Artists by Number of Tracks","artist_name", 15, "album" )

#f6

# مثال مبسط لإضافة lat/lon
coords = {
    "USA": {"lat": 37.0902, "lon": -95.7129},
    "Canada": {"lat": 56.1304, "lon": -106.3468},
    "Brazil": {"lat": -14.2350, "lon": -51.9253},
    "France": {"lat": 46.2276, "lon": 2.2137}
}

customers_country_distribution["lat"] = customers_country_distribution["country"].map(lambda x: coords.get(x, {}).get("lat"))
customers_country_distribution["lon"] = customers_country_distribution["country"].map(lambda x: coords.get(x, {}).get("lon"))

fig7 = px.scatter_mapbox(
    customers_country_distribution, 
    lat="lat",
    lon="lon",
    hover_data=["country", "customer_count"], 
    color="customer_count",
    zoom=1,
    width=700,
    height=500
)

fig7.update_layout(mapbox_style="carto-positron")






# plotly_chart
st.set_page_config(layout="wide", page_title="Chinook Dashboard")



figures = [fig1, fig2, fig3, fig4, fig5, fig6, fig7] 

for i in range(0, len(figures), 2):  
    # عمودين لكل صف
    if i + 1 < len(figures):
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(figures[i], use_container_width=True)
        with col2:
            st.plotly_chart(figures[i+1], use_container_width=True)
    else:  # لو الشارت الأخير لوحده
        st.plotly_chart(figures[i], use_container_width=True)



#for fig in figures:
#    st.plotly_chart(fig, use_container_width=True)
