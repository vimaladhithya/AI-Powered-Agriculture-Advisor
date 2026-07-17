import requests
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import streamlit as st

@tool
def get_coordinates_agent(city):
    """
    Get latitude and longitude using Open-Meteo Geocoding API
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)

    data = response.json()


    if "results" not in data:
        return "Location not found"

    global location 
    location=data["results"][0]
    #print(location)
    
    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "population": location["population"],
        "state":location["admin1"]
    }

def run_location_agent(city,selected_model,API_KEY):
    llm = LLM(
    model=selected_model,
    api_key=API_KEY
)

    location_agent = Agent(
        role="Location Agent",
        goal="Find latitude and longitude of a city",
        backstory="You are an expert in finding geographical coordinates.",
        tools=[get_coordinates_agent],
        llm=llm,
        verbose=True
    )
    
    location_task = Task(
    description=f"""
    Find the latitude and longitude of {city} using the available tool.

    Return ONLY the following information.

    Format exactly like this:

    City: <city_name>
    Latitude: <latitude>
    Longitude: <longitude>
    State: <state_name>
    Population: <population>

    Do not return markdown.
    Do not return a table.
    Do not add explanations.
    Do not add headings.
    """,
    expected_output="""
    City: Bengaluru
    Latitude: 12.97194
    Longitude: 77.59369
    State: Karnataka
    Population: 8495492
    """,
    agent=location_agent
)

    crew = Crew(
        agents=[location_agent],
        tasks=[location_task],
        verbose=True
    )

    result = crew.kickoff()

    return result.raw

#def get_coordinates():
 #   latitude=location["latitude"]
  #  longitude=location["longitude"]
   # return latitude,longitude
