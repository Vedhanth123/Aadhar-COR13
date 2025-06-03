# Custom Recommendations Feature

This document explains how to use the new custom recommendations feature in the Aadhar Analysis Dashboard.

## Overview

The dashboard now allows you to write, save, and manage your own custom recommendations and insights for each chart. These recommendations will persist between sessions, so you don't have to rewrite them each time you run the dashboard.

## Features

### 1. Adding Custom Recommendations

Each chart now has a text area labeled "Your Recommendation" where you can enter your custom insights and analysis. Initially, these will be pre-populated with auto-generated insights, but you can modify them as needed.

### 2. Saving Recommendations

After entering your custom recommendation for a chart:

1. Click the "Save Recommendation" button below the text area
2. You'll see a success message confirming that your recommendation has been saved
3. Your recommendation will now be displayed in the "Key Insights" section below the chart

### 3. Exporting Recommendations

You can export all recommendations for a specific category (e.g., Gender, Education, Zone):

1. Click the "Export/Import Recommendations" expander at the top of the dashboard
2. Click "Export All Recommendations"
3. A JSON file will be saved with your recommendations, named with a timestamp

### 4. Importing Recommendations

You can import previously exported recommendations:

1. Click the "Export/Import Recommendations" expander
2. Use the "Import recommendations from JSON" uploader to select a previously exported JSON file
3. Click "Upload" to import those recommendations

## Persistent Storage

All recommendations are automatically saved to a local file called `aadhar_dashboard_recommendations.json` in the project directory. This ensures your recommendations persist between different runs of the dashboard.

## Using the New Batch File

A new batch file `run_dashboard_with_recommendations.bat` is provided that offers the following options:

1. Start Full Analysis Dashboard with Custom Recommendations
2. Start Simple Analysis Dashboard with Custom Recommendations
3. Create Sample Zone Data (if needed)
4. Exit

Simply run this batch file and select the option you want to use.

## Technical Notes for Developers

- Recommendations are stored in Streamlit's session state with keys following the pattern `{category}_{chart_name}_recommendation`
- The `recommendation_storage.py` module handles persistent storage of recommendations
- To extend this functionality to new charts, make sure to use the `save_recommendation()` function

## Troubleshooting

If your recommendations aren't being saved properly:

1. Make sure the `aadhar_dashboard_recommendations.json` file is writable
2. Try exporting your recommendations and reimporting them
3. Check that you're clicking the "Save" button after making changes
