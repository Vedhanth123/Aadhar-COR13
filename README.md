# Aadhar Analysis Dashboard

## Overview
This project provides an interactive dashboard for visualizing Aadhar data across multiple categories. 
This repository contains a scrollable interactive dashboard for Aadhar data visualization across multiple categories:
- Gender
- Education
- Experience
- Age

## Features
- Interactive tabs for each category
- Scrollable interface
- 9 different visualizations per category
- Dynamic charts with tooltips
- Rotated labels for better readability (especially for Education)
- Responsive layout

## Prerequisites
- Python 3.9+ with pip
- Required packages: pandas, matplotlib, seaborn, streamlit

## How to Run

### Option 1: Using the batch file
1. Simply double-click on `run_dashboard.bat`
2. The dashboard will open in your default web browser

### Option 2: Using Command Line
1. Open a command prompt
2. Navigate to the project directory:
```
cd path\to\Ver6-COR-13-Aadhar
```
3. Activate the virtual environment:
```
.\env\Scripts\activate
```
4. Run the dashboard:
```
streamlit run streamlit_dashboard.py
```

## Navigation
- Use the tabs at the top to switch between different categories
- Scroll down to see all visualizations
- Hover over data points to see more details
- Each visualization can be expanded to full screen by clicking the "⋮" menu in the top-right corner of each chart
- Download data or images using the export functionality in each chart's menu

## Advantages Over Static Images
- Interactive data exploration
- Ability to view specific data points
- Responsive layout that works on any screen size
- No image clutter
- Easier to share and distribute
