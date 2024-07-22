from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from funcs import create_temp_folder
from config import dokapp_temp
from router import router as main_router


create_temp_folder()
app = FastAPI()
app.mount(f'/{dokapp_temp}', StaticFiles(directory=f'{dokapp_temp}'), name=f'{dokapp_temp}')
app.include_router(main_router)
