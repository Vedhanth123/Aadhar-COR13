@echo off
echo Aadhar Dashboard with Custom Recommendations

REM Define the base directory for the project
set BASE_DIR="e:\Ver6-COR-13-Aadhar"

REM Ensure the script is run from the correct directory
cd /d %BASE_DIR%

echo Activating virtual environment...
call .\env\Scripts\activate

:menu
echo Select an option:
echo 1. Start Full Analysis Dashboard with Custom Recommendations
echo 2. Start Simple Analysis Dashboard with Custom Recommendations
echo 3. Create Sample Zone Data (if needed)
echo 4. Exit
set /p choice="Enter your choice (1-4): "

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
    echo Creating Sample Zone Data...
    cd /d "e:\Ver6-COR-13-Aadhar"
    python create_zone_sample.py
    goto menu
) else if "%choice%"=="4" (
    echo Exiting...
    goto :eof
) else (
    echo Invalid choice. Please try again.
    goto menu
)

:eof
