from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    # Perform analysis based on accelerometer data to classify road condition
    if agent_data.accelerometer.z > 16000:  # Example condition, adjust as needed
        road_state = "pothole"
    else:
        road_state = "normal"

    # Create a ProcessedAgentData object with classified road condition
    processed_data = ProcessedAgentData(
        road_state = road_state,
        agent_data = agent_data,
    )

    return processed_data