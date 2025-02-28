import streamlit as st
import pandas as pd
import datetime
import json
import os
import numpy as np
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="RoX Semantic Model UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    dcat_df = pd.read_csv("assets/dcat3.csv")
    opcua_df = pd.read_csv("assets/opcua_robotics_object_hierarchy.csv")
    return dcat_df, opcua_df

dcat_df, opcua_df = load_data()

# Helper functions
def get_dcat_properties(class_name):
    """Get all properties for a given DCAT class"""
    return dcat_df[dcat_df['Class'] == class_name]['Property'].tolist()

def get_opcua_object_types():
    """Get all OPC UA object types"""
    return opcua_df['ObjectType'].unique().tolist()

def get_opcua_levels(object_type, level_num):
    """Get all values for a specific level of an object type"""
    level_col = f'level_{level_num}'
    if level_col in opcua_df.columns:
        # Filter for the object type and get unique values for the level
        values = opcua_df[(opcua_df['ObjectType'] == object_type) & 
                          (opcua_df[level_col].notna())][level_col].unique().tolist()
        return values
    return []

def get_next_level_options(object_type, selected_levels):
    """Get options for the next level based on previous selections"""
    next_level = len(selected_levels) + 1
    level_col = f'level_{next_level}'
    
    if level_col not in opcua_df.columns:
        return []
    
    # Build filter conditions
    conditions = (opcua_df['ObjectType'] == object_type)
    for i, val in enumerate(selected_levels, 1):
        if val:  # Only add condition if a value was selected
            conditions &= (opcua_df[f'level_{i}'] == val)
    
    # Get unique values for the next level
    values = opcua_df[conditions & opcua_df[level_col].notna()][level_col].unique().tolist()
    return values

def search_opcua_nodes(search_term):
    """Search for nodes in the OPC UA model"""
    if not search_term:
        return pd.DataFrame()
    
    # Search in full_name column
    search_results = opcua_df[opcua_df['full_name'].str.contains(search_term, case=False, na=False)]
    
    # Also search in individual level columns
    level_cols = [col for col in opcua_df.columns if col.startswith('level_')]
    for col in level_cols:
        level_matches = opcua_df[opcua_df[col].str.contains(search_term, case=False, na=False)]
        search_results = pd.concat([search_results, level_matches]).drop_duplicates()
    
    return search_results

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def save_asset_data(data):
    """Save asset data to a JSON file"""
    # Create directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate filename based on title and timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data['dcat']['title'].replace(' ', '_')}_{timestamp}.json"
    
    # Save to file using the custom encoder
    with open(output_dir / filename, "w") as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)
    
    return filename

# UI Components
st.title("RoX Semantic Model UI")
st.markdown("""
This application helps you describe assets using both DCAT and OPC UA information models.
* **Mandatory fields** use DCAT for general asset description
* **Optional fields** use OPC UA for specific robotics details
""")

# Asset type selection
asset_type = st.selectbox(
    "Select Asset Type",
    ["Software Service", "Model", "Raw Data"],
    help="Choose the type of asset you want to describe"
)

# Create tabs for mandatory and optional fields
tab1, tab2 = st.tabs(["Mandatory DCAT Fields", "Optional OPC UA Fields"])

# Mandatory DCAT fields (tab 1)
with tab1:
    st.header("Mandatory DCAT Fields")
    st.markdown("These fields are required to describe the asset using the DCAT standard.")
    
    # Create form for mandatory fields
    with st.form("dcat_form"):
        # Title
        title = st.text_input(
            "Title (dcterms:title)", 
            help="A name given to the asset"
        )
        
        # Description
        description = st.text_area(
            "Description (dcterms:description)",
            help="A free-text account of the asset"
        )
        
        # Listing date
        listing_date = st.date_input(
            "Listing Date (dcterms:issued)",
            datetime.date.today(),
            help="Date of formal issuance of the asset"
        )
        
        # Update/modification date
        modification_date = st.date_input(
            "Update/Modification Date (dcterms:modified)",
            datetime.date.today(),
            help="Most recent date on which the asset was changed, updated or modified"
        )
        
        # Primary topic
        primary_topic = st.text_input(
            "Primary Topic (foaf:primaryTopic)",
            help="The resource that is the primary topic of the catalog record"
        )
        
        # Conforms to
        conforms_to = st.text_input(
            "Conforms To (dcat:conformsTo)",
            help="An established standard to which the described resource conforms"
        )
        
        # Owner information
        st.subheader("Asset Ownership Information")
        owner_name = st.text_input("Owner Name")
        owner_organization = st.text_input("Owner Organization")
        owner_email = st.text_input("Owner Email")
        
        # Keywords
        keywords = st.text_input(
            "Keywords (comma separated)",
            help="Keywords or tags describing the asset"
        )
        
        # Submit button for mandatory fields
        submit_dcat = st.form_submit_button("Save DCAT Information")
        
        if submit_dcat:
            if not title or not description:
                st.error("Title and Description are required fields.")
            else:
                st.success("DCAT information saved successfully!")
                # We'll handle the actual saving when both sections are complete

# Optional OPC UA fields (tab 2)
with tab2:
    st.header("Optional OPC UA Fields")
    st.markdown("These fields provide specific details about robotics assets using the OPC UA information model.")
    
    # Add expander with OPC UA explanation
    with st.expander("About OPC UA Information Model", expanded=False):
        st.markdown("""
        ### OPC UA Information Model
        
        OPC UA provides a framework for representing complex information as Objects in an AddressSpace. These Objects consist of Nodes connected by References, with different node classes conveying different semantics:
        
        - **Object Nodes**: Represent physical or logical components
        - **Variable Nodes**: Represent values that can be read or written
        - **Method Nodes**: Represent functions that can be called
        
        #### Hierarchical Structure
        
        The OPC UA model is organized hierarchically:
        
        1. **ObjectTypes** (top level): Define templates for objects
        2. **Objects**: Instances of ObjectTypes
        3. **Variables/Methods**: Properties or actions associated with Objects
        
        Every Node has attributes including a unique identifier (NodeId) and a non-localized name (BrowseName).
        
        #### Type System
        
        Object and Variable Nodes always reference a TypeDefinition (ObjectType or VariableType) that describes their semantics and structure. Types act as templates defining all children that can be present in an instance.
        
        OPC UA also supports sub-typing, allowing modelers to extend existing types. This enables:
        - Adding new properties to existing types
        - Specializing general types for specific use cases
        - Maintaining compatibility with clients expecting the parent type
        
        In this application, you can navigate the OPC UA robotics model by selecting an ObjectType and then drilling down through its hierarchical structure.
        """)
    
    # Add search functionality
    st.subheader("Search OPC UA Nodes")
    search_term = st.text_input("Search for objects, variables, or methods", 
                               help="Enter a search term to find specific nodes in the OPC UA model")
    
    if search_term:
        search_results = search_opcua_nodes(search_term)
        if not search_results.empty:
            st.success(f"Found {len(search_results)} matching nodes")
            
            # Display search results in a more readable format
            display_cols = ['ObjectType', 'type', 'id', 'full_name']
            st.dataframe(search_results[display_cols], width=1000)
            
        else:
            st.warning(f"No nodes found matching '{search_term}'")
    
    st.markdown("---")
    
    # Create hierarchical filter for OPC UA fields
    st.subheader("Hierarchical Node Selection")
    
    # Use search result if available
    if 'search_selected_object_type' in st.session_state:
        object_types = get_opcua_object_types()
        default_index = object_types.index(st.session_state.search_selected_object_type) if st.session_state.search_selected_object_type in object_types else 0
        selected_object_type = st.selectbox("Select Object Type", object_types, index=default_index)
        # Clear the search selection after using it
        del st.session_state.search_selected_object_type
    else:
        object_types = get_opcua_object_types()
        selected_object_type = st.selectbox("Select Object Type", object_types)
    
    # Initialize session state for selected levels if not exists
    if 'selected_levels' not in st.session_state:
        st.session_state.selected_levels = []
    
    # Use search result levels if available
    if 'search_selected_levels' in st.session_state and st.session_state.search_selected_levels:
        preset_levels = st.session_state.search_selected_levels
        del st.session_state.search_selected_levels
    else:
        preset_levels = []
    
    # Dynamic level selection based on previous choices
    level_selections = []
    current_level = 1
    continue_levels = True
    
    while continue_levels:
        level_options = get_next_level_options(selected_object_type, level_selections)
        
        if not level_options:
            break
            
        level_label = f"Level {current_level}"
        
        # Use preset value from search if available
        default_value = ""
        if current_level <= len(preset_levels):
            if preset_levels[current_level-1] in level_options:
                default_value = preset_levels[current_level-1]
        
        # Find index of default value
        default_index = 0
        if default_value and default_value in [""] + level_options:
            default_index = ([""] + level_options).index(default_value)
        
        selected_value = st.selectbox(
            level_label, 
            [""] + level_options,
            index=default_index,
            key=f"level_{current_level}"
        )
        
        level_selections.append(selected_value)
        
        # If no value was selected at this level, stop adding more levels
        if not selected_value:
            break
            
        current_level += 1
    
    # Store the selections in session state
    st.session_state.selected_levels = level_selections
    
    # Show the selected path
    if level_selections and any(level_selections):
        selected_path = " > ".join([selected_object_type] + [l for l in level_selections if l])
        st.info(f"Selected path: {selected_path}")
        
        # Allow adding a value for the selected path
        st.subheader("Add Value for Selected Path")
        
        # Determine the type of the selected node
        filter_conditions = (opcua_df['ObjectType'] == selected_object_type)
        for i, val in enumerate(level_selections, 1):
            if val:
                filter_conditions &= (opcua_df[f'level_{i}'] == val)
        
        matching_nodes = opcua_df[filter_conditions]
        
        if not matching_nodes.empty:
            node_type = matching_nodes.iloc[0]['type']
            # Convert NumPy int64 to Python int
            node_id = int(matching_nodes.iloc[0]['id'])
            
            st.write(f"Node Type: {node_type}")
            st.write(f"Node ID: {node_id}")
            
            # Different input based on node type
            if node_type == 'Variable':
                node_value = st.text_input("Variable Value")
            elif node_type == 'Method':
                node_value = st.text_area("Method Parameters")
            elif node_type == 'Object' or node_type == 'ObjectType':
                node_value = st.text_input("Object Identifier")
            else:
                node_value = st.text_input("Value")
                
            # Add button to save the value
            if st.button("Add Value"):
                if not node_value:
                    st.warning("Please enter a value.")
                else:
                    if 'opcua_values' not in st.session_state:
                        st.session_state.opcua_values = {}
                    
                    # Store the value with the full path as key
                    path_key = f"{selected_object_type}.{'.'.join([l for l in level_selections if l])}"
                    st.session_state.opcua_values[path_key] = {
                        "id": node_id,  # Already converted to Python int
                        "type": node_type,
                        "value": node_value
                    }
                    
                    st.success(f"Value added for {path_key}")
    
    # Display all added OPC UA values
    if 'opcua_values' in st.session_state and st.session_state.opcua_values:
        st.subheader("Added OPC UA Values")
        
        # Create a table to display the values
        opcua_values_df = pd.DataFrame([
            {
                "Path": path,
                "ID": details["id"],
                "Type": details["type"],
                "Value": details["value"]
            }
            for path, details in st.session_state.opcua_values.items()
        ])
        
        st.table(opcua_values_df)
        
        # Button to clear all values
        if st.button("Clear All OPC UA Values"):
            st.session_state.opcua_values = {}
            st.rerun()

# Final submission section
st.header("Save Asset Description")
st.markdown("Click the button below to save all the information about this asset.")

if st.button("Save Complete Asset Description"):
    # Check if mandatory fields are filled
    if not 'title' in locals() or not title or not description:
        st.error("Please fill in the mandatory fields (Title and Description) in the first tab.")
    else:
        # Prepare data structure
        asset_data = {
            "asset_type": asset_type,
            "dcat": {
                "title": title,
                "description": description,
                "issued": listing_date.isoformat(),
                "modified": modification_date.isoformat(),
                "primaryTopic": primary_topic,
                "conformsTo": conforms_to,
                "owner": {
                    "name": owner_name,
                    "organization": owner_organization,
                    "email": owner_email
                },
                "keywords": [k.strip() for k in keywords.split(",")] if keywords else []
            },
            "opcua": st.session_state.opcua_values if 'opcua_values' in st.session_state else {}
        }
        
        # Save to file
        try:
            filename = save_asset_data(asset_data)
            st.success(f"Asset description saved successfully to {filename}")
            
            # Display the JSON
            st.subheader("Asset Description JSON")
            st.json(asset_data)
            
            # Option to download the file
            st.download_button(
                label="Download JSON File",
                data=json.dumps(asset_data, indent=2, cls=NumpyEncoder),
                file_name=filename,
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error saving asset description: {str(e)}")

# Add some styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
        border-bottom: 2px solid #4c78a8;
    }
</style>
""", unsafe_allow_html=True)