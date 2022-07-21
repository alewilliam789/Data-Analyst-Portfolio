import folium
from get_Country_storage import get_country_storage
import plotly.graph_objects as go

# Get dictionary with all country and information
countrydict = get_country_storage()

# Initialize Folium map
worldmap = folium.Map(location=[0, 0], zoom_start=2.0, max_zoom=5)

# Loop through every country
for key in countrydict:
    # Create interactive Plotly html
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=countrydict[key][1],
            y=countrydict[key][0],
            name=key
        )
    )
    fig.update_layout(
     title_text='Number of Arrivals per Year'
     )
    # Add range slider
    fig.update_layout(
     xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=5,
                     label="5Y",
                     step="year",
                     stepmode="backward"),
                dict(count=10,
                     label="10Y",
                     step="year",
                     stepmode="backward"),
                dict(label='All', step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
      )
    )
    # Write these graphs to html file of the country.
    fig.write_html(countrydict[key][4])
    html = """
        <iframe src=\"""" + countrydict[key][4] + """\" width="850" height="400"  frameborder="0">    
        """
    # Pass that html to the Folium popup
    popup = folium.Popup(folium.Html(html, script=True))

    # Create Folium markers and add to interactive map.
    folium.Marker(
        location=[countrydict[key][2], countrydict[key][3]], popup=popup,
        tooltip=key
    ).add_to(worldmap)

# Save the file to view
worldmap.save('worldmap.html')


