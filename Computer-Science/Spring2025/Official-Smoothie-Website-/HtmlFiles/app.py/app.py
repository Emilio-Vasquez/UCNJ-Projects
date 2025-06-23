{
  "configurations": [
    {
      "type": "debugpy",
      "request": "launch",
      "name": "Launch Flask App",
      "program": "${OfficialSmoothieWebsite}/app.py/app.py",
      "args": [
        "run",
        "--no-debugger",
        "--no-reload"
      ],
      "env": {
        "FLASK_APP": "${OfficialSmoothieWebsite}/app.py/app.py",
        "FLASK_ENV": "development"
      }
    }
  ]
} 

{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "${OfficialSmoothieWbsite}/app.py/app.py"
      },
      "args": [
        "run"
      ],
      "jinja": True 
    }
  ]
}