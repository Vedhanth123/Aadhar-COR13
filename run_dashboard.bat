@echo off
echo Aadhar Analysis Dashboard Launcher

REM Define the base directory for the project
set BASE_DIR="e:\Ver6-COR-13-Aadhar"

REM Ensure the script is run from the correct directory
cd /d %BASE_DIR%

echo Activating virtual environment...
call .\venv\Scripts\activate

:menu
echo Select an option:
echo 1. Start Full Analysis Dashboard (streamlit_dashboard.py)
echo 2. Start Simple Analysis Dashboard (streamlit_dashboard_simple.py)
echo 3. Exit
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Aadhar Full Analysis Dashboard...
    cd /d "e:\Ver6-COR-13-Aadhar"
    streamlit run streamlit_dashboard.py
    goto menu
) else if "%choice%"=="2" (
    echo Starting Aadhar Simple Analysis Dashboard...
    cd /d "e:\Ver6-COR-13-Aadhar"
    streamlit run streamlit_dashboard_simple.py
    goto menu
) else if "%choice%"=="3" (
    echo Exiting...
    goto :eof
) else (
    echo Invalid choice. Please try again.
    goto menu
)

:eof
