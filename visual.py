import plotly.express as px
import plotly.colors as pc

#
def bar(df, x, y, title , n=10 , hover=None, hover2=None ):
   
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text=y ,
        hover_data={hover: True , hover2: True}
                     )   
        
  
    colors = pc.sample_colorscale(
        "Blues",  [i/(n) for i in range((n))]  )[::-1]

    fig.update_traces(
        marker=dict(color=colors),
        textposition="outside",  
        textfont=dict(size=12, color="black")  ,
        
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig

#######
def treemap (df , path , values, color, color_continuous_scale , title): 
   
    fig = px.treemap(
    df,
    path=path,
    values= values,
    color=color,
    color_continuous_scale = color_continuous_scale, 
    title= title,


)
    fig.update_layout(template="plotly_white")
    
    return fig


########

def line(df, x, y, title ,text, n=10 , markers=True):
   
    fig = px.line(
        df,
        x=x,
        y=y,
        
        title=title,
        text=text
        )
  
   
    fig =fig.update_traces(line=dict(width=3, color="royalblue"),
                  texttemplate="%{text:.1f}",
                  textfont=dict(size=12, color="black")  
    )
    
    fig= fig.update_layout(template="plotly_white")
    
    return fig

##########


def pie(df, names, values, title , text ,  n=10 , hover=None, hover2=None  ):

    fig = px.pie(
    df,
    names= names,
    values= values,
    title= title,  
    #text= names,
    hover_data={hover: True , hover2: True} )
    
    colors = pc.sample_colorscale(
        "Blues",  [i/(n) for i in range((n))]  )[::-1]
    
    fig.update_traces(
        marker=dict(colors=colors),
        textinfo="label+percent",  
        textposition="inside"      
    )
 
    return fig


