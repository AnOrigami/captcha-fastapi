import uvicorn
from fastapi import FastAPI
import Event
import api2

appliction = FastAPI()

appliction.add_event_handler("startup", Event.event_startup(appliction))
appliction.add_event_handler("shutdown", Event.event_shutdown(appliction))
appliction.include_router(api2.captcharouter)
app = appliction

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
