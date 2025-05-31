@echo off
echo Running Aadhar Chart Generator...
cd /d "e:\Ver6-COR-13-Aadhar"

echo Activating virtual environment...
call .\venv\Scripts\activate

echo Generating charts...
python generate_charts.py

echo Charts generated in the 'charts' directory.
explorer "e:\Ver6-COR-13-Aadhar\charts"

pause
