from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import requests

@tool
def get_weather_forecast(latitude: float, longitude: float):
    """
    Returns 15-day weather forecast useful for agriculture.
    """

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&daily="
        f"temperature_2m_max,"
        f"temperature_2m_min,"
        f"precipitation_sum,"
        f"precipitation_probability_max,"
        f"wind_speed_10m_max"
        f"&forecast_days=20"
    )

    response = requests.get(url)

    return response.json()


def run_weather_agent(latitude: float, longitude: float,selected_model,API_KEY):
    llm = LLM(
    model=selected_model,
    api_key=API_KEY
)

    # Agent
    weather_agent = Agent(
        role="Weather Forecast Analyst",
        goal="Provide accurate weather forecasts for agriculture",
        backstory=(
            "You are an agricultural weather expert who analyzes "
            "weather forecasts and provides useful information to farmers."
        ),
        tools=[get_weather_forecast],
        llm=llm,
        verbose=True
    )

    # Task
    weather_task = Task(
        description=f"""
        Get the 15-day weather forecast for: {latitude},{longitude}.

        Provide:
        - latitude
        - longitude
        - Maximum Temperature
        - Minimum Temperature
        - Rainfall
        - Rain Probability
        - Wind Speed
        """,
        expected_output="A structured 15-day weather forecast report like table format.",
        agent=weather_agent
    )

    # Crew
    crew = Crew(
        agents=[weather_agent],
        tasks=[weather_task],
        verbose=True
    )

    # Run
    result = crew.kickoff()

    return result.raw   