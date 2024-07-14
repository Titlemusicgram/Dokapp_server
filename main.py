from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from funcs import clean_temp_dir, create_temp_folder
from config import dokapp_temp
from router import router as main_router


# Создаем временную папку, если ее нет
create_temp_folder()

# Запускаем сервер
app = FastAPI()

# Создаем папку, где будут храниться фото
app.mount(f'/{dokapp_temp}', StaticFiles(directory=f'{dokapp_temp}'), name=f'{dokapp_temp}')

# Удаляем все временные фото в dokapp_temp при запуске
clean_temp_dir(dokapp_temp)

app.include_router(main_router)
