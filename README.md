 Step:1
 install uv first and setup uv https://docs.astral.sh/uv/getting-started/installation/
    command 1: 
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    command 2:
        pip install uv
    command for Creating virtual environment: uv venv
    Activate with: .venv\Scripts\activate
 Step:2
 Download MongoDB server , and compass
 Step:3
 Crate virtual environment
 Step:4
 Run app command
 uvicorn main:app --reload