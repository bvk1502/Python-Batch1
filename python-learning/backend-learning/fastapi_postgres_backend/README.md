Use below command to run the service
uvicorn app.main:app

Run as Debug
python debug.py

Link to open 
http://127.0.0.1:8000

Docs
http://127.0.0.1:8000/docs

ReDocs
http://127.0.0.1:8000/redoc


Debug via visual studio code settings
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "args": [],
            "justMyCode": false
        },
        {
            "name": "FastAPI with uvicorn",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--log-level", "debug"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "justMyCode": false
        }
    ]
}