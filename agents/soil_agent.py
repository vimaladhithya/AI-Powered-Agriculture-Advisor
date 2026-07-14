import requests
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

@tool
def get_soil_data(latitude: float, longitude: float):
    """
    Returns soil properties useful for agriculture.
    """

    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
        f"lat={latitude}"
        f"&lon={longitude}"
        f"&property=phh2o"
        f"&property=soc"
        f"&property=sand"
        f"&property=silt"
        f"&property=clay"
        f"&depth=0-5cm"
        f"&value=mean"
    )

    response = requests.get(url)

    return response.json()

def run_soil_agent(latitude: float, longitude: float,selected_model,API_KEY):
    llm = LLM(
    model=selected_model,
    api_key=API_KEY
)

    soil_agent = Agent(
    role="Soil Analysis Specialist",
    goal="Analyze soil characteristics using SoilGrids data",
    backstory=(
        "You are an expert soil scientist. "
        "You analyze soil pH, organic carbon, sand, silt, and clay content "
        "to assess soil quality and suitability for agriculture."
        
    ),
    tools=[get_soil_data],
    llm=llm,
    verbose=True
    )

    soil_task = Task(
        description=f"""
            "Using latitude {latitude} and longitude {longitude}.
            "retrieve soil information and provide:\n"
                "Soil pH
                "Organic Carbon
                "Sand Percentage
                "Silt Percentage
                "Clay Percentage
                "Soil Type 
            "Soil Fertility Assessment"
        """,
        expected_output=
            "A structured soil report containing pH, organic carbon, "
            "sand, silt, clay percentages, texture type, and fertility analysis."
            "I want in table structure"
            "I want charecteristic and its value",
        agent=soil_agent
    )

    crew = Crew(
    agents=[soil_agent],
    tasks=[soil_task],
    verbose=True
    )

    result=crew.kickoff()
    return result.raw