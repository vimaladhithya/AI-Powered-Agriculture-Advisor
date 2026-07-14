from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
import pandas as pd

@tool
def get_crop_context(
    crop_name: str,
    soil_agent_output: str,
    weather_agent_output: str
) -> str:
    """
    Get crop requirements and agent outputs for comparison.
    """

    df = pd.read_csv("./data/crop_requirements.csv")

    crop_row = df[
        df["Crop"].astype(str).str.lower() == crop_name.lower()
    ]

    if crop_row.empty:
        return f"Crop '{crop_name}' not found in database."

    crop_requirements = crop_row.iloc[0].to_dict()

    return f"""
Crop Selected:
{crop_name}

Crop Requirements:
{crop_requirements}

Soil Agent Output:
{soil_agent_output}

Weather Agent Output:
{weather_agent_output}
"""


def run_agriculture_agent(
    crop_name: str,
    soil_agent_output: str,
    weather_agent_output: str,
    selected_model,
    API_KEY
):

    llm = LLM(
    model=selected_model,
    api_key=API_KEY
)
    agriculture_advisor_agent = Agent(
        role="Agricultural Planning Expert",
        goal="""
        Analyze crop requirements, soil conditions,
        and 20-day weather forecasts to determine
        crop suitability and generate a complete
        farming plan.
        """,
        backstory="""
        You are an experienced agricultural scientist
        specializing in crop suitability analysis,
        irrigation planning, weather forecasting,
        sowing recommendations, and harvest scheduling.
        """,
        tools=[get_crop_context],
        llm=llm,
        verbose=True
    )

    agriculture_task = Task(
    description=f"""
    Crop Name:
    {crop_name}


    Soil Agent Output:
    {soil_agent_output}

    Weather Agent Output:
    {weather_agent_output}

    First call the tool:

    get_crop_context(
        crop_name="{crop_name}",
        soil_agent_output={soil_agent_output},
        weather_agent_output={weather_agent_output}
    )

    Then analyze the returned crop requirements.

    IMPORTANT INSTRUCTIONS:

    - Weather Agent Output already contains actual forecast dates.
    - Use those exact dates in all recommendations.
    - NEVER use Day 1, Day 2, Day 3, etc.
    - Always display dates in DD/MM/YYYY format.
    - Analyze every forecast date individually.
    - Base decisions on crop requirements, soil conditions, and weather forecast.

    PLANTING DATE ANALYSIS:

    - Identify the single best planting date from the forecast.
    - Identify 2-3 alternative planting dates.
    - Consider:
        * Rainfall before sowing
        * Rainfall after sowing
        * Soil moisture availability
        * Temperature suitability
        * Wind speed
        * Humidity
        * Soil type and drainage
    - Explain clearly why the recommended date is best.

    IRRIGATION ANALYSIS:

    - Analyze every forecast date.
    - Identify dates requiring irrigation.
    - Identify dates where irrigation is not required.
    - Identify dates where irrigation should be avoided.
    - Mention exact dates.
    - Recommend irrigation intensity:
        * Light
        * Moderate
        * Heavy
    - Recommend best irrigation timing.

    HARVEST ANALYSIS:

    - Use crop duration from crop requirements.
    - Calculate:
        * Expected Harvest Date
        * Harvest Window Start
        * Harvest Window End
    - Show exact calendar dates.
    - Mention weather-related harvest risks.

    WEATHER RISK ANALYSIS:

    Classify forecast dates into:
    - Heavy rainfall dates
    - Moderate rainfall dates
    - Low rainfall dates
    - High wind dates
    - Extreme temperature dates

    Determine:

    1. Crop suitability
    - Suitable / Moderately Suitable / Not Suitable
    - Suitability score (0-100)

    2. Parameter comparison
    - Soil pH
    - Soil type
    - Temperature
    - Rainfall
    - Humidity
    - Wind speed

    3. Weather risk assessment

    4. Planting recommendation

    5. Irrigation plan

    6. Harvest planning

    7. Final farmer recommendations
    - Fertilizer suggestions
    - Irrigation suggestions
    - Weather precautions
    - Risk level

    Base all decisions on:
    - Crop requirements
    - Soil conditions
    - Weather forecast dates and values
    """,

    expected_output="""
    AGRICULTURAL ADVISORY REPORT

    Crop Name

    Suitability Status

    Suitability Score

    PARAMETER COMPARISON

    WEATHER ANALYSIS

    Heavy Rainfall Dates:
    - DD/MM/YYYY

    Moderate Rainfall Dates:
    - DD/MM/YYYY

    Low Rainfall Dates:
    - DD/MM/YYYY

    High Wind Dates:
    - DD/MM/YYYY

    Extreme Temperature Dates:
    - DD/MM/YYYY

    PLANTING RECOMMENDATION

    Best Planting Date:
    DD/MM/YYYY

    Alternative Planting Dates:
    - DD/MM/YYYY
    - DD/MM/YYYY

    Reason:
    Detailed explanation

    IRRIGATION SCHEDULE

    Date | Recommendation | Reason

    Example:
    13/07/2026 | Irrigate (Light) | Low rainfall
    14/07/2026 | Avoid Irrigation | Heavy rainfall expected

    Best Irrigation Time:
    Early Morning / Evening

    Water Saving Recommendations

    HARVEST PLANNING

    Recommended Planting Date:
    DD/MM/YYYY

    Expected Harvest Date:
    DD/MM/YYYY

    Harvest Window:
    DD/MM/YYYY to DD/MM/YYYY

    Weather Risks Near Harvest

    RISK ASSESSMENT

    FINAL FARMER RECOMMENDATIONS
    - Fertilizer Suggestions
    - Irrigation Suggestions
    - Weather Precautions
    - Risk Level
    """,

    agent=agriculture_advisor_agent

)

    crew = Crew(
        agents=[agriculture_advisor_agent],
        tasks=[agriculture_task],
        verbose=True
    )

    result = crew.kickoff()

    try:
        return result.raw
    except:
        return str(result)

