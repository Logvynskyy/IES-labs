from fastapi import *
from sqlalchemy.ext.asyncio import AsyncSession
from models import ProcessedAgentData, ProcessedAgentDataInDB
from database import engine, processed_agent_data
from websocket import app, send_data_to_subscribers
from typing import List


# FastAPI CRUDL endpoints
@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    # Insert data to database
    created_records = []
    with engine.begin() as connection:
        for item in data:
            query = processed_agent_data.insert().values(
                road_state=item.road_state,
                x=item.agent_data.accelerometer.x,
                y=item.agent_data.accelerometer.y,
                z=item.agent_data.accelerometer.z,
                latitude=item.agent_data.gps.latitude,
                longitude=item.agent_data.gps.longitude,
                timestamp=item.agent_data.timestamp
            )
            result = connection.execute(query)
            last_record_id = result.lastrowid
            created_record = {
                **item.dict(),
                "id": last_record_id
            }
            created_records.append(created_record)
    await send_data_to_subscribers(created_records)
    return created_records


@app.get(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB
)
def read_processed_agent_data(processed_agent_data_id: int):
    with engine.connect() as connection:
        query = processed_agent_data.select().where(processed_agent_data.c.id == processed_agent_data_id)
        result = connection.execute(query)
        record = result.first()
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record

@app.get(
    "/processed_agent_data/",
    response_model=list[ProcessedAgentDataInDB]
)
def list_processed_agent_data():
    # Get list of data
    with engine.connect() as connection:
        query = processed_agent_data.select()
        result = connection.execute(query)
        records = result.fetchall()
        return records


@app.put(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB
)
def update_processed_agent_data(
        processed_agent_data_id: int,
        data: ProcessedAgentData
):
    # Update data
    with engine.begin() as connection:
        query = (
            processed_agent_data
            .update()
            .where(processed_agent_data.c.id == processed_agent_data_id)
            .values(
                road_state=data.road_state,
                x=data.agent_data.accelerometer.x,
                y=data.agent_data.accelerometer.y,
                z=data.agent_data.accelerometer.z,
                latitude=data.agent_data.gps.latitude,
                longitude=data.agent_data.gps.longitude,
                timestamp=data.agent_data.timestamp
            )
            .returning(*processed_agent_data.c)
        )
        result = connection.execute(query)
        updated_record = result.first()
        if updated_record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return updated_record

@app.delete(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=int
)
def delete_processed_agent_data(processed_agent_data_id: int):
    # Delete by id
    with engine.begin() as connection:
        query = processed_agent_data.delete().where(processed_agent_data.c.id == processed_agent_data_id)
        result = connection.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        return processed_agent_data_id


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)