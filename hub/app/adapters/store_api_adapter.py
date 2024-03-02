import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url
   
    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (List[ProcessedAgentData]): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        try:
            # Convert the processed data batch to JSON
            processed_data_json = [data.dict() for data in processed_agent_data_batch]

            # Make a POST request to the Store API endpoint
            response = requests.post(
                f"{self.api_base_url}/processed_agent_data",
                json=processed_data_json
            )

            # Check if the request was successful
            if response.status_code == 200:
                logging.info("Processed data saved successfully.")
                return True
            else:
                logging.error(f"Failed to save processed data. Status code: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"An error occurred while saving processed data: {e}")
            return False