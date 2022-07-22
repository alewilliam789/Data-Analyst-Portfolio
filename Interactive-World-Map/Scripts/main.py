import folium
from get_Country_storage import get_country_storage
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Get dictionary with all country and information
countrydict = get_country_storage()

# Initialize Folium map
worldmap = folium.Map(location=[0, 0], zoom_start=2.0, max_zoom=5)

# Loop through every country
for key in countrydict:
    # Create Plotly subplots for both table and scatter
    # Create grid for subplots
    # Assign titles for each subplot
    fig = make_subplots(rows=2, cols=1,
                        specs=[[{"type": "table"}], [{"type": "scatter"}]],
                        subplot_titles=["Recent Growth Rates", 'Number of Arrivals Per Year']
                        )
    # Add scatter and define position
    fig.add_trace(
        go.Scatter(x=countrydict[key][1],
                   y=countrydict[key][0],
                   ),
        row=2, col=1
    )
    # Add table and define position
    fig.add_trace(
        go.Table(
            header=dict(
                values=['5-Year', '10-Year', 'All-Time'],
                font=dict(size=10)
            ),
            cells=dict(values=[countrydict[key][5], countrydict[key][6], countrydict[key][7]])),
        row=1, col=1)

    # Create main chart title
    fig.update_layout(
        title_text=f'{key}'
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
