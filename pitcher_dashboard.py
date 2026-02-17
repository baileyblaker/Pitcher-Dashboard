import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="Pitcher Analytics Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional dark theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 48px !important;
        margin-bottom: 8px !important;
        letter-spacing: -1px !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 32px !important;
        margin-top: 40px !important;
        margin-bottom: 24px !important;
        letter-spacing: -0.5px !important;
    }
    
    h3 {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
        font-size: 22px !important;
        margin-top: 20px !important;
        margin-bottom: 16px !important;
    }
    
    h4 {
        color: #c0c0c0 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
    }
    
    /* Subtitle */
    .subtitle {
        color: #888;
        font-size: 18px;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    /* Text */
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: linear-gradient(135deg, #1a1d24 0%, #1f2229 100%);
        padding: 20px 24px;
        border-radius: 16px;
        margin-bottom: 40px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #888;
        border-radius: 10px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 15px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.05);
        color: #aaa;
        border-color: #444;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff3333 100%);
        color: #ffffff !important;
        border-color: #ff4b4b;
        box-shadow: 0 4px 16px rgba(255, 75, 75, 0.3);
    }
    
    /* Filter section */
    .filter-container {
        background: linear-gradient(135deg, #1a1d24 0%, #242830 100%);
        padding: 28px;
        border-radius: 16px;
        margin-bottom: 36px;
        border: 1px solid #333;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Selectbox and input */
    .stSelectbox > div > div {
        background-color: #1e2127;
        border: 2px solid #333;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #555;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #ff4b4b;
        box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    /* Slider */
    .stSlider {
        padding: 10px 0;
    }
    
    .stSlider label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    .stRadio > div {
        background-color: #1a1d24;
        padding: 14px;
        border-radius: 10px;
        border: 2px solid #333;
    }
    
    .stRadio [role="radiogroup"] {
        gap: 12px;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: #1a1d24;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff3333 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #ff3333 0%, #ff1a1a 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }
    
    /* Divider */
    hr {
        border-color: #333;
        margin: 40px 0;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Warning/info boxes */
    .stAlert {
        background-color: #262730;
        border-left: 4px solid #ff4b4b;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Plotly theme configuration
plotly_template = {
    'layout': {
        'paper_bgcolor': '#1a1d24',
        'plot_bgcolor': '#1a1d24',
        'font': {'color': '#e0e0e0', 'family': 'Inter, sans-serif'},
        'xaxis': {
            'gridcolor': '#333',
            'linecolor': '#444',
            'zerolinecolor': '#444'
        },
        'yaxis': {
            'gridcolor': '#333',
            'linecolor': '#444',
            'zerolinecolor': '#444'
        },
        'title': {
            'font': {'size': 18, 'color': '#ffffff'}
        }
    }
}

# Helper function to format numbers without trailing zeros
def format_number(value, decimals=1):
    """Format number to remove trailing zeros"""
    if pd.isna(value):
        return ""
    if decimals == 0:
        return f"{int(value)}"
    formatted = f"{value:.{decimals}f}"
    # Remove trailing zeros and decimal point if not needed
    formatted = formatted.rstrip('0').rstrip('.')
    return formatted

# Helper function to create movement plot
def create_movement_plot(pitch_data, title="Pitch Movement"):
    """Create pitch movement plot showing break patterns"""
    fig = go.Figure()
    
    # Color map for pitch types
    color_map = {
        'Fastball': '#FF6B6B',
        'FourSeamFastBall': '#FF6B6B',
        'TwoSeamFastBall': '#FF8C8C',
        'Sinker': '#FFA07A',
        'Cutter': '#FFD93D',
        'Slider': '#6BCF7F',
        'Curveball': '#4ECDC4',
        'ChangeUp': '#95E1D3',
        'Splitter': '#A8E6CF'
    }
    
    for _, pitch in pitch_data.iterrows():
        color = color_map.get(pitch['TaggedPitchType'], '#CCCCCC')
        
        # Calculate size - much smaller now, max 25 pixels
        size = min(8 + (pitch['Pitch_Count'] / 50), 25)
        
        fig.add_trace(go.Scatter(
            x=[pitch['Avg_HorzBreak']],
            y=[pitch['Avg_InducedVert']],
            mode='markers+text',
            name=pitch['TaggedPitchType'],
            marker=dict(
                size=size,
                color=color,
                line=dict(color='white', width=2)
            ),
            text=pitch['TaggedPitchType'],
            textposition='top center',
            textfont=dict(size=10, color='white'),
            hovertemplate=(
                f"<b>{pitch['TaggedPitchType']}</b><br>" +
                f"Horizontal: {format_number(pitch['Avg_HorzBreak'])}″<br>" +
                f"Vertical: {format_number(pitch['Avg_InducedVert'])}″<br>" +
                f"Count: {int(pitch['Pitch_Count'])}<br>" +
                "<extra></extra>"
            )
        ))
    
    # Add quadrant lines
    fig.add_hline(y=0, line_dash="dash", line_color="#666", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="#666", opacity=0.5)
    
    fig.update_layout(
        title=f"<b>{title}</b>",
        xaxis_title="Horizontal Break (inches)",
        yaxis_title="Induced Vertical Break (inches)",
        template=plotly_template,
        showlegend=False,
        height=500,
        xaxis=dict(range=[-25, 25], zeroline=True),
        yaxis=dict(range=[-25, 25], zeroline=True)
    )
    
    return fig

# Helper function to create strike zone plot
def create_strike_zone_plot(pitch_data, title="Pitch Location"):
    """Create strike zone heat map"""
    
    # Check if we have location data
    if 'PlateLocSide' not in pitch_data.columns or 'PlateLocHeight' not in pitch_data.columns:
        # Return empty plot with message
        fig = go.Figure()
        fig.add_annotation(
            text="Location data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#888")
        )
        fig.update_layout(
            template=plotly_template,
            height=500,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    fig = go.Figure()
    
    # Color map for pitch types
    color_map = {
        'Fastball': '#FF6B6B',
        'FourSeamFastBall': '#FF6B6B',
        'TwoSeamFastBall': '#FF8C8C',
        'Sinker': '#FFA07A',
        'Cutter': '#FFD93D',
        'Slider': '#6BCF7F',
        'Curveball': '#4ECDC4',
        'ChangeUp': '#95E1D3',
        'Splitter': '#A8E6CF'
    }
    
    # Plot each pitch type - NO FLIPPING, use data as-is
    for _, pitch in pitch_data.iterrows():
        if pd.notna(pitch.get('PlateLocSide')) and pd.notna(pitch.get('PlateLocHeight')):
            color = color_map.get(pitch['TaggedPitchType'], '#CCCCCC')
            
            # Much smaller bubbles - max 20 pixels
            size = min(6 + (pitch['Pitch_Count'] / 60), 20)
            
            fig.add_trace(go.Scatter(
                x=[pitch['PlateLocSide']],
                y=[pitch['PlateLocHeight']],
                mode='markers',
                name=pitch['TaggedPitchType'],
                marker=dict(
                    size=size,
                    color=color,
                    opacity=0.7,
                    line=dict(color='white', width=1)
                ),
                hovertemplate=(
                    f"<b>{pitch['TaggedPitchType']}</b><br>" +
                    f"Horizontal: {format_number(pitch['PlateLocSide'], 2)}<br>" +
                    f"Height: {format_number(pitch['PlateLocHeight'], 2)}<br>" +
                    f"Count: {int(pitch['Pitch_Count'])}<br>" +
                    "<extra></extra>"
                )
            ))
    
    # Draw strike zone (approximate MLB strike zone)
    strike_zone_x = [-0.83, 0.83, 0.83, -0.83, -0.83]
    strike_zone_y = [1.5, 1.5, 3.5, 3.5, 1.5]
    
    fig.add_trace(go.Scatter(
        x=strike_zone_x,
        y=strike_zone_y,
        mode='lines',
        line=dict(color='white', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add home plate - ROTATED 180° FOR PITCHER'S VIEW
    # Point of plate facing down/away (toward catcher)
    # Base of plate at top (toward pitcher)
    plate_x = [0.83, -0.83, -0.83, 0, 0.83]
    plate_y = [-0.15, -0.15, 0.0, 0.15, 0.0]
    
    fig.add_trace(go.Scatter(
        x=plate_x,
        y=plate_y,
        fill='toself',
        fillcolor='rgba(255, 255, 255, 0.3)',
        line=dict(color='white', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=f"<b>{title}</b>",
        xaxis_title="Horizontal Location (ft, pitcher's view)",
        yaxis_title="Height (ft)",
        template=plotly_template,
        showlegend=False,
        height=500,
        xaxis=dict(range=[-2.5, 2.5], zeroline=False),
        yaxis=dict(range=[-0.5, 4.5], zeroline=False, scaleanchor="x", scaleratio=1)
    )
    
    return fig

# Title
st.markdown("# ⚾ Pitcher Analytics Dashboard")
st.markdown("<p class='subtitle'>Advanced Stuff+ and Pitching+ Performance Analysis</p>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        pitch_type_df = pd.read_csv('pitcher_pitch_type_summary_2025.csv')
        overall_df = pd.read_csv('pitcher_overall_summary_2025.csv')
        return pitch_type_df, overall_df
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.stop()

pitch_type_df, overall_df = load_data()

# Check if we have the raw data with PlateLocSide and PlateLocHeight
try:
    raw_data = pd.read_csv('pitching_2025.csv')
    has_location_data = 'PlateLocSide' in raw_data.columns and 'PlateLocHeight' in raw_data.columns
except:
    has_location_data = False

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👤 Pitcher Profile", "🎯 Pitch Type Analysis", "📈 Rankings"])

# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.markdown("## League Overview")
    
    # Filters for Overview
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        teams_overview = ['All Teams'] + sorted(overall_df['PitcherTeam'].unique().tolist())
        selected_team_overview = st.selectbox("Team Filter", teams_overview, key="overview_team")
    
    with col2:
        min_pitches_overview = st.slider(
            "Minimum Pitches",
            min_value=0,
            max_value=500,
            value=50,
            step=10,
            key="overview_min_pitches"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    if selected_team_overview != 'All Teams':
        overview_filtered = overall_df[overall_df['PitcherTeam'] == selected_team_overview]
    else:
        overview_filtered = overall_df.copy()
    
    overview_filtered = overview_filtered[overview_filtered['Total_Pitches'] >= min_pitches_overview]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pitchers",
            f"{len(overview_filtered):,}"
        )
    
    with col2:
        avg_pitching_plus = overview_filtered['Overall_PitchingPlus'].mean()
        st.metric(
            "Avg Pitching+",
            format_number(avg_pitching_plus, 1)
        )
    
    with col3:
        avg_stuff_plus = overview_filtered['Overall_StuffPlus'].mean()
        st.metric(
            "Avg Stuff+",
            format_number(avg_stuff_plus, 1)
        )
    
    with col4:
        total_pitches = overview_filtered['Total_Pitches'].sum()
        st.metric(
            "Total Pitches",
            f"{int(total_pitches):,}"
        )
    
    st.markdown("---")
    
    # Distribution plots
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pitching = px.histogram(
            overview_filtered,
            x='Overall_PitchingPlus',
            nbins=30,
            title="<b>Pitching+ Distribution</b>",
            labels={'Overall_PitchingPlus': 'Pitching+'},
            color_discrete_sequence=['#636EFA']
        )
        fig_pitching.add_vline(x=100, line_dash="dash", line_color="#ff4b4b", 
                               annotation_text="League Avg", annotation_position="top")
        fig_pitching.update_layout(template=plotly_template, height=400)
        st.plotly_chart(fig_pitching, use_container_width=True)
    
    with col2:
        fig_stuff = px.histogram(
            overview_filtered,
            x='Overall_StuffPlus',
            nbins=30,
            title="<b>Stuff+ Distribution</b>",
            labels={'Overall_StuffPlus': 'Stuff+'},
            color_discrete_sequence=['#EF553B']
        )
        fig_stuff.add_vline(x=100, line_dash="dash", line_color="#ff4b4b", 
                           annotation_text="League Avg", annotation_position="top")
        fig_stuff.update_layout(template=plotly_template, height=400)
        st.plotly_chart(fig_stuff, use_container_width=True)
    
    # Scatter plot
    st.markdown("## Performance Matrix")
    
    fig_scatter = px.scatter(
        overview_filtered,
        x='Overall_StuffPlus',
        y='Overall_PitchingPlus',
        hover_data=['Pitcher', 'PitcherTeam', 'Total_Pitches'],
        size='Total_Pitches',
        color='Total_Pitches',
        title="<b>Stuff+ vs Pitching+</b>",
        labels={
            'Overall_StuffPlus': 'Stuff+',
            'Overall_PitchingPlus': 'Pitching+',
            'Total_Pitches': 'Pitches'
        },
        color_continuous_scale='Plasma'
    )
    
    fig_scatter.add_hline(y=100, line_dash="dash", line_color="#666", opacity=0.5)
    fig_scatter.add_vline(x=100, line_dash="dash", line_color="#666", opacity=0.5)
    fig_scatter.update_layout(template=plotly_template, height=600)
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Top performers tables
    st.markdown("## Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 10 by Pitching+")
        top_pitching = overview_filtered.nlargest(10, 'Overall_PitchingPlus')[
            ['Pitcher', 'PitcherTeam', 'Overall_PitchingPlus', 'Total_Pitches']
        ].copy()
        
        top_pitching['Overall_PitchingPlus'] = top_pitching['Overall_PitchingPlus'].apply(lambda x: format_number(x, 1))
        top_pitching['Total_Pitches'] = top_pitching['Total_Pitches'].astype(int)
        top_pitching.index = range(1, len(top_pitching) + 1)
        
        st.dataframe(top_pitching, use_container_width=True, height=400)
    
    with col2:
        st.markdown("### 🏆 Top 10 by Stuff+")
        top_stuff = overview_filtered.nlargest(10, 'Overall_StuffPlus')[
            ['Pitcher', 'PitcherTeam', 'Overall_StuffPlus', 'Total_Pitches']
        ].copy()
        
        top_stuff['Overall_StuffPlus'] = top_stuff['Overall_StuffPlus'].apply(lambda x: format_number(x, 1))
        top_stuff['Total_Pitches'] = top_stuff['Total_Pitches'].astype(int)
        top_stuff.index = range(1, len(top_stuff) + 1)
        
        st.dataframe(top_stuff, use_container_width=True, height=400)

# ==================== TAB 2: PITCHER PROFILE ====================
with tab2:
    st.markdown("## Individual Pitcher Analysis")
    
    # Filters for Pitcher Profile
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        teams_profile = ['All Teams'] + sorted(overall_df['PitcherTeam'].unique().tolist())
        selected_team_profile = st.selectbox("Filter by Team", teams_profile, key="profile_team")
    
    # Filter pitcher list by team
    if selected_team_profile != 'All Teams':
        available_pitchers = overall_df[overall_df['PitcherTeam'] == selected_team_profile]['Pitcher'].unique()
    else:
        available_pitchers = overall_df['Pitcher'].unique()
    
    with col2:
        selected_pitcher = st.selectbox(
            "Select Pitcher",
            sorted(available_pitchers.tolist()),
            key="profile_pitcher"
        )
    
    with col3:
        min_pitch_count = st.slider(
            "Min Pitch Count",
            min_value=0,
            max_value=50,
            value=5,
            step=1,
            key="profile_min_count",
            help="Filter out rarely-used or mis-tagged pitches"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if selected_pitcher:
        # Get pitcher data
        pitcher_overall = overall_df[overall_df['Pitcher'] == selected_pitcher].iloc[0]
        pitcher_pitches = pitch_type_df[pitch_type_df['Pitcher'] == selected_pitcher].copy()
        pitcher_pitches_filtered = pitcher_pitches[pitcher_pitches['Pitch_Count'] >= min_pitch_count]
        
        # Get raw pitch data for strike zone if available
        if has_location_data:
            pitcher_raw = raw_data[raw_data['Pitcher'] == selected_pitcher].copy()
        
        # Header metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Team", pitcher_overall['PitcherTeam'])
        
        with col2:
            pitching_val = pitcher_overall['Overall_PitchingPlus']
            pitching_delta = pitching_val - 100
            st.metric("Pitching+", format_number(pitching_val, 1), delta=format_number(pitching_delta, 1))
        
        with col3:
            stuff_val = pitcher_overall['Overall_StuffPlus']
            stuff_delta = stuff_val - 100
            st.metric("Stuff+", format_number(stuff_val, 1), delta=format_number(stuff_delta, 1))
        
        with col4:
            st.metric("Total Pitches", f"{int(pitcher_overall['Total_Pitches'])}")
        
        with col5:
            st.metric("Pitch Arsenal", f"{len(pitcher_pitches_filtered)} types")
        
        st.markdown("---")
        
        if len(pitcher_pitches_filtered) == 0:
            st.warning("⚠️ No pitch types meet the minimum pitch count threshold. Try lowering the filter.")
        else:
            # Pitch Movement and Location
            st.markdown("## Pitch Arsenal Visualization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Movement plot
                movement_fig = create_movement_plot(pitcher_pitches_filtered, "Pitch Movement Profile")
                st.plotly_chart(movement_fig, use_container_width=True)
            
            with col2:
                # Strike zone plot
                if has_location_data:
                    # Aggregate location data by pitch type
                    location_by_pitch = []
                    for _, pitch in pitcher_pitches_filtered.iterrows():
                        pitch_type = pitch['TaggedPitchType']
                        pitch_locs = pitcher_raw[pitcher_raw['TaggedPitchType'] == pitch_type]
                        if len(pitch_locs) > 0:
                            avg_side = pitch_locs['PlateLocSide'].mean()
                            avg_height = pitch_locs['PlateLocHeight'].mean()
                            location_by_pitch.append({
                                'TaggedPitchType': pitch_type,
                                'PlateLocSide': avg_side,
                                'PlateLocHeight': avg_height,
                                'Pitch_Count': len(pitch_locs)
                            })
                    
                    if location_by_pitch:
                        location_df = pd.DataFrame(location_by_pitch)
                        zone_fig = create_strike_zone_plot(location_df, "Average Pitch Location")
                        st.plotly_chart(zone_fig, use_container_width=True)
                    else:
                        st.info("Location data not available for this pitcher")
                else:
                    st.info("Location data not available in dataset")
            
            st.markdown("---")
            
            # Pitch type breakdown
            st.markdown("## Arsenal Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pitch type usage
                fig_usage = px.pie(
                    pitcher_pitches_filtered,
                    values='Pitch_Count',
                    names='TaggedPitchType',
                    title="<b>Usage Distribution</b>",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_usage.update_layout(template=plotly_template, height=400)
                fig_usage.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_usage, use_container_width=True)
            
            with col2:
                # Pitch metrics comparison
                fig_metrics = go.Figure()
                
                fig_metrics.add_trace(go.Bar(
                    x=pitcher_pitches_filtered['TaggedPitchType'],
                    y=pitcher_pitches_filtered['StuffPlus'],
                    name='Stuff+',
                    marker_color='#636EFA',
                    text=pitcher_pitches_filtered['StuffPlus'].apply(lambda x: format_number(x, 1)),
                    textposition='outside'
                ))
                
                fig_metrics.add_trace(go.Bar(
                    x=pitcher_pitches_filtered['TaggedPitchType'],
                    y=pitcher_pitches_filtered['PitchingPlus'],
                    name='Pitching+',
                    marker_color='#EF553B',
                    text=pitcher_pitches_filtered['PitchingPlus'].apply(lambda x: format_number(x, 1)),
                    textposition='outside'
                ))
                
                fig_metrics.add_hline(
                    y=100, 
                    line_dash="dash", 
                    line_color="#ff4b4b", 
                    annotation_text="League Avg",
                    annotation_position="right"
                )
                
                fig_metrics.update_layout(
                    title="<b>Performance Ratings</b>",
                    barmode='group',
                    xaxis_title="Pitch Type",
                    yaxis_title="Rating",
                    template=plotly_template,
                    height=400
                )
                
                st.plotly_chart(fig_metrics, use_container_width=True)
            
            # Detailed pitch type table
            st.markdown("## Detailed Metrics")
            
            display_cols = [
                'TaggedPitchType', 'Pitch_Count', 'StuffPlus', 'PitchingPlus',
                'Avg_Velocity', 'Avg_InducedVert', 'Avg_HorzBreak', 'Avg_SpinRate',
                'Avg_Extension', 'Avg_RelHeight', 'Avg_RelSide'
            ]
            
            pitch_display = pitcher_pitches_filtered[display_cols].copy()
            pitch_display = pitch_display.sort_values('Pitch_Count', ascending=False)
            
            # Format all columns without trailing zeros
            formatted_display = pd.DataFrame()
            formatted_display['Pitch Type'] = pitch_display['TaggedPitchType']
            formatted_display['Count'] = pitch_display['Pitch_Count'].astype(int)
            formatted_display['Stuff+'] = pitch_display['StuffPlus'].apply(lambda x: format_number(x, 1))
            formatted_display['Pitching+'] = pitch_display['PitchingPlus'].apply(lambda x: format_number(x, 1))
            formatted_display['Velo'] = pitch_display['Avg_Velocity'].apply(lambda x: format_number(x, 1))
            formatted_display['IVB'] = pitch_display['Avg_InducedVert'].apply(lambda x: format_number(x, 1))
            formatted_display['HB'] = pitch_display['Avg_HorzBreak'].apply(lambda x: format_number(x, 1))
            formatted_display['Spin'] = pitch_display['Avg_SpinRate'].apply(lambda x: format_number(x, 0))
            formatted_display['Ext'] = pitch_display['Avg_Extension'].apply(lambda x: format_number(x, 1))
            formatted_display['RelH'] = pitch_display['Avg_RelHeight'].apply(lambda x: format_number(x, 1))
            formatted_display['RelS'] = pitch_display['Avg_RelSide'].apply(lambda x: format_number(x, 1))
            
            st.dataframe(
                formatted_display,
                use_container_width=True,
                height=400
            )

# ==================== TAB 3: PITCH TYPE ANALYSIS ====================
with tab3:
    st.markdown("## Pitch Type Analysis")
    
    # Filters for Pitch Type Analysis
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        teams_pitch = ['All Teams'] + sorted(pitch_type_df['PitcherTeam'].unique().tolist())
        selected_team_pitch = st.selectbox("Team Filter", teams_pitch, key="pitch_team")
    
    with col2:
        pitch_types = sorted(pitch_type_df['TaggedPitchType'].unique().tolist())
        selected_pitch_type = st.selectbox("Pitch Type", pitch_types, key="pitch_type")
    
    with col3:
        min_pitches_pitch = st.slider(
            "Minimum Pitches",
            min_value=0,
            max_value=100,
            value=10,
            step=5,
            key="pitch_min_pitches"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    if selected_team_pitch != 'All Teams':
        pitch_filtered = pitch_type_df[pitch_type_df['PitcherTeam'] == selected_team_pitch]
    else:
        pitch_filtered = pitch_type_df.copy()
    
    pitch_data = pitch_filtered[
        (pitch_filtered['TaggedPitchType'] == selected_pitch_type) &
        (pitch_filtered['Pitch_Count'] >= min_pitches_pitch)
    ].copy()
    
    if len(pitch_data) == 0:
        st.warning("⚠️ No pitchers meet the selected criteria. Try adjusting your filters.")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pitchers", f"{len(pitch_data)}")
        
        with col2:
            avg_stuff = pitch_data['StuffPlus'].mean()
            st.metric("Avg Stuff+", format_number(avg_stuff, 1))
        
        with col3:
            avg_pitching = pitch_data['PitchingPlus'].mean()
            st.metric("Avg Pitching+", format_number(avg_pitching, 1))
        
        with col4:
            avg_velo = pitch_data['Avg_Velocity'].mean()
            st.metric("Avg Velocity", f"{format_number(avg_velo, 1)} mph")
        
        st.markdown("---")
        
        # Movement scatter plot for all pitchers
        st.markdown("## Movement Profile Comparison")
        
        fig_movement_scatter = go.Figure()
        
        # Calculate smaller bubble sizes for the scatter plot - max 15 pixels
        sizes = pitch_data['Pitch_Count'].apply(lambda x: min(5 + (x / 80), 15))
        
        # Add scatter for each pitcher
        fig_movement_scatter.add_trace(go.Scatter(
            x=pitch_data['Avg_HorzBreak'],
            y=pitch_data['Avg_InducedVert'],
            mode='markers',
            marker=dict(
                size=sizes,
                color=pitch_data['PitchingPlus'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Pitching+"),
                line=dict(color='white', width=1),
                cmin=80,
                cmax=120
            ),
            text=pitch_data['Pitcher'],
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Horizontal: %{x:.1f}″<br>" +
                "Vertical: %{y:.1f}″<br>" +
                "<extra></extra>"
            )
        ))
        
        # Add quadrant lines
        fig_movement_scatter.add_hline(y=0, line_dash="dash", line_color="#666", opacity=0.5)
        fig_movement_scatter.add_vline(x=0, line_dash="dash", line_color="#666", opacity=0.5)
        
        fig_movement_scatter.update_layout(
            title=f"<b>{selected_pitch_type} Movement Patterns</b>",
            xaxis_title="Horizontal Break (inches)",
            yaxis_title="Induced Vertical Break (inches)",
            template=plotly_template,
            height=600,
            xaxis=dict(range=[-25, 25]),
            yaxis=dict(range=[-25, 25])
        )
        
        st.plotly_chart(fig_movement_scatter, use_container_width=True)
        
        st.markdown("---")
        
        # Top performers
        st.markdown("## Top Performers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Top 10 by Pitching+")
            top_pitching = pitch_data.nlargest(10, 'PitchingPlus')[
                ['Pitcher', 'PitcherTeam', 'PitchingPlus', 'Pitch_Count', 'Avg_Velocity']
            ].copy()
            
            formatted_top_pitching = pd.DataFrame()
            formatted_top_pitching['Pitcher'] = top_pitching['Pitcher']
            formatted_top_pitching['Team'] = top_pitching['PitcherTeam']
            formatted_top_pitching['Pitching+'] = top_pitching['PitchingPlus'].apply(lambda x: format_number(x, 1))
            formatted_top_pitching['Count'] = top_pitching['Pitch_Count'].astype(int)
            formatted_top_pitching['Velo'] = top_pitching['Avg_Velocity'].apply(lambda x: format_number(x, 1))
            formatted_top_pitching.index = range(1, len(formatted_top_pitching) + 1)
            
            st.dataframe(formatted_top_pitching, use_container_width=True, height=400)
        
        with col2:
            st.markdown("### 🏆 Top 10 by Stuff+")
            top_stuff = pitch_data.nlargest(10, 'StuffPlus')[
                ['Pitcher', 'PitcherTeam', 'StuffPlus', 'Pitch_Count', 'Avg_Velocity']
            ].copy()
            
            formatted_top_stuff = pd.DataFrame()
            formatted_top_stuff['Pitcher'] = top_stuff['Pitcher']
            formatted_top_stuff['Team'] = top_stuff['PitcherTeam']
            formatted_top_stuff['Stuff+'] = top_stuff['StuffPlus'].apply(lambda x: format_number(x, 1))
            formatted_top_stuff['Count'] = top_stuff['Pitch_Count'].astype(int)
            formatted_top_stuff['Velo'] = top_stuff['Avg_Velocity'].apply(lambda x: format_number(x, 1))
            formatted_top_stuff.index = range(1, len(formatted_top_stuff) + 1)
            
            st.dataframe(formatted_top_stuff, use_container_width=True, height=400)
        
        st.markdown("---")
        
        # Velocity correlation plots
        st.markdown("## Performance vs Velocity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vel_pitch = px.scatter(
                pitch_data,
                x='Avg_Velocity',
                y='PitchingPlus',
                hover_data=['Pitcher', 'PitcherTeam', 'Pitch_Count'],
                size='Pitch_Count',
                color='PitchingPlus',
                title=f"<b>{selected_pitch_type}: Velocity vs Pitching+</b>",
                labels={'Avg_Velocity': 'Velocity (mph)', 'PitchingPlus': 'Pitching+'},
                color_continuous_scale='RdYlGn'
            )
            fig_vel_pitch.add_hline(y=100, line_dash="dash", line_color="#ff4b4b")
            fig_vel_pitch.update_layout(template=plotly_template, height=500)
            st.plotly_chart(fig_vel_pitch, use_container_width=True)
        
        with col2:
            fig_vel_stuff = px.scatter(
                pitch_data,
                x='Avg_Velocity',
                y='StuffPlus',
                hover_data=['Pitcher', 'PitcherTeam', 'Pitch_Count'],
                size='Pitch_Count',
                color='StuffPlus',
                title=f"<b>{selected_pitch_type}: Velocity vs Stuff+</b>",
                labels={'Avg_Velocity': 'Velocity (mph)', 'StuffPlus': 'Stuff+'},
                color_continuous_scale='RdYlGn'
            )
            fig_vel_stuff.add_hline(y=100, line_dash="dash", line_color="#ff4b4b")
            fig_vel_stuff.update_layout(template=plotly_template, height=500)
            st.plotly_chart(fig_vel_stuff, use_container_width=True)

# ==================== TAB 4: RANKINGS ====================
with tab4:
    st.markdown("## Pitcher Rankings")
    
    # Filters for Rankings
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ranking_type = st.radio(
            "Ranking Type",
            ["Overall Performance", "By Pitch Type"],
            key="ranking_type"
        )
    
    with col2:
        teams_rank = ['All Teams'] + sorted(overall_df['PitcherTeam'].unique().tolist())
        selected_team_rank = st.selectbox("Team Filter", teams_rank, key="rank_team")
    
    with col3:
        metric_rank = st.radio(
            "Sort By",
            ["Pitching+", "Stuff+"],
            key="rank_metric"
        )
    
    with col4:
        min_pitches_rank = st.slider(
            "Minimum Pitches",
            min_value=0,
            max_value=200,
            value=50,
            step=10,
            key="rank_min_pitches"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if ranking_type == "Overall Performance":
        # Apply filters
        if selected_team_rank != 'All Teams':
            rank_filtered = overall_df[overall_df['PitcherTeam'] == selected_team_rank]
        else:
            rank_filtered = overall_df.copy()
        
        rank_filtered = rank_filtered[rank_filtered['Total_Pitches'] >= min_pitches_rank]
        
        # Sort
        sort_col = 'Overall_PitchingPlus' if metric_rank == 'Pitching+' else 'Overall_StuffPlus'
        ranked_df = rank_filtered.sort_values(sort_col, ascending=False).reset_index(drop=True)
        
        # Format display
        formatted_ranked = pd.DataFrame()
        formatted_ranked['Rank'] = range(1, len(ranked_df) + 1)
        formatted_ranked['Pitcher'] = ranked_df['Pitcher']
        formatted_ranked['Team'] = ranked_df['PitcherTeam']
        formatted_ranked['Pitching+'] = ranked_df['Overall_PitchingPlus'].apply(lambda x: format_number(x, 1))
        formatted_ranked['Stuff+'] = ranked_df['Overall_StuffPlus'].apply(lambda x: format_number(x, 1))
        formatted_ranked['Pitches'] = ranked_df['Total_Pitches'].astype(int)
        formatted_ranked['Arsenal'] = ranked_df['Num_Pitch_Types'].astype(int)
        formatted_ranked['Velo'] = ranked_df['Avg_Velocity'].apply(lambda x: format_number(x, 1))
        
        st.dataframe(
            formatted_ranked,
            use_container_width=True,
            height=700
        )
        
        # Download button
        csv = ranked_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Rankings as CSV",
            data=csv,
            file_name=f"overall_rankings_{metric_rank.lower().replace('+', 'plus')}.csv",
            mime="text/csv"
        )
    
    else:
        # By pitch type
        pitch_type_rank = st.selectbox(
            "Select Pitch Type",
            sorted(pitch_type_df['TaggedPitchType'].unique()),
            key="rank_pitch_type"
        )
        
        # Apply filters
        if selected_team_rank != 'All Teams':
            rank_filtered = pitch_type_df[pitch_type_df['PitcherTeam'] == selected_team_rank]
        else:
            rank_filtered = pitch_type_df.copy()
        
        pitch_ranked = rank_filtered[
            (rank_filtered['TaggedPitchType'] == pitch_type_rank) &
            (rank_filtered['Pitch_Count'] >= min_pitches_rank)
        ].copy()
        
        # Sort
        sort_col = 'PitchingPlus' if metric_rank == 'Pitching+' else 'StuffPlus'
        pitch_ranked = pitch_ranked.sort_values(sort_col, ascending=False).reset_index(drop=True)
        
        # Format display
        formatted_pitch_ranked = pd.DataFrame()
        formatted_pitch_ranked['Rank'] = range(1, len(pitch_ranked) + 1)
        formatted_pitch_ranked['Pitcher'] = pitch_ranked['Pitcher']
        formatted_pitch_ranked['Team'] = pitch_ranked['PitcherTeam']
        formatted_pitch_ranked['Pitching+'] = pitch_ranked['PitchingPlus'].apply(lambda x: format_number(x, 1))
        formatted_pitch_ranked['Stuff+'] = pitch_ranked['StuffPlus'].apply(lambda x: format_number(x, 1))
        formatted_pitch_ranked['Count'] = pitch_ranked['Pitch_Count'].astype(int)
        formatted_pitch_ranked['Velo'] = pitch_ranked['Avg_Velocity'].apply(lambda x: format_number(x, 1))
        formatted_pitch_ranked['IVB'] = pitch_ranked['Avg_InducedVert'].apply(lambda x: format_number(x, 1))
        formatted_pitch_ranked['HB'] = pitch_ranked['Avg_HorzBreak'].apply(lambda x: format_number(x, 1))
        formatted_pitch_ranked['Spin'] = pitch_ranked['Avg_SpinRate'].apply(lambda x: format_number(x, 0))
        
        st.dataframe(
            formatted_pitch_ranked,
            use_container_width=True,
            height=700
        )
        
        # Download button
        csv = pitch_ranked.to_csv(index=False)
        st.download_button(
            label="📥 Download Rankings as CSV",
            data=csv,
            file_name=f"{pitch_type_rank}_rankings_{metric_rank.lower().replace('+', 'plus')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px 0;'>
        <p style='font-size: 14px; font-weight: 600;'>Pitcher Analytics Dashboard</p>
        <p style='font-size: 12px; margin-top: 5px;'>Advanced Stuff+ and Pitching+ Performance Models</p>
    </div>
    """, unsafe_allow_html=True)