from src.handlers.add_city import router as add_city_router
from src.handlers.help import router as help_router
from src.handlers.input_cities import router as weather_router
from src.handlers.process_weather import router as process_router
from src.handlers.remove_city import router as remove_router
from src.handlers.start import router as start_router

routers = [
    add_city_router,
    start_router,
    help_router,
    weather_router,
    remove_router,
    process_router,
]
