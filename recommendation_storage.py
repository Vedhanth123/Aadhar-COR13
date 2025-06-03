import json
import os
import streamlit as st
from datetime import datetime

# File to store recommendations permanently
RECOMMENDATIONS_FILE = 'aadhar_dashboard_recommendations.json'

def load_recommendations():
    """Load saved recommendations from file"""
    try:
        if os.path.exists(RECOMMENDATIONS_FILE):
            with open(RECOMMENDATIONS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.warning(f"Could not load recommendations: {str(e)}")
        return {}

def save_recommendations(recommendations):
    """Save recommendations to file"""
    try:
        with open(RECOMMENDATIONS_FILE, 'w') as f:
            json.dump(recommendations, f)
        return True
    except Exception as e:
        st.error(f"Could not save recommendations: {str(e)}")
        return False

def export_recommendations(name=None):
    """Export recommendations to a timestamped file"""
    try:
        # Get current timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine which recommendations to export
        if name:
            # Export only recommendations for a specific category
            recommendations = {k: v for k, v in st.session_state.items() 
                               if k.startswith(f"{name}_") and k.endswith("_recommendation")}
            filename = f"recommendations_{name}_{timestamp}.json"
        else:
            # Export all recommendations
            recommendations = {k: v for k, v in st.session_state.items() 
                               if k.endswith("_recommendation")}
            filename = f"recommendations_all_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(recommendations, f, indent=4)
        
        return filename
    except Exception as e:
        st.error(f"Error exporting recommendations: {str(e)}")
        return None

def import_recommendations(file_content):
    """Import recommendations from uploaded file content"""
    try:
        recommendations = json.loads(file_content)
        
        # Update session state with imported recommendations
        for k, v in recommendations.items():
            if k.endswith("_recommendation"):
                st.session_state[k] = v
                
        # Also update the persistent storage
        current_recs = load_recommendations()
        current_recs.update(recommendations)
        save_recommendations(current_recs)
        
        return True
    except Exception as e:
        st.error(f"Error importing recommendations: {str(e)}")
        return False

def init_recommendations():
    """Initialize recommendations from storage when app starts"""
    # Load saved recommendations
    saved_recommendations = load_recommendations()
    
    # Update session state with saved values
    for k, v in saved_recommendations.items():
        if k.endswith("_recommendation"):
            st.session_state[k] = v
            
    return saved_recommendations

def save_recommendation(key, value):
    """Save a single recommendation both to session state and persistent storage"""
    # Update session state
    st.session_state[key] = value
    
    # Load current recommendations and update
    recommendations = load_recommendations()
    recommendations[key] = value
    
    # Save back to file
    return save_recommendations(recommendations)
