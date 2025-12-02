"""
Helper functions for populating UI fields from loaded data
"""

def get_column_items(app):
    """Get list of column names from loaded data for dropdown menu"""
    if app.loaded_data is None:
        return []
    return [{"text": col, "viewclass": "OneLineListItem", 
             "on_release": lambda x=col: None} for col in app.loaded_data.columns]


def populate_field_from_column(app, field_id, column_name):
    """Populate a text field with data from a specific column"""
    if app.loaded_data is None:
        app.show_dialog("Error", "No data loaded. Please load data first.")
        return
    
    if column_name not in app.loaded_data.columns:
        app.show_dialog("Error", f"Column '{column_name}' not found.")
        return
    
    # Get the data from the column
    column_data = app.loaded_data[column_name].tolist()
    
    # Convert to comma-separated string
    data_string = ", ".join([str(val) for val in column_data])
    
    # Set the field text
    field_id.text = data_string
