import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files =[
    'networksecurity/__init__.py',
    'networksecurity/components/__init__.py',
    'networksecurity/constant/__init__.py',
    'networksecurity/entity/__init__.py',
    'networksecurity/logging/__init__.py',
    'networksecurity/logging/logger.py',
    'networksecurity/exception/__init__.py',
    'networksecurity/exception/exception.py',
    'networksecurity/pipeline/__init__.py',
    'networksecurity/utils/__init__.py',
    'networksecurity/cloud/__init__.py',
    # 'networksecurity/',
    'noteboks/',
    'Dockerfile',
    'main.py',
    'app.py',
    'setup.py'
]

for filepath in list_of_files:
    file_path = Path(filepath)
    filedir, filename = os.path.split(file_path)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating file directory {filedir} for the file : {filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
            logging.info(f"Creating empty file: {file_path}")
    
    else:
        logging.info(f"{filename} is already existing!!")