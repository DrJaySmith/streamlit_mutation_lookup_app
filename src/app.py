import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def adjust_mutation(mutation_str, protein):
    """Adjust mutation string for RBD if needed."""
    try:
        pos = int(''.join(filter(str.isdigit, mutation_str)))
        if protein == "rbd" and pos > 330:
            orig_aa = mutation_str[0]
            new_aa = mutation_str[-1]
            adjusted_pos = pos - 330
            return f"{orig_aa}{adjusted_pos}{new_aa}"
        return mutation_str
    except ValueError:
        return mutation_str

# Set page config
st.set_page_config(
    page_title="SARS-CoV-2 Mutation Lookup",
    page_icon="🧬",
    layout="wide"
)

# Title and description
st.title("SARS-CoV-2 Mutation Analysis")
st.markdown("""
This app allows you to analyze mutations in different SARS-CoV-2 proteins:
- Mpro (Main Protease)
- PLpro (Papain-Like Protease)
- RBD (Receptor Binding Domain)
            
The data is sourced from GISAID and GenBank, representing mutations sequenced in the population.
""")

# Protein selection
protein_options = ["mpro", "plpro", "rbd"]
protein = st.selectbox("Select Protein", protein_options)

# Mutation input - works for both single and multiple mutations
mutation_input = st.text_input(
    "Enter Mutation(s)",
    "",
    placeholder="Enter a single mutation (e.g., 'P132H') or multiple mutations separated by commas (e.g., 'P132H, K90R')"
)
mutations = [m.strip() for m in mutation_input.split(",")] if mutation_input else []

# Apply mutation adjustment for RBD
if protein == "rbd" and mutations:
    mutations = [adjust_mutation(mut, protein) for mut in mutations]

# Process data when mutations are entered
if mutations:
    # Load date matrix data for both sources
    gisaid_matrix = pd.read_csv(f"data/gisaid/{protein}/gisaid_{protein}_date_matrix.csv", index_col=0).fillna(0)
    genbank_matrix = pd.read_csv(f"data/genbank/{protein}/genbank_{protein}_date_matrix.csv", index_col=0).fillna(0)
    
    # Find strains with all specified mutations (use AND logic for multiple mutations)
    if len(mutations) == 1:
        gisaid_matching_strains = gisaid_matrix.index[gisaid_matrix.index.str.contains(mutations[0])]
        genbank_matching_strains = genbank_matrix.index[genbank_matrix.index.str.contains(mutations[0])]
    else:
        # For multiple mutations, find strains that contain ALL mutations
        gisaid_mask = pd.Series(True, index=gisaid_matrix.index)
        genbank_mask = pd.Series(True, index=genbank_matrix.index)
        
        for mutation in mutations:
            gisaid_mask = gisaid_mask & gisaid_matrix.index.str.contains(mutation)
            genbank_mask = genbank_mask & genbank_matrix.index.str.contains(mutation)
        
        gisaid_matching_strains = gisaid_matrix.index[gisaid_mask]
        genbank_matching_strains = genbank_matrix.index[genbank_mask]
    
    # Get date counts for matching strains
    if len(gisaid_matching_strains) > 0:
        gisaid_mutation_counts = gisaid_matrix.loc[gisaid_matching_strains].sum()
    else:
        gisaid_mutation_counts = pd.Series(0, index=gisaid_matrix.columns)
    
    if len(genbank_matching_strains) > 0:
        genbank_mutation_counts = genbank_matrix.loc[genbank_matching_strains].sum()
    else:
        genbank_mutation_counts = pd.Series(0, index=genbank_matrix.columns)
    
    # Get total counts for each date
    gisaid_total_counts = gisaid_matrix.sum()
    genbank_total_counts = genbank_matrix.sum()

    # Calculate statistics for display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GISAID Dataset")
        if len(gisaid_matching_strains) > 0:
            st.metric("Sequence Count", int(gisaid_mutation_counts.sum()))
            st.metric("Unique Strain Count", len(gisaid_matching_strains))
            st.metric("Prevalence", f"{(gisaid_mutation_counts.sum() / gisaid_total_counts.sum()):.2%}")
        else:
            st.warning("Mutation(s) not found in GISAID dataset")
    
    with col2:
        st.subheader("GenBank Dataset")
        if len(genbank_matching_strains) > 0:
            st.metric("Sequence Count", int(genbank_mutation_counts.sum()))
            st.metric("Unique Strain Count", len(genbank_matching_strains))
            st.metric("Prevalence", f"{(genbank_mutation_counts.sum() / genbank_total_counts.sum()):.2%}")
        else:
            st.warning("Mutation(s) not found in GenBank dataset")
    
    # Plot options
    st.sidebar.header("Plot Options")
    binning = st.sidebar.selectbox("Time Binning", ["Daily", "Weekly", "Monthly"], index=1)  # Default to Weekly
    y_scale = st.sidebar.selectbox("Y-axis Scale", ["Linear", "Log"], index=0)
    count_type = st.sidebar.selectbox("Count Type", ["Absolute", "Relative (%)"], index=1)
    
    # Find common date columns from both datasets
    gisaid_dates = set(gisaid_matrix.columns)
    genbank_dates = set(genbank_matrix.columns)
    common_dates = sorted(gisaid_dates.union(genbank_dates))  # Use union to include all dates
    
    # Convert to datetime
    dates = pd.to_datetime(common_dates)
    
    # Ensure all data is aligned to the same date index
    gisaid_mutation_aligned = gisaid_mutation_counts.reindex(common_dates, fill_value=0)
    gisaid_total_aligned = gisaid_total_counts.reindex(common_dates, fill_value=0)
    genbank_mutation_aligned = genbank_mutation_counts.reindex(common_dates, fill_value=0)
    genbank_total_aligned = genbank_total_counts.reindex(common_dates, fill_value=0)
    
    # Create DataFrame for easier manipulation - now all arrays have the same length
    data_df = pd.DataFrame({
        'date': dates,
        'gisaid_mutation': gisaid_mutation_aligned.values,
        'gisaid_total': gisaid_total_aligned.values,
        'genbank_mutation': genbank_mutation_aligned.values,
        'genbank_total': genbank_total_aligned.values
    })
    
    # Apply binning
    if binning == "Weekly":
        data_df['period'] = data_df['date'].dt.to_period('W-SUN')  # Week ending on Sunday
        period_col = 'period'
    elif binning == "Monthly":
        data_df['period'] = data_df['date'].dt.to_period('M')
        period_col = 'period'
    else:  # Daily
        data_df['period'] = data_df['date'].dt.date
        period_col = 'period'
    
    # Group by period and sum
    grouped_df = data_df.groupby(period_col).agg({
        'gisaid_mutation': 'sum',
        'gisaid_total': 'sum',
        'genbank_mutation': 'sum',
        'genbank_total': 'sum',
        'date': ['min', 'max']  # Get date range for hover text
    }).reset_index()
    
    # Flatten column names
    grouped_df.columns = [
        'period', 'gisaid_mutation', 'gisaid_total', 'genbank_mutation', 
        'genbank_total', 'date_min', 'date_max'
    ]
    
    # Create timeline plot
    fig = go.Figure()
    
    # Prepare x-axis values and hover text
    if binning == "Daily":
        x_values = pd.to_datetime(grouped_df['date_min']).dt.to_pydatetime()
        hover_dates = [d.strftime('%Y-%m-%d') for d in grouped_df['date_min']]
    elif binning == "Weekly":
        x_values = pd.to_datetime(grouped_df['date_min']).dt.to_pydatetime()  # Use start of week for x-axis
        hover_dates = [f"{row['date_min'].strftime('%Y-%m-%d')} to {row['date_max'].strftime('%Y-%m-%d')}" 
                      for _, row in grouped_df.iterrows()]
    else:  # Monthly
        x_values = pd.to_datetime(grouped_df['date_min']).dt.to_pydatetime()  # Use start of month for x-axis
        hover_dates = [d.strftime('%Y-%m') for d in grouped_df['date_min']]
    
    # Add GISAID data
    if len(gisaid_matching_strains) > 0:
        if count_type == "Relative (%)":
            y_values = (grouped_df['gisaid_mutation'] / grouped_df['gisaid_total'] * 100).fillna(0)
            hover_template = "<b>GISAID</b><br>%{customdata}<br>%{y:.2f}%<extra></extra>"
        else:
            y_values = grouped_df['gisaid_mutation']
            hover_template = "<b>GISAID</b><br>%{customdata}<br>%{y}<extra></extra>"
            
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            name='GISAID',
            mode='lines',
            line=dict(color='darkviolet', width=2),
            fill='tozeroy',
            fillcolor='rgba(148,0,211,0.2)',
            connectgaps=False,
            customdata=hover_dates,
            hovertemplate=hover_template
        ))
    
    # Add GenBank data
    if len(genbank_matching_strains) > 0:
        if count_type == "Relative (%)":
            y_values = (grouped_df['genbank_mutation'] / grouped_df['genbank_total'] * 100).fillna(0)
            hover_template = "<b>GenBank</b><br>%{customdata}<br>%{y:.2f}%<extra></extra>"
        else:
            y_values = grouped_df['genbank_mutation']
            hover_template = "<b>GenBank</b><br>%{customdata}<br>%{y}<extra></extra>"
            
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            name='GenBank',
            mode='lines',
            line=dict(color='steelblue', width=2),
            fill='tozeroy',
            fillcolor='rgba(70,130,180,0.2)',
            connectgaps=False,
            customdata=hover_dates,
            hovertemplate=hover_template
        ))

    # Update layout
    mutation_str = ", ".join(mutations)
    y_axis_title = "Prevalence (%)" if count_type == "Relative (%)" else "Number of Sequences"
    
    fig.update_layout(
        title=f"Timeline of {mutation_str} Occurrence ({binning})",
        xaxis_title="Date",
        yaxis_title=y_axis_title,
        yaxis_type='log' if y_scale == "Log" else 'linear',
        showlegend=True,
        plot_bgcolor='white'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True) 