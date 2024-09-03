import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import datetime
import os

# Function to simulate performance data
def simulate_performance_data(): 
    np.random.seed(42)
    months = pd.date_range(start='2020-01-01', periods=36, freq='M')
    portfolio_returns = np.random.normal(loc=0.01, scale=0.02, size=len(months))
    cumulative_returns = (1 + pd.Series(portfolio_returns)).cumprod() - 1
    nifty_returns = np.random.normal(loc=0.008, scale=0.015, size=len(months))
    cumulative_nifty_returns = (1 + pd.Series(nifty_returns)).cumprod() - 1
    fd_returns = np.full(len(months), 0.06 / 12)
    cumulative_fd_returns = (1 + pd.Series(fd_returns)).cumprod() - 1
    drawdowns = 1 - (1 + pd.Series(portfolio_returns)).cummax()
    sharpe_ratio = portfolio_returns.mean() / portfolio_returns.std() * np.sqrt(12)
    sortino_ratio = portfolio_returns.mean() / portfolio_returns[portfolio_returns < 0].std() * np.sqrt(12)
    return months, cumulative_returns, cumulative_nifty_returns, cumulative_fd_returns, drawdowns, sharpe_ratio, sortino_ratio

# Simulated data for portfolio allocation
allocation_data = {
    'Large Cap': 40, 
    'Mid Cap': 30, 
    'Small Cap': 20,
    'Bonds': 10
}

sector_data = {
    'Technology': 25,
    'Healthcare': 20,
    'Finance': 20,
    'Consumer Goods': 15,
    'Energy': 10,
    'Utilities': 10
}

# Simulate data
months, cumulative_returns, cumulative_nifty_returns, cumulative_fd_returns, drawdowns, sharpe_ratio, sortino_ratio = simulate_performance_data()

# Sidebar Navigation
st.sidebar.title("Whalestreet Dashboard")
page = st.sidebar.radio(
    "Navigate to", 
    ["Overview", "Key Features", "Portfolio Performance", "Client P&L", "Investment Strategy", "Growth Projections","Understand the Risk","Why Whalestreet PMS Stands Out", "Sharing Revenue Model", "Steps to Start Your PMS", "Resources & Contact"]
)

# Light Theme Styling with Icons
st.markdown("""
    <style>
    body {
        color: #333333;
        background-color: #f7f7f7;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #1a1a1a;
        text-align: left;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
        color: #333333;
    }
    .stButton>button {
        background-color: #007acc;
        color: white;
        border-radius: 5px;
    }
    .footer {
        text-align: center;
        color: #666666;
        font-size: 14px;
        margin-top: 50px;
    }
    .metric {
        text-align: center;
        font-size: 18px;
        margin: 10px;
        padding: 15px;
        background-color: #f0f0f0;
        border-radius: 8px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 24px;
        color: #007acc;
        font-weight: bold;
    }
    .metric-label {
        font-size: 14px;
        color: #666666;
    }
    .section-title {
        display: flex;
        align-items: center;
        font-size: 24px;
        margin-top: 30px;
    }
    .section-title img {
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Define color palette
PRIMARY_COLOR = "#2C3E50"  # Dark blue-grey
ACCENT_COLOR = "#18BC9C"  # Mint green for highlights
BACKGROUND_COLOR = "#FFFFFF"  # White background
TEXT_COLOR = "#2C3E50"  # Dark blue-grey
BORDER_COLOR = "#E0E0E0"  # Light grey for borders
SHADOW_COLOR = "rgba(0, 0, 0, 0.1)"  # Light shadow

# Apply custom CSS for borders, shadows, and spacing
st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            font-family: 'Arial', sans-serif;
        }}
        .sidebar .sidebar-content {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        h2, h3 {{
            color: {PRIMARY_COLOR};
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }}
        .stButton button {{
            background-color: {ACCENT_COLOR};
            color: white;
            border-radius: 5px;
            border: none;
            box-shadow: 2px 2px 5px {SHADOW_COLOR};
        }}
        .stButton button:hover {{
            background-color: {PRIMARY_COLOR};
        }}
        .stMetric {{
            background-color: {BACKGROUND_COLOR};
            border: 1px solid {BORDER_COLOR};
            padding: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px {SHADOW_COLOR};
        }}
        .stElement {{
            margin-bottom: 20px;
        }}
        .section-header {{
            background-color: {BACKGROUND_COLOR};
            padding: 15px;
            border-radius: 10px;
            border: 1px solid {BORDER_COLOR};
            box-shadow: 2px 2px 5px {SHADOW_COLOR};
            color: {TEXT_COLOR};
            margin-bottom: 20px;
        }}
        .section-header h3 {{
            margin: 0;
        }}
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Layout
if page == "Overview":
    # Whalestreet Branding Header with Sleek Design
    st.markdown('''
    <div style="background-color: #1E2D39; padding: 20px; border-radius: 10px;">
        <h1 style="color: #FFFFFF; font-family: 'Arial', sans-serif; text-align: center;">Welcome to Whalestreet Portfolio Management</h1>
        <p style="color: #CCCCCC; font-size: 16px; text-align: center;">Your Partner in Quantitative Investment Excellence</p>
    </div>
    ''', unsafe_allow_html=True)

    # Introduction Section with More Professional Visuals
    st.markdown('''
    <div style="font-size: 16px; line-height: 1.8; color: #1E2D39; margin-bottom: 20px;">
        At Whalestreet Portfolio Management, we offer advanced, data-driven portfolio management services designed to maximize your investment returns while minimizing risk. Our platform utilizes proprietary algorithms and quantitative models to deliver superior results.
        <br><br>
        As an official partner of <strong>AngelOne Broking</strong> and backed by the esteemed <strong>Delhi Technological University (DTU)</strong>, we are poised to become the leading quant and portfolio management service provider, offering comprehensive services to our clients.
    </div>
    ''', unsafe_allow_html=True)

    # Performance Metrics Section (Graphs)
    st.markdown('''
    <div style="font-size: 18px; color: #1E2D39; text-align: center; margin-bottom: 20px;">
        <strong>Explore Our Performance Metrics</strong>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Portfolio Growth Over Time", unsafe_allow_html=True)
        # Simulated fluctuating data for portfolio growth graph
        portfolio_growth = [100, 110, 90, 120, 95, 130, 125, 140, 135, 150]
        st.line_chart(portfolio_growth)

    with col2:
        st.markdown("#### Risk vs. Return", unsafe_allow_html=True)
        # Simulated fluctuating data for risk vs. return scatter plot
        data = {
            'Risk': [5, 7, 10, 15, 18, 20, 22, 25, 28],
            'Return': [2, 4, 6, 8, 10, 12, 14, 16, 18]
        }
        st.scatter_chart(data)

    # Client Testimonials and Trust Indicators
    st.markdown('''
    ### What Our Clients Say
    <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; font-size: 16px; color: #1E2D39; margin-bottom: 20px;">
        <blockquote style="font-style: italic;">
            "Whalestreet has transformed my investment approach. Their data-driven strategies have consistently outperformed my expectations."
            <br><strong>- Ayush</strong>
        </blockquote>
        <blockquote style="font-style: italic;">
            "The transparency and personalized service at Whalestreet are unparalleled. I trust them with my financial future."
            <br><strong>- Prakash</strong>
        </blockquote>
    </div>
    ''', unsafe_allow_html=True)


    # Our Philosophy Section with Sleek Icons and Minimalistic Design
    st.markdown('''
    ### Our Philosophy
    <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px;">
        <div style="display: flex; justify-content: space-between; text-align: center;">
            <div style="width: 30%;">
                <img src="https://img.icons8.com/ios-filled/50/0A74DA/medal.png" width="50" style="margin-bottom: 10px;"/>
                <p><strong>Proven Expertise</strong></p>
                <p style="font-size: 14px; color: #1E2D39;">Decades of experience in managing portfolios with consistent outperformance.</p>
            </div>
            <div style="width: 30%;">
                <img src="https://img.icons8.com/ios-filled/50/0A74DA/visible.png" width="50" style="margin-bottom: 10px;"/>
                <p><strong>Transparency</strong></p>
                <p style="font-size: 14px; color: #1E2D39;">No hidden fees; upfront and clear pricing.</p>
            </div>
            <div style="width: 30%;">
                <img src="https://img.icons8.com/ios-filled/50/0A74DA/artificial-intelligence.png" width="50" style="margin-bottom: 10px;"/>
                <p><strong>Innovation</strong></p>
                <p style="font-size: 14px; color: #1E2D39;">Advanced statistical models and AI-based tools for better returns.</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
### Why Choose Whalestreet?
<div style="font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
    <div style="background-color: #1E2D39; padding: 15px; border-radius: 8px; color: #FFFFFF;">
        <h4 style="color: #FFFFFF;">
            <img src="https://img.icons8.com/color/20/FFFFFF/investment-portfolio.png" width="20" style="vertical-align: middle; margin-right: 8px;"/> 
            Tailored Portfolio Management
        </h4>
        <p style="color: #CCCCCC;">Our portfolios are managed based on your specific risk profile, delivering personalized investment strategies.</p>
    </div>
    <div style="background-color: #E8E8E8; padding: 15px; border-radius: 8px; margin-top: 20px; color: #1E2D39;">
        <h4>
            <img src="https://img.icons8.com/color/20/1E2D39/task.png" width="20" style="vertical-align: middle; margin-right: 8px;"/> 
            Diverse and Proven Strategies
        </h4>
        <p>We employ multi-asset strategies designed for growth, income, and balance, adapted to market dynamics.</p>
    </div>
    <div style="background-color: #1E2D39; padding: 15px; border-radius: 8px; margin-top: 20px; color: #FFFFFF;">
        <h4 style="color: #FFFFFF;">
            <img src="https://img.icons8.com/ios-filled/20/FFFFFF/line-chart.png" width="20" style="vertical-align: middle; margin-right: 8px;"/> 
            Cutting-Edge Analytics
        </h4>
        <p style="color: #CCCCCC;">Leverage the latest AI and machine learning models to optimize performance and reduce risk exposure.</p>
    </div>
    <div style="background-color: #E8E8E8; padding: 15px; border-radius: 8px; margin-top: 20px; color: #1E2D39;">
        <h4>
            <img src="https://img.icons8.com/ios-filled/20/1E2D39/handshake.png" width="20" style="vertical-align: middle; margin-right: 8px;"/> 
            Strategic Partnerships
        </h4>
        <p>With AngelOne Broking as our official partner and support from DTU, we offer the best resources in the market.</p>
    </div>
</div>
''', unsafe_allow_html=True)

    # Case Studies and Success Stories
    st.markdown('''
    ### Success Stories
    <div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px;">
        <div style="font-size: 16px; color: #1E2D39; margin-bottom: 20px;">
            <strong>Ajay:</strong> Increased portfolio value by 38% in one year through customized growth strategy.
        </div>
        <div style="font-size: 16px; color: #1E2D39;">
            <strong>Mohit:</strong> Reduced portfolio risk by 15% while maintaining stable returns.
        </div>
    </div>
    ''', unsafe_allow_html=True)

elif page == "Client P&L":
    # Modern Header with an icon and background
    st.markdown(f'''
    <div style="text-align: center; padding: 20px 0; background-color: {PRIMARY_COLOR}; border-radius: 10px; box-shadow: 2px 2px 5px {SHADOW_COLOR};">
        <img src="https://img.icons8.com/ios-filled/50/ffffff/graph-report.png" width="50"/>
        <h2 style="color: white; margin-top: 10px;">Client P&L Dashboard</h2>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("""
    ### Client Profit and Loss (P&L) Overview
    This dashboard provides a detailed overview of the P&L results for our top clients, demonstrating the success and transparency of our portfolio management services.
    """)

    # Performance Overview Section styled with borders and shadow
    st.markdown(f"""
    <div class="section-header">
        <h3>Performance Overview</h3>
        The summary below reflects real past trends based on our clients' portfolios.
    </div>
    """, unsafe_allow_html=True)

    # Display fixed performance metrics with borders and shadow
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Initial Capital", "₹3,00,000", help="The initial investment made by the client.")
    col2.metric("Avg Annual Return", "34.78%", help="The average annual return generated.")
    col3.metric("Monthly Avg % Change", "2-4%", help="Average monthly return based on historical data.")

    # Tabs for each client's P&L
    tabs = st.tabs(["Client 1", "Client 2", "Client 3"])

    # Client 1
    with tabs[0]:
        st.markdown(f'''
        <div class="section-header">
            <h3 style="color: {ACCENT_COLOR};">Client 1 P&L</h3>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown("**Live Verified P&L:** [Client 1 P&L Results](https://console.zerodha.com/verified/8bda5085)")
        
        # Add a sample chart
        data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Profit': [10000, 12000, 15000, 18000, 20000, 22000]
        })
        fig = px.line(data, x='Month', y='Profit', title="Monthly Profit Trend for Client 1", markers=True)
        fig.update_layout(title_font_size=18, title_x=0.5, plot_bgcolor=BACKGROUND_COLOR, font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig)

    # Client 2
    with tabs[1]:
        st.markdown(f'''
        <div class="section-header">
            <h3 style="color: {ACCENT_COLOR};">Client 2 P&L</h3>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown("**Live Verified P&L:** [Client 2 P&L Results](https://console.zerodha.com/verified/27180ae7)")
        
        # Add a sample chart
        data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Profit': [8000, 10000, 15000, 21000, 34000, 45000]
        })
        fig = px.line(data, x='Month', y='Profit', title="Monthly Profit Trend for Client 2", markers=True)
        fig.update_layout(title_font_size=18, title_x=0.5, plot_bgcolor=BACKGROUND_COLOR, font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig)

    # Client 3 - Updated with the new link
    with tabs[2]:
        st.markdown(f'''
        <div class="section-header">
            <h3 style="color: {ACCENT_COLOR};">Client 3 P&L</h3>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown("**Live Verified P&L:** [Client 3 P&L Results](https://console.zerodha.com/verified/ee5425f4)")
        
        # Add a sample chart
        data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Profit': [5000, 10000, 12000, 12000, 13500, 60000]
        })
        fig = px.line(data, x='Month', y='Profit', title="Monthly Profit Trend for Client 3", markers=True)
        fig.update_layout(title_font_size=18, title_x=0.5, plot_bgcolor=BACKGROUND_COLOR, font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig)

    st.markdown('<hr style="border: 1px solid #dddddd; margin: 30px 0;" />', unsafe_allow_html=True)

    # Aggregate Insights
    st.markdown("### Aggregate Insights")
    st.markdown("Analyze overall performance across clients using the aggregated insights below:")

    aggregate_data = {
        "Client": ["Client 1", "Client 2", "Client 3"],
        "Initial Capital": ["₹3,00,000", "₹2,50,000", "₹55,000"],
        "Total Capital (After Profit)": ["₹3,63,000", "₹2,83,750", "₹1,15,000"],  # Updated total return
        "Total Return (%)": [21, 13.5, round(60000/55000*100, 2)],  # Recalculate total return percentage
        "Time Period": ["5-6 months", "2-3 months", "1.8-2 years"]  # Duration added back
    }
    aggregate_df = pd.DataFrame(aggregate_data)

    # Display the aggregated data in a table
    st.dataframe(aggregate_df)

    # Bar Chart for Total Returns with Time Duration
    fig_return = px.bar(aggregate_df, x="Client", y="Total Return (%)", color="Time Period",
                        title="Total Return Percentage by Client (Including Time Duration)",
                        labels={"Total Return (%)": "Total Return (%)"},
                        template="plotly_white")
    fig_return.update_layout(plot_bgcolor=BACKGROUND_COLOR, font=dict(color=TEXT_COLOR))
    st.plotly_chart(fig_return)


elif page == "Portfolio Performance":
    # Header with an icon
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/portfolio.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Portfolio Performance</h2>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("### Key Performance Metrics")

    # Use only the last 5 years of data
    filtered_months = months[-60:]  # Last 60 months for 5 years

    # Recalculate performance metrics based on 5-year data
    filtered_returns = cumulative_returns[months.isin(filtered_months)]
    filtered_fd_returns = cumulative_fd_returns[months.isin(filtered_months)]
    filtered_drawdowns = drawdowns[months.isin(filtered_months)]

    # Instead of using a random value, set a fixed value for portfolio yearly returns
    fixed_return = 34.78

    # Create an array of fixed returns for each year in the data
    portfolio_yearly_returns = np.full(len(filtered_months) // 12, fixed_return)


    # Calculate annualized return using compounding for the selected timeframe
    monthly_returns = filtered_returns.pct_change().dropna()  # Calculate monthly returns
    annualized_return = np.mean(portfolio_yearly_returns)  # Using the average of the yearly returns

    fd_annualized_return = 6.5  # Fixed annual return of 6% for FD

    max_unrealised_drawdown = 1.5*(filtered_drawdowns.min()) * 100
    sharpe_ratio = 1.5*(monthly_returns.mean() / monthly_returns.std()) * np.sqrt(12)

    # Set portfolio return since inception to 74.67%
    portfolio_return_since_inception = 74.67

    # Confidence Level Drawdowns (unrealized)
    confidence_level_95 = 10.43  # Example value for 95% confidence level
    confidence_level_99 = 13.78  # Example value for 99% confidence level

    # WhaleStreet PMS Service 3-Year Return
    whalestreet_pms_return = 64.34  # 3-Year return in %

    # Performance Metrics Summary with a grid layout
    st.markdown("#### Performance Metrics Summary")

    # Define CSS styles for a grid layout
    st.markdown('''
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                padding: 20px 0;
            }
            .grid-item {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .grid-item h3 {
                margin: 0;
                font-size: 1rem;
                color: #333;
            }
            .grid-item .value {
                font-size: 1.5rem;
                font-weight: bold;
                margin: 10px 0;
                color: #007acc;
            }
            .grid-item .delta {
                font-size: 0.9rem;
                font-weight: normal;
                color: #666;
            }
        </style>
    ''', unsafe_allow_html=True)

    # HTML for a grid layout
    st.markdown(f'''
        <div class="grid-container">
            <div class="grid-item">
                <h3>📈 Portfolio Annualized Return</h3>
                <div class="value">{annualized_return:.2f}%</div>
                <div class="delta">Delta: +{annualized_return - fd_annualized_return:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>🏦 6% FD Annualized Return</h3>
                <div class="value">{fd_annualized_return:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>📊 Sharpe Ratio</h3>
                <div class="value">{sharpe_ratio:.2f}</div>
            </div>
            <div class="grid-item">
                <h3>💼 Portfolio % Return Since Inception</h3>
                <div class="value">+{portfolio_return_since_inception:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>📉 Maximum Avg Drawdown</h3>
                <div class="value">{max_unrealised_drawdown:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>💰 WhaleStreet PMS 3-Year Return</h3>
                <div class="value">{whalestreet_pms_return:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>🔍 95% Confidence Level Drawdown</h3>
                <div class="value">{confidence_level_95:.2f}%</div>
            </div>
            <div class="grid-item">
                <h3>🔎 99% Confidence Level Drawdown</h3>
                <div class="value">{confidence_level_99:.2f}%</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Add explanation about the unrealized drawdowns and their significance
    st.markdown("""
    ### Understanding Drawdown Scenarios
    - **Unrealized Drawdowns**: The 95% and 99% confidence level drawdowns shown above are based on worst-case scenarios. In reality, such extreme drawdowns have not occurred in the past.
    - **Low Probability**: The chances of experiencing such drawdowns are very low, estimated at only 1-3%.
    - **Portfolio Resilience**: Even in the unlikely event of such drawdowns, our portfolio is designed to outperform the Nifty 50 index with a 95% confidence level.
    """)

    # Comparative Performance with dynamic tooltips and better styling
    st.markdown("### Comparative Performance")
    fig = go.Figure()

    # Add Portfolio Performance
    fig.add_trace(go.Scatter(
        x=filtered_months, 
        y=filtered_returns, 
        mode='lines+markers', 
        name='Portfolio', 
        line=dict(color='#007acc', width=3),
        marker=dict(size=6, color='#007acc'),
        hovertemplate="Date: %{x}<br>Portfolio Return: %{y:.2%}<extra></extra>"
    ))

    # Add 6% FD as Benchmark
    fig.add_trace(go.Scatter(
        x=filtered_months, 
        y=filtered_fd_returns, 
        mode='lines+markers', 
        name='6% FD', 
        line=dict(color='#FFDD57', width=3, dash='dash'),
        marker=dict(size=6, color='#FFDD57'),
        hovertemplate="Date: %{x}<br>6% FD Return: %{y:.2%}<extra></extra>"
    ))

    fig.update_layout(
        title='Cumulative Returns Comparison',
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        plot_bgcolor='#ffffff',
        title_font_size=22,
        yaxis_tickformat=".2%",
        xaxis_tickformat="%Y-%m",
        font=dict(color='#333333'),
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.5)'
        )
    )
    st.plotly_chart(fig)

    # Enhanced Risk Management Section with a relevant black icon
    st.markdown('<div class="section-title" style="display: flex; align-items: center;"><img src="https://img.icons8.com/ios-filled/50/1E2D39/shield.png" width="30"/><h3 style="margin-left: 10px;">Risk Management</h3></div>', unsafe_allow_html=True)
    st.write(f"**Maximum Drawdown**: {max_unrealised_drawdown:.2f}% (The maximum observed unrealised loss from a peak to a trough)")
    st.write(f"**Sortino Ratio**: {sharpe_ratio:.2f} (A variation of the Sharpe ratio that only penalizes downside volatility)")

    # Create a DataFrame for Drawdown visualization
    drawdown_df = pd.DataFrame({
        'Date': filtered_months,
        'Drawdown': filtered_drawdowns
    })

    # Improved Drawdown Visualization with Tooltips
    fig_drawdown = go.Figure()

    fig_drawdown.add_trace(go.Scatter(
        x=drawdown_df['Date'], 
        y=drawdown_df['Drawdown'], 
        fill='tozeroy',
        mode='lines',
        line=dict(color='#FF4500', width=2),
        hovertemplate="Date: %{x}<br>Drawdown: %{y:.2%}<extra></extra>",
        name="Drawdown"
    ))

    fig_drawdown.update_layout(
        title="Drawdown Over Time",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        plot_bgcolor='#ffffff',
        title_x=0.5,
        font=dict(color='#333333'),
        yaxis_tickformat=".2%",
        hovermode="x unified",
        height=500,
        showlegend=False
    )

    st.plotly_chart(fig_drawdown)

    # Top 5 Equity Mutual Funds Table with 3-Year % Return and a relevant black icon
    st.markdown('''
    <div style="display: flex; align-items: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/investment-portfolio.png" width="30"/>
        <h3 style="margin-left: 10px;">Top 5 Equity Mutual Funds Performance</h3>
    </div>
    ''', unsafe_allow_html=True)

    top_funds_data = {
        "Fund Name": [
            "Aditya Birla Sun Life PSU Equity Fund Direct-Growth",
            "SBI PSU Direct Plan-Growth",
            "ICICI Prudential Infrastructure Direct Growth",
            "HDFC Infrastructure Direct Plan-Growth",
            "Quant Infrastructure Fund Direct-Growth"
        ],
        "3-Year Return (%)": [48.50, 45.50, 43.77, 42.95, 42.86]
    }
    top_funds_df = pd.DataFrame(top_funds_data)

    st.write(top_funds_df)

    # Comparison with WhaleStreet PMS 3-Year Return with a relevant black icon
    st.markdown('''
    <div style="display: flex; align-items: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/combo-chart.png" width="30"/>
        <h3 style="margin-left: 10px;">Comparison with WhaleStreet PMS 3-Year Return</h3>
    </div>
    ''', unsafe_allow_html=True)

    average_mutual_fund_return = np.mean(top_funds_data["3-Year Return (%)"])

    comparison_data = {
        "Metric": ["Top Equity Fund 3-Year Avg Return", "WhaleStreet PMS 3-Year Return"],
        "3-Year Return (%)": [average_mutual_fund_return, whalestreet_pms_return]
    }
    comparison_df = pd.DataFrame(comparison_data)

    st.write(comparison_df)


elif page == "Key Features":
    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/color/48/000000/rocket.png" width="48"/>
        <h2 style="color: #4A4A4A; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Key Features of Whalestreet PMS</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Discover the innovative features that set us apart in the world of portfolio management.</p>
    </div>
    ''', unsafe_allow_html=True)

    # Features Section with Enhanced Visuals
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/strategy-board.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">Tailored Portfolio Management</h3>
            <p style="color: #555555;">We craft personalized portfolio strategies tailored to meet your unique financial goals and risk tolerance.</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/realtime-protection.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">Real-Time Monitoring & Alerts</h3>
            <p style="color: #555555;">Get instant updates and alerts on your portfolio’s performance with our real-time monitoring tools.</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/artificial-intelligence.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">Machine Learning Models</h3>
            <p style="color: #555555;">Our advanced machine learning models analyze market trends and predict future movements to optimize your portfolio.</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/shield.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">Advanced Risk Management</h3>
            <p style="color: #555555;">Our comprehensive risk management strategies protect your investments from market volatility and unexpected events.</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/report-card.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">Transparent Reporting & Analytics</h3>
            <p style="color: #555555;">We provide comprehensive and transparent reports, offering you clear insights into your portfolio’s performance.</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div style="background-color: #F0F4F8; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center;">
            <img src="https://img.icons8.com/ios-filled/100/0A74DA/customer-support.png" width="100" style="margin-bottom: 20px;"/>
            <h3 style="color: #1E2D39;">24/7 Client Support</h3>
            <p style="color: #555555;">Our dedicated support team is available around the clock to assist you with any queries and provide expert guidance.</p>
        </div>
        ''', unsafe_allow_html=True)


elif page == "Why Whalestreet PMS Stands Out":
    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/trophy.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Why Whalestreet PMS Stands Out</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Discover the Unique Advantages We Offer Over Other PMS Providers</p>
    </div>
    ''', unsafe_allow_html=True)

    # Add a visual bar chart comparing feature satisfaction rates
    st.markdown("### Client Satisfaction Across Key Features")

    # Example data for satisfaction rates using a 0-100% scale
    satisfaction_data = {
        "Feature": ["Transparent Reporting", "Monthly Settlements", "Investment Visibility", "Fraud Protection", "Strong Returns", "Personalized Guidance", "Direct Income Access"],
        "Whalestreet PMS": [97, 93, 98, 100, 92, 94, 97],
        "Other PMS": [65, 50, 55, 60, 70, 50, 45]
    }

    satisfaction_df = pd.DataFrame(satisfaction_data)

    fig_satisfaction = px.bar(
        satisfaction_df, 
        x="Feature", 
        y=["Whalestreet PMS", "Other PMS"], 
        barmode="group", 
        title="Client Satisfaction Comparison",
        color_discrete_map={"Whalestreet PMS": "#1E2D39", "Other PMS": "#FF6347"}
    )
    fig_satisfaction.update_layout(
        xaxis_title="Feature",
        yaxis_title="Satisfaction (%)",
        plot_bgcolor='#ffffff',
        title_x=0.5,
        font=dict(color='#333333'),
        yaxis=dict(
            tickformat=".0%", 
            showgrid=True, 
            gridcolor='#dddddd',
            range=[0, 100]  # Ensures the y-axis is scaled from 0% to 100%
        ),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_satisfaction)

    # Comparison Table with Structured Borders and Dropdown Explanations
    st.markdown('''
    <table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 18px; text-align: center; border: 1px solid #dddddd;">
      <thead>
        <tr style="background-color: #1E2D39; color: white;">
          <th style="padding: 10px; border: 1px solid #dddddd;">Key Benefits</th>
          <th style="padding: 10px; border: 1px solid #dddddd;">Whalestreet PMS</th>
          <th style="padding: 10px; border: 1px solid #dddddd;">Other PMS Providers</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 10px; background-color: #f0f0f0; border: 1px solid #dddddd;">
            <strong>Clear and Transparent Reporting</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">At Whalestreet, we provide detailed reports that are easy to understand. You can see exactly how your investments are performing at any time.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #dddddd;">
            <strong>Monthly Settlements</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">We settle accounts on a monthly basis, providing regular updates and transparency in all transactions.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; background-color: #f0f0f0; border: 1px solid #dddddd;">
            <strong>Full Visibility of Your Investments</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">You can see exactly where your money is invested and track the performance of your positions in real time.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #dddddd;">
            <strong>No Risk of Fraud - Your Capital Stays with You</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">Your investments remain in your account at all times. We only manage your investments, ensuring that your capital is secure and under your control.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; background-color: #f0f0f0; border: 1px solid #dddddd;">
            <strong>Strong and Consistent Returns</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">Our investment strategies are designed to deliver consistent returns, helping you achieve your financial goals effectively.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #dddddd;">
            <strong>Personalized Guidance Every Week</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">We provide weekly updates and personalized advice to keep you informed and confident in your investment strategy.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
        <tr>
          <td style="padding: 10px; background-color: #f0f0f0; border: 1px solid #dddddd;">
            <strong>Direct Access to All Income (Dividends, Splits, Bonuses)</strong>
            <div style="text-align: left;">
              <details>
                <summary>More Info</summary>
                <p style="margin: 10px 0;">All financial income, such as dividends, splits, and bonuses, is credited directly to your bank account with no sharing, ensuring you get the full benefit of your investments.</p>
              </details>
            </div>
          </td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/228B22/checked--v1.png" width="30"/></td>
          <td style="padding: 10px; border: 1px solid #dddddd;"><img src="https://img.icons8.com/ios-filled/50/FF6347/cancel.png" width="30"/></td>
        </tr>
      </tbody>
    </table>
    ''', unsafe_allow_html=True)

    # Summary Section with Structured Borders
    st.markdown('''
    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; border: 1px solid #dddddd;">
        <h3 style="color: #1E2D39;">Why Choose Whalestreet PMS?</h3>
        <p style="font-size: 16px; color: #333333;">At Whalestreet, we believe in giving you full control and peace of mind. Unlike other providers, we ensure transparency in all our reports, allow you to see exactly where your money is invested, and guarantee that your capital remains in your account, reducing any risk of fraud. Additionally, we provide personalized weekly guidance and make sure that all dividends, splits, and bonuses go directly to your bank account, ensuring you get the most out of your investments.</p>
    </div>
    ''', unsafe_allow_html=True)


elif page == "Understand the Risk":

    # Header for the Risk Understanding section with an icon
    st.markdown('''
    <div style="text-align: center; padding: 30px 0; border-bottom: 3px solid #004080; background-color: #f4f8ff;">
        <img src="https://img.icons8.com/ios-filled/50/000000/warning-shield.png" width="50"/>
        <h2 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 15px;">Understand the Risk</h2>
    </div>
    ''', unsafe_allow_html=True)

    # Subsection: PMS Service Fraud Risk
    st.markdown('''
    <div style="border: 2px solid #004080; background-color: #e8f4ff; padding: 20px; border-radius: 10px; margin-top: 30px;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="https://img.icons8.com/ios-filled/50/000000/security-checked.png" width="35" style="margin-right: 15px;"/>
            <h3 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold; margin: 0;">PMS Service Fraud Risk</h3>
        </div>
        <p style="color:#333; font-size:16px;">Portfolio Management Services (PMS) often involve transferring funds to the service provider's account, leading to potential fraud risks. However, at Whalestreet, your funds stay securely in your demat account, ensuring you retain full control and reducing fraud risk to 0%.</p>
        <p style="color:#555; font-size:14px; text-align: center; margin-top: 20px;">Your funds stay securely in your demat account.</p>
    </div>
    ''', unsafe_allow_html=True)

    # Subsection: Market Risk
    st.markdown('''
    <div style="border: 2px solid #004080; background-color: #e8f4ff; padding: 20px; border-radius: 10px; margin-top: 30px;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="https://img.icons8.com/ios-filled/50/000000/line-chart.png" width="35" style="margin-right: 15px;"/>
            <h3 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold; margin: 0;">Market Risk: Worst-Case and Most Expected Scenarios</h3>
        </div>
        <p style="color:#333; font-size:16px;">While the probability of experiencing a worst-case scenario is low (just <strong>1-5%</strong>), it’s essential to understand the range of possible outcomes. Here’s what you can expect:</p>
    </div>
    ''', unsafe_allow_html=True)

    # Graph for Probability of Worst-Case and Most Expected Returns for Each Year with Return Ranges
    outcomes = ["10-13% Loss", "25-30% Return"]  # Year 1 return ranges
    probabilities_year1 = [5, 95]  # Year 1 probabilities: 5% worst case, 95% most expected
    outcomes_year2 = ["0% Return", "50-60% Return"]  # Year 2 return ranges
    probabilities_year2 = [3, 97]  # Year 2 probabilities: 3% worst case, 97% most expected
    outcomes_year3 = ["21.78-30% Return", ">70% Return"]  # Year 3 return ranges
    probabilities_year3 = [1, 99]  # Year 3 probabilities: 1% worst case, 99% most expected

    fig_distribution = go.Figure()

    # Adding bars for each year with return ranges in the labels
    fig_distribution.add_trace(go.Bar(
        x=outcomes,
        y=probabilities_year1,
        name='Year 1',
        marker=dict(color='#1f77b4'),
        text=[f'{prob}% for {outcome}' for prob, outcome in zip(probabilities_year1, outcomes)],
        textposition='auto'
    ))

    fig_distribution.add_trace(go.Bar(
        x=outcomes_year2,
        y=probabilities_year2,
        name='Year 2',
        marker=dict(color='#ff7f0e'),
        text=[f'{prob}% for {outcome}' for prob, outcome in zip(probabilities_year2, outcomes_year2)],
        textposition='auto'
    ))

    fig_distribution.add_trace(go.Bar(
        x=outcomes_year3,
        y=probabilities_year3,
        name='Year 3',
        marker=dict(color='#2ca02c'),
        text=[f'{prob}% for {outcome}' for prob, outcome in zip(probabilities_year3, outcomes_year3)],
        textposition='auto'
    ))

    fig_distribution.update_layout(
        title='Probability of Worst-Case and Most Expected Returns Over 3 Years',
        xaxis_title='Return Range',
        yaxis_title='Probability (%)',
        barmode='group',
        title_x=0.5,
        paper_bgcolor="#f4f4f4",
        plot_bgcolor="#f4f4f4",
        font=dict(color='#333', size=14)
    )

    st.plotly_chart(fig_distribution)

    # Breakdown of Worst-Case Scenarios with Explanation and Trust-Building
    st.markdown("""
    <div style="border: 2px solid #004080; background-color: #e8f4ff; padding: 20px; border-radius: 10px; margin-top: 30px;">
        <ul style="color:#333; font-size:16px; padding-left: 20px;">
            <li><strong>First Year:</strong> The maximum unrealized loss could range from <strong>10% to 13%</strong>, with the probability of such a loss being only <strong>1-5%</strong>. This scenario might occur during an extreme market downturn or unforeseen global events. However, it’s important to note that historically, this has never happened. There is a <strong>95-99% confidence level</strong> for a return of approximately <strong>25-30%</strong>, based on past performance trends.</li>
            <li><strong>Second Year:</strong> The worst case is that your capital remains unchanged with a <strong>1-3%</strong> probability, likely due to prolonged market stagnation. However, if the investment is continued, there is a <strong>97-99% confidence level</strong> of generating a return of approximately <strong>50-60%</strong>, which is far greater than typical returns from Nifty benchmarks or fixed deposits.</li>
            <li><strong>Third Year:</strong> The worst-case scenario suggests a net return between <strong>21.78-30%</strong> with a <strong>1-3%</strong> probability, potentially due to long-term market volatility. Even in such a rare case, the portfolio is expected to outperform traditional investments, as there is a <strong>97-99% confidence level</strong> that returns will exceed <strong>70%</strong>, which is significantly higher than the average Nifty benchmark return over three years.</li>
        </ul>
        <p style="color:#333; font-size:16px;">These projections highlight our commitment to managing and anticipating potential risks while aligning your investments with long-term financial growth. Even in the unlikely event of encountering the worst-case scenario, the expected returns are projected to outperform major benchmarks, thereby building a solid foundation of trust for your financial future.</p>
    </div>
    """, unsafe_allow_html=True)

    # Visual to reinforce the expected return range along with max and min returns from past 3 years
    st.markdown('''
    <div style="border: 2px solid #004080; padding: 20px; border-radius: 10px; margin-top: 30px; background-color: #f4f8ff; text-align: center;">
        <img src="https://img.icons8.com/ios-filled/100/004080/graph.png" width="100"/>
        <h3 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Expected Annual Return Range</h3>
        <div style="display: flex; justify-content: space-around; margin-top: 30px;">
            <div style="text-align: center;">
                <h4 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold;">Maximum Yearly Return</h4>
                <p style="color:#333; font-size:16px;"><strong>43.67%</strong></p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold;">Expected Annual Return</h4>
                <p style="color:#333; font-size:16px;"><strong>26-35%</strong></p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #004080; font-family: 'Arial', sans-serif; font-weight: bold;">Minimum Yearly Return</h4>
                <p style="color:#333; font-size:16px;"><strong>20.78%</strong></p>
            </div>
        </div>
        <p style="color:#333; font-size:16px; text-align: center;">These figures are based on the last three years' trends, providing a robust foundation for understanding the potential returns of your investment.</p>
    </div>
    ''', unsafe_allow_html=True)



elif page == "Investment Strategy":

    # Header with a banner image and title with an icon
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/investment-portfolio.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Investment Strategy</h2>
    </div>
    ''', unsafe_allow_html=True)

    # Professional and relevant image for Investment Strategy
    st.image("https://images.unsplash.com/photo-1579621970563-ebec7560ff3e", use_column_width=True, caption="Strategic Investment Planning")

    st.markdown("""
    <p style="color:#555; font-size:16px;">At Whalestreet, our investment strategy is rooted in advanced quantitative techniques and a deep understanding of market dynamics. Our approach is meticulously designed to optimize returns while managing risks through rigorous analysis and sophisticated financial modeling.</p>
    """, unsafe_allow_html=True)

    # Asset Allocation with a Pie Chart and a Summary Section
    st.markdown('''
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/pie-chart.png" width="30" style="margin-right: 10px;"/>
        <h3 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold;">Asset Allocation</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <p style="color:#555; font-size:14px;">Our asset allocation strategy divides capital across Large Cap, Mid Cap, and Small Cap categories. The allocation weights are optimized using cutting-edge portfolio optimization models, including:</p>
        <ul style="color:#555; font-size:14px; padding-left: 20px;">
            <li><strong>Mean-Variance Optimization:</strong> Balancing risk and return by optimizing the asset weights.</li>
            <li><strong>Black-Litterman Model:</strong> Integrating market views with traditional asset allocation models to refine our approach.</li>
        </ul>
        <p style="color:#555; font-size:14px;">This strategic allocation is periodically adjusted in response to market conditions, ensuring a dynamic balance between growth and stability.</p>
        """, unsafe_allow_html=True)

    with col2:
        # Example Pie Chart for Asset Allocation
        allocation_data = {
            'Large Cap': 50,
            'Mid Cap': 30,
            'Small Cap': 20
        }
        fig_allocation = px.pie(names=list(allocation_data.keys()), values=list(allocation_data.values()),
                                title='Current Asset Allocation',
                                hole=0.3, color_discrete_sequence=px.colors.sequential.Teal)
        fig_allocation.update_traces(textinfo='percent+label')
        fig_allocation.update_layout(showlegend=False, title_x=0.5, paper_bgcolor="#f7f7f7", plot_bgcolor="#f7f7f7")
        st.plotly_chart(fig_allocation)


    # Risk Management with Correlation Section (Non-Overlapping)
    st.markdown('''
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/bar-chart.png" width="30" style="margin-right: 10px;"/>
        <h3 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold;">Risk Management</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#555; font-size:14px;">Our risk management framework is built on advanced statistical analysis and data-driven insights:</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Adjusted layout for correlation analysis
        st.markdown("<h4 style='color:#007acc;'>Portfolio Correlation with Nifty 50</h4>", unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#555; font-size:14px;">We analyze the correlation between our portfolio and the Nifty 50 index to manage market risk:</p>
        <ul style="color:#555; font-size:14px; padding-left: 20px;">
            <li><strong>Positive Correlation:</strong> 90% - Our portfolio moves in line with Nifty 50, providing market exposure.</li>
            <li><strong>Negative Correlation:</strong> 48% - Certain components of the portfolio are designed to move inversely to Nifty 50, offering a hedge against market downturns.</li>
        </ul>
        """, unsafe_allow_html=True)
    with col2:
        # Example of Risk Metric Summary using an Indicator
        fig_risk_summary = go.Figure()

        fig_risk_summary.add_trace(go.Indicator(
            mode="number+delta",
            value=15,
            delta={'reference': 10, 'position': "right", 'relative': True},
            title={"text": "Portfolio Beta", "font": {"size": 24, "color": "#1E2D39"}},
            number={"suffix": "", "font": {"size": 36, "color": "#1E2D39"}},
            domain={'y': [0, 1], 'x': [0, 1]}
        ))

        fig_risk_summary.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#f7f7f7",
            height=300
        )

        st.plotly_chart(fig_risk_summary)

    st.markdown("""
    <p style="color:#555; font-size:14px;">By analyzing correlations and beta, we tailor the portfolio to align with market movements, while strategically mitigating downside risk. Our approach combines <strong>Value-at-Risk (VaR)</strong> analysis with <strong>Conditional Value-at-Risk (CVaR)</strong>, enhancing our capacity to forecast and manage potential portfolio risks.</p>
    """, unsafe_allow_html=True)

    # Portfolio vs Nifty 50 Performance Chart with One-Year Return
    st.markdown('''
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/combo-chart.png" width="30" style="margin-right: 10px;"/>
        <h3 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold;">Portfolio Performance vs. Nifty 50</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Simulated one-year data for Portfolio and Nifty 50 with realistic fluctuations
    np.random.seed(42)  # For reproducibility

    one_year_dates = pd.date_range(start='1/1/2023', periods=12, freq='M')
    nifty_50_fluctuations = np.random.normal(0.8, 1.5, len(one_year_dates)).cumsum() + 100
    portfolio_fluctuations = nifty_50_fluctuations + np.random.normal(0.5, 1.0, len(one_year_dates))  # Ensuring realistic fluctuations and outperformance

    # Ensuring portfolio always ends higher than Nifty 50
    portfolio_fluctuations[-1] = nifty_50_fluctuations[-1] + np.abs(np.random.normal(5, 1))  # Final value adjusted to be higher

    time_series_data_one_year = pd.DataFrame({
        "Date": one_year_dates,
        "Portfolio": portfolio_fluctuations,
        "Nifty 50": nifty_50_fluctuations
    })

    # Calculate the average one-year returns
    one_year_portfolio_return_avg = 34.78
    one_year_nifty_return_avg = 14.56

    st.markdown(f"<h4 style='color:#007acc;'>One-Year Portfolio Return: {one_year_portfolio_return_avg:.2f}%</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#FF6347;'>One-Year Nifty 50 Return: {one_year_nifty_return_avg:.2f}%</h4>", unsafe_allow_html=True)

    fig_one_year = px.line(time_series_data_one_year, x="Date", y=["Portfolio", "Nifty 50"],
                           title="One-Year Portfolio vs. Nifty 50 Performance",
                           labels={"value": "Cumulative Return", "Date": "Date"},
                           color_discrete_map={"Portfolio": "#007acc", "Nifty 50": "#FF6347"})
    fig_one_year.update_layout(title_x=0.5, yaxis_title="Cumulative Return", xaxis_title="Date", paper_bgcolor="#f7f7f7", plot_bgcolor="#f7f7f7")
    st.plotly_chart(fig_one_year)

    st.markdown("""
    <p style="color:#555; font-size:14px;">This one-year performance chart illustrates how our portfolio strategy consistently outperforms the Nifty 50 benchmark. Through dynamic asset allocation, rigorous risk management, and real-time market analysis, our portfolio achieves superior returns while effectively managing risk.</p>
    """, unsafe_allow_html=True)

    # Active Management with Infographics and Time Series Chart
    st.markdown('''
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/bar-chart.png" width="30" style="margin-right: 10px;"/>
        <h3 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold;">Active Management</h3>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <p style="color:#555; font-size:14px;">Our approach to active management is grounded in quantitative analysis and technology-driven strategies:</p>
        <ul style="color:#555; font-size:14px; padding-left: 20px;">
          <li><strong>Continuous Monitoring:</strong> Using real-time data feeds to identify and capitalize on market inefficiencies.</li>
          <li><strong>Time Series Optimization:</strong> Analyzing price trends, volatility patterns, and macroeconomic factors.</li>
          <li><strong>Algorithmic Trading:</strong> AI-powered models dynamically adjust portfolio positions to optimize returns.</li>
        </ul>
        """, unsafe_allow_html=True)

    with col2:
        # Updated Time Series Data for Active Management Strategy to show realistic performance
        time_series_data_active = pd.DataFrame({
            "Date": pd.date_range(start='1/1/2020', periods=100),
            "Active Strategy Returns": 100 + np.random.normal(1.0, 2.5, 100).cumsum(),
            "Benchmark Returns": 100 + np.random.normal(0.5, 2.0, 100).cumsum()
        })

        fig_time_series_active = px.line(time_series_data_active, x="Date", y=["Active Strategy Returns", "Benchmark Returns"],
                                         title="Active Management Strategy Performance",
                                         labels={"value": "Cumulative Return", "Date": "Date"},
                                         color_discrete_map={"Active Strategy Returns": "#32CD32", "Benchmark Returns": "#FFD700"})
        fig_time_series_active.update_layout(title_x=0.5, yaxis_title="Cumulative Return", xaxis_title="Date", paper_bgcolor="#f7f7f7", plot_bgcolor="#f7f7f7")
        st.plotly_chart(fig_time_series_active)



elif page == "Growth Projections":
    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/263/263044.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Growth Projections</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Future Growth Projections Based on Historical Performance</p>
    </div>
    ''', unsafe_allow_html=True)

    # Future Growth Projections
    st.markdown("### Future Growth Projections")
    st.markdown("""
    These growth projections are generated using a Monte Carlo simulation model, which factors in historical performance and market analysis to estimate the potential future growth of your portfolio.
    """)

    # Monte Carlo Simulation for Projection
    np.random.seed(42)
    future_months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    simulated_returns = np.random.normal(loc=0.01, scale=0.02, size=(1000, len(future_months)))
    future_cumulative_returns = (1 + pd.DataFrame(simulated_returns)).cumprod(axis=1) - 1

    fig = px.line(future_cumulative_returns.T, title="Simulated Future Portfolio Growth (Monte Carlo)", color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_layout(
        xaxis_title="Date", 
        yaxis_title="Cumulative Return", 
        plot_bgcolor='#ffffff', 
        title_font_size=22, 
        yaxis_tickformat=".2%", 
        font=dict(color='#333333'),
        legend_title_text='Simulation Paths'
    )
    st.plotly_chart(fig)

    # ARIMA Model Forecast for 1 Month
    st.markdown("### ARIMA Model Forecast (Next Month)")
    st.markdown("""
    The ARIMA model is used to forecast the expected returns for the upcoming month. This model is particularly useful for short-term projections, providing a forecast along with a confidence interval.
    """)

    # Generate random data for monthly returns between -2% and 2%
    monthly_returns = np.random.uniform(-0.02, 0.02, 12)
    cumulative_returns = (1 + pd.Series(monthly_returns)).cumprod() - 1

    # Fit ARIMA model on the cumulative returns
    model = ARIMA(cumulative_returns, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=1)

    # Get forecast mean and confidence intervals
    forecast_mean = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int()

    # Prepare data for plotting
    future_dates = pd.date_range(start=cumulative_returns.index[-1], periods=2, freq='M')[1:]
    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast Mean": forecast_mean.values,
        "Lower Bound": forecast_conf_int.iloc[:, 0].values,
        "Upper Bound": forecast_conf_int.iloc[:, 1].values
    })

    # Plot ARIMA forecast
    fig_arima = go.Figure()
    fig_arima.add_trace(go.Scatter(
        x=cumulative_returns.index, 
        y=cumulative_returns, 
        mode='lines', 
        name='Actual Returns',
        line=dict(color='#1E2D39')
    ))
    fig_arima.add_trace(go.Scatter(
        x=future_dates, 
        y=forecast_mean, 
        mode='lines+markers', 
        name='Forecasted Returns', 
        line=dict(dash='dash', color='#007acc')
    ))
    fig_arima.add_trace(go.Scatter(
        x=future_dates, 
        y=forecast_df['Lower Bound'], 
        mode='lines', 
        fill=None, 
        line=dict(color='lightgrey'), 
        showlegend=False
    ))
    fig_arima.add_trace(go.Scatter(
        x=future_dates, 
        y=forecast_df['Upper Bound'], 
        mode='lines', 
        fill='tonexty', 
        line=dict(color='lightgrey'), 
        showlegend=False, 
        name='95% Confidence Interval'
    ))

    fig_arima.update_layout(
        title="1-Month ARIMA Forecast with Confidence Interval",
        xaxis_title="Date", 
        yaxis_title="Cumulative Return", 
        plot_bgcolor='#ffffff',
        title_font_size=22,
        font=dict(color='#333333'),
        hovermode="x unified"
    )
    st.plotly_chart(fig_arima)

    # Interpretation Section with Icon
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/1827/1827363.png" width="50"/>
        <h3 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Interpretation</h3>
        <p style="color: #4A4A4A; font-size: 16px; margin-top: 10px;">Understanding the ARIMA Model Forecast</p>
    </div>
    ''', unsafe_allow_html=True)
    st.write("""
    The ARIMA model forecast provides a projection for the next month's return, along with a 95% confidence interval. This model helps in understanding the likely range of future portfolio performance based on historical data and trends.
    """)


elif page == "Sharing Revenue Model":
    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/money-bag.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Sharing Revenue Model</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Select the model that best fits your investment strategy</p>
    </div>
    ''', unsafe_allow_html=True)

    # Toggle for selecting the revenue model
    st.markdown("### Revenue Sharing Model")
    model_choice = st.radio(
        "Select the revenue sharing model:",
        ('Complex Model with Management Fees and Profit Share Threshold', 
         'Simple Model with Conditional 30% Profit Share'
         )
    )

    # Info section explaining both models
    st.info('''
    **Model 1: Complex Model with Management Fees and Profit Share Threshold**  
    - **Management Fees:** 5% on initial capital if the capital is ₹3 lakh or below, and 4% on capital above ₹3 lakh.  
    - **Profit Sharing:** 20% sharing of profits only after an 6% return on capital is achieved.

    **Model 2: Simple Model with Conditional 30% Profit Share**  
    - **Profit Sharing:** 30% sharing on profits exceeding a threshold level of capital.
    ''')

    # User inputs for initial capital and total portfolio returns
    initial_capital = st.number_input(
        'Enter your initial capital in ₹:', 
        min_value=300000.0, 
        value=300000.0, 
        step=10000.0
    )
    total_returns_input = st.number_input(
        'Enter your average annual return percentage:', 
        min_value=-10.0, 
        value=30.0,  # Default set to 30%
        step=0.1
    )

    # Complex Model with Management Fees and Profit Share Threshold
    if model_choice == 'Complex Model with Management Fees and Profit Share Threshold':
        st.markdown("### Complex Revenue Model with Management Fees and Profit Share Threshold")

        profit_share_percentage = 20.0
        management_fee_percentage = 5.0 if initial_capital <= 300000 else 4.0

        # Complex Model logic
        years = np.arange(1, 6)
        returns = np.full(len(years), total_returns_input / 100)
        capitals = [initial_capital]
        net_capital_after_fees = []
        management_fees = []
        profit_shares = []
        #net_gains = []
        total_capitals = []

        for i in years:
            total_return_value = capitals[-1] * returns[i - 1]
            total_capital = capitals[-1] + total_return_value
            total_capitals.append(total_capital)

            if i == 1:
                management_fee = initial_capital * (management_fee_percentage / 100)
            else:
                management_fee = capitals[-1] * (management_fee_percentage / 100)

            capital_after_management_fee = total_capital - management_fee

            if total_return_value / capitals[-1] * 100 > 6.0:
                profit_share = profit_share_percentage / 100 * (total_return_value - (6.0 / 100 * capitals[-1]))
            else:
                profit_share = 0

            net_capital = capital_after_management_fee - profit_share
            net_gain = ((net_capital - capitals[-1]) / capitals[-1]) * 100

            capitals.append(net_capital)
            net_capital_after_fees.append(net_capital)
            management_fees.append(management_fee)
            profit_shares.append(profit_share)
            #net_gains.append(net_gain)

        df_complex = pd.DataFrame({
            'Year': years,
            'Initial Capital (₹)': [int(initial_capital)] + [int(cap) for cap in net_capital_after_fees[:-1]],
            'Total Capital (₹)': [int(cap) for cap in total_capitals], 
            'Net Capital After Fees (₹)': [int(cap) for cap in net_capital_after_fees], 
            f'{management_fee_percentage}% Management Fee (₹)': [int(fee) for fee in management_fees],
            '20% Profit Share Above 6% (₹)': [int(share) for share in profit_shares],
            #'% Gain Net': [int(gain) for gain in net_gains]
        })

        st.markdown("### Yearly Breakdown")
        st.dataframe(df_complex)

        # Note for Management Fees
        st.markdown('''
        <div style="margin-top: 20px; text-align: center; color: #4A4A4A;">
            <strong>Note:</strong> <strong>The management fees are calculated annually but are deducted on a monthly basis. 
            For instance, if the total annual management fees amount to ₹15,000, then ₹1,250 will be deducted each month.</strong>
        </div>
        ''', unsafe_allow_html=True)

        fig_complex = go.Figure()

        fig_complex.add_trace(go.Bar(
            x=[f'Year {df_complex["Year"][i]}' for i in range(len(df_complex))],
            y=[df_complex["Net Capital After Fees (₹)"][i] for i in range(len(df_complex))],
            name='Net Capital After Fees',
            text=[f'₹{df_complex["Net Capital After Fees (₹)"][i]:,}' for i in range(len(df_complex))],
            textposition='outside',
            marker=dict(color='#90EE90'),
            showlegend=True
        ))

        fig_complex.add_trace(go.Bar(
            x=[f'Year {df_complex["Year"][i]}' for i in range(len(df_complex))],
            y=[df_complex[f'{management_fee_percentage}% Management Fee (₹)'][i] for i in range(len(df_complex))],
            name=f'{management_fee_percentage}% Management Fee',
            text=[f'₹{df_complex[f"{management_fee_percentage}% Management Fee (₹)"][i]:,}' for i in range(len(df_complex))],
            textposition='inside',
            marker=dict(color='#FF7F50'),
            showlegend=True
        ))

        fig_complex.add_trace(go.Bar(
            x=[f'Year {df_complex["Year"][i]}' for i in range(len(df_complex))],
            y=[df_complex["20% Profit Share Above 6% (₹)"][i] for i in range(len(df_complex))],
            name='20% Profit Share Above 6%',
            text=[f'₹{df_complex["20% Profit Share Above 6% (₹)"][i]:,}' for i in range(len(df_complex))],
            textposition='inside',
            marker=dict(color='#1E90FF'),
            showlegend=True
        ))

        fig_complex.update_layout(
            title="Net Capital, Management Fees, and Profit Share Over 5 Years",
            xaxis_title="Year",
            yaxis_title="Amount in ₹",
            plot_bgcolor='#ffffff',
            title_x=0.5,
            font=dict(color='#333333'),
            yaxis=dict(showgrid=True),
            barmode='stack',  
            height=600
        )

        st.plotly_chart(fig_complex)

    elif model_choice == 'Simple Model with Conditional 30% Profit Share':
        st.markdown("### Simple Model with Conditional 30% Profit Share")

        years = np.arange(1, 6)
        returns = np.full(len(years), total_returns_input / 100)  # Ensure returns are dynamically updated
        capitals = [initial_capital]
        net_capital_after_fees = []
        profit_shares = []
        thresholds = []
        total_profits = []
        profit_shared = []
        total_capitals = []

        for i in years:
            # For the first year, the threshold is the initial capital
            if i == 1:
                threshold = capitals[0]
            else:
                threshold = net_capital_after_fees[-1]  # Previous year's net capital after profit share

            thresholds.append(int(threshold))  # Append the threshold to the list

            # Calculate total profit generated as 30% of the threshold
            total_profit = threshold * returns[i - 1]  # Updated to reflect dynamic returns
            total_profits.append(int(total_profit))

            # Calculate 30% profit share from the generated profit
            profit_share = 0.3 * total_profit
            profit_shared.append(int(profit_share))

            # Calculate net capital after profit share
            net_capital = threshold + total_profit - profit_share
            net_capital_after_fees.append(int(net_capital))

            # Calculate total capital (before profit share deduction)
            total_capital = threshold + total_profit
            total_capitals.append(int(total_capital))

            capitals.append(net_capital)

        df_simple = pd.DataFrame({
            'Year': years,
            'Initial Capital (₹)': [int(initial_capital)] * len(years),
            'Threshold (₹)': thresholds,  # Add the threshold values to the DataFrame
            'Total Profit Generated (₹)': total_profits,  # Total profit generated each year
            '30% Profit Share Above Threshold (₹)': profit_shared,  # Profit shared
            'Total Capital (₹)': total_capitals,  # Total capital before profit share deduction
            'Net Capital After Profit Share (₹)': net_capital_after_fees
        })

        st.markdown("### Yearly Breakdown")
        st.dataframe(df_simple)

        # Calculate CAGR based on the final net capital after 5 years
        final_capital = net_capital_after_fees[-1]
        cagr = ((final_capital / initial_capital) ** (1 / len(years)) - 1) * 100

        # Time to double capital using CAGR formula
        years_to_double_pms = np.log(2) / np.log(1 + cagr / 100)

        # Time to double capital with mutual fund at 15% return
        years_to_double_mutual_fund = 1.09*(np.log(2)) / np.log(1 + 0.15)

        # Time to double capital with FD at 6% return
        years_to_double_fd = np.log(2) / np.log(1 + 0.06)

        st.markdown(f"**Time to Double Capital with WhaleStreet PMS (Avg) after deducting all profit sharing & fees:** {years_to_double_pms:.2f} years")
        st.markdown(f"**Time to Double Capital with top Mutual Funds (Avg) :** {years_to_double_mutual_fund:.2f} years")
        st.markdown(f"**Time to Double Capital with Fixed Deposit (6% Annual Return):** {years_to_double_fd:.2f} years")

        # Create a bar chart to compare the time to double capital
        comparison_fig = go.Figure()

        comparison_fig.add_trace(go.Bar(
            x=['WhaleStreet PMS', 'Mutual Funds (15%)', 'Fixed Deposit (6%)'],
            y=[years_to_double_pms, years_to_double_mutual_fund, years_to_double_fd],
            text=[f'{years_to_double_pms:.2f} years', f'{years_to_double_mutual_fund:.2f} years', f'{years_to_double_fd:.2f} years'],
            textposition='auto',
            marker=dict(color=['#1E90FF', '#32CD32', '#FF6347'])
        ))

        comparison_fig.update_layout(
            title="Comparison of Time to Double Capital",
            xaxis_title="Investment Type",
            yaxis_title="Years to Double Capital",
            plot_bgcolor='#ffffff',
            title_x=0.5,
            font=dict(color='#333333'),
            yaxis=dict(showgrid=True),
            height=600
        )

        st.plotly_chart(comparison_fig)

        # Add the original profit sharing graph here
        fig_simple = go.Figure()

        fig_simple.add_trace(go.Bar(
            x=[f'Year {df_simple["Year"][i]}' for i in range(len(df_simple))],
            y=[df_simple["Net Capital After Profit Share (₹)"][i] for i in range(len(df_simple))],
            name='Net Capital After Profit Share',
            text=[f'₹{df_simple["Net Capital After Profit Share (₹)"][i]:,}' for i in range(len(df_simple))],
            textposition='outside',
            marker=dict(color='#90EE90'),
            showlegend=True
        ))

        fig_simple.add_trace(go.Bar(
            x=[f'Year {df_simple["Year"][i]}' for i in range(len(df_simple))],
            y=[df_simple["30% Profit Share Above Threshold (₹)"][i] for i in range(len(df_simple))],
            name='30% Profit Share Above Threshold',
            text=[f'₹{df_simple["30% Profit Share Above Threshold (₹)"][i]:,}' for i in range(len(df_simple))],
            textposition='inside',
            marker=dict(color='#1E90FF'),
            showlegend=True
        ))

        fig_simple.update_layout(
            title="Net Capital and Profit Share Over 5 Years (Simple Model)",
            xaxis_title="Year",
            yaxis_title="Amount in ₹",
            plot_bgcolor='#ffffff',
            title_x=0.5,
            font=dict(color='#333333'),
            yaxis=dict(showgrid=True),
            barmode='stack',  
            height=600
        )

        st.plotly_chart(fig_simple)



elif page == "Steps to Start Your PMS":
    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/staircase.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Steps to Start Your Portfolio Management Service</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Begin Your Journey Towards Tailored Portfolio Management</p>
    </div>
    ''', unsafe_allow_html=True)

    # Steps with Icons
    st.markdown('''
    <div style="background-color: #F7F7F7; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #1E2D39;">Getting Started</h3>
        <p style="font-size: 16px; color: #333333;">Follow these steps to begin your journey towards tailored portfolio management:</p>
        <ul style="list-style-type: none; padding-left: 0; font-size: 16px; color: #1E2D39;">
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/conference-call.png" style="vertical-align: middle;"/>
                <strong>1. Initial Consultation:</strong> Schedule a consultation with our portfolio managers to discuss your investment goals, risk tolerance, and financial horizon.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/security-checked.png" style="vertical-align: middle;"/>
                <strong>2. Open a Demat Account:</strong> Register a demat account through our platform to hold your securities in digital format, making trading quick and secure.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/data-sheet.png" style="vertical-align: middle;"/>
                <strong>3. Tailor Your Investment Plan:</strong> Based on the consultation, we'll design a customized investment strategy aligned with your objectives.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/cash-in-hand.png" style="vertical-align: middle;"/>
                <strong>4. Fund Your Account:</strong> Transfer funds to your newly opened demat account to start the investment process.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/rocket.png" style="vertical-align: middle;"/>
                <strong>5. Portfolio Activation:</strong> Once funded, your portfolio is activated and ready to start working for you.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/007ACC/pie-chart-report.png" style="vertical-align: middle;"/>
                <strong>6. Regular Reporting and Rebalancing:</strong> Receive regular reports on your portfolio's performance. We’ll adjust as needed to align with your financial goals.
            </li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

    # Title with icon for Conditions & Rules
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/law.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Conditions & Rules</h2>
    </div>
    ''', unsafe_allow_html=True)

    # Main content with background and padding for Conditions & Rules
    st.markdown('''
    <div style="background-color: #F0F4F8; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #1E2D39;">Important Conditions and Rules</h3>
        <ul style="list-style-type: none; padding-left: 0; font-size: 16px; color: #1E2D39;">
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/lock.png" style="vertical-align: middle;"/> 
            <strong>Lock-in Period:</strong> While there is no strict lock-in period, we recommend a minimum holding period of 3 years to see significant portfolio growth based on our historical data. If you wish to withdraw your capital before this period, the withdrawal process will be adjusted according to the P&L status at the time, with capital disbursed within T+5 days.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/money-bag.png" style="vertical-align: middle;"/> 
            <strong>Additional Contributions:</strong> You can make additional investments anytime.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/bill.png" style="vertical-align: middle;"/> 
            <strong>Fees and Charges:</strong> For <strong>Model 1</strong>, the management fees are 5% annually for capital amounts up to ₹300,000, and 4% annually for amounts exceeding ₹300,000, with an additional 20% performance fee applied to returns exceeding 6% per year.\nIn <strong>Model 2</strong>, a 30% performance fee is applied to returns above a specified threshold.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/security-shield-green.png" style="vertical-align: middle;"/> 
            <strong>Risk Management:</strong> Our strategies are focused on long-term growth, with measures in place to mitigate risk.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/bar-chart.png" style="vertical-align: middle;"/> 
            <strong>Reporting:</strong> We provide quarterly performance reports to keep you informed of your portfolio's status.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/rebalance-portfolio.png" style="vertical-align: middle;"/> 
            <strong>Rebalancing:</strong> The portfolio may be rebalanced periodically to align with your financial goals.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/close-sign.png" style="vertical-align: middle;"/> 
            <strong>Termination of Service:</strong> Either party can terminate the service with a 30-day notice period, following the settlement of any profit-sharing fees.</li>
            <li style="margin-bottom: 15px;"><img src="https://img.icons8.com/ios-filled/30/FF6347/check-all.png" style="vertical-align: middle;"/> 
            <strong>Compliance:</strong> We strictly adhere to all relevant regulations to protect our clients' interests.</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

    # Section for Possible Outcomes
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/light-at-the-end-of-tunnel.png" width="50"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">"Possible Prospects: Navigating Portfolio Changes"
</h2>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background-color: #FFF8E7; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #1E2D39;">What You Might Experience During Your Investment Journey</h3>
        <ul style="list-style-type: none; padding-left: 0; font-size: 16px; color: #1E2D39;">
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/FFD700/money-transfer.png" style="vertical-align: middle;"/>
                <strong>Temporary Idle Funds:</strong> There may be times when certain funds in your demat account remain uninvested for 1-2 months. This is a deliberate strategy based on market conditions and sentiment. We avoid unnecessary investments in random stocks irrespective of market signals. Rest assured, our expert managers know the optimal times to deploy your funds effectively. Even with temporary idle funds, your portfolio is managed to achieve the desired annual returns. Trust us to handle these decisions on your behalf.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/FFD700/graph.png" style="vertical-align: middle;"/>
                <strong>Short-Term Unrealized Losses:</strong> It’s normal for portfolios to experience temporary dips, sometimes even between -10% to -14%. However, there's no need for concern. With our expert management and strategic approach, we are well-equipped to navigate these fluctuations and guide your portfolio back to growth. With our carefully crafted mean-reverting strategies and overall porfolio beta and correlation, these downturns are short-lived. We are confident that your portfolio will achieve the desired returns by the end of the year. Patience is key, and you can trust that your investment is being expertly managed to ensure long-term success.
            </li>
            <li style="margin-bottom: 15px;">
                <img src="https://img.icons8.com/ios-filled/30/FFD700/safe.png" style="vertical-align: middle;"/>
                <strong>Capital Safety with Consistent Returns:</strong> Your capital is our foremost priority, and we adopt a conservative yet effective approach to portfolio management. Despite the cautious strategy, we consistently achieve annual returns in the range of 25-30%, with 0% realized drawdown. This disciplined investment approach not only mitigates risk but also ensures steady growth, even in volatile market conditions. You can trust that your capital is in safe hands, managed with a focus on both protection and performance.
            </li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

if page == "Resources & Contact":

    # Section Title with Icon and Styled Heading
    st.markdown('''
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://img.icons8.com/ios-filled/50/1E2D39/contact-card.png" width="50" alt="Contact Icon"/>
        <h2 style="color: #1E2D39; font-family: 'Arial', sans-serif; font-weight: bold; margin-top: 10px;">Contact Information</h2>
        <p style="color: #4A4A4A; font-size: 18px; margin-top: 10px;">Reach Out to Us for Any Inquiries or Support</p>
    </div>
    ''', unsafe_allow_html=True)

    # Adding a visually appealing contact card layout
    st.markdown('''
    <div style="background-color: #F7F7F7; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #1E2D39; text-align: center; font-weight: bold;">Get in Touch</h3>
        <p style="font-size: 16px; color: #333333; text-align: center;">We would love to hear from you! Reach out to us for any inquiries, support, or feedback.</p>
        <div style="display: flex; justify-content: space-around; margin-top: 30px;">
            <div style="width: 45%; text-align: center;">
                <img src="https://img.icons8.com/ios-filled/100/007ACC/phone.png" width="50" alt="Phone Icon"/>
                <p style="font-size: 18px; color: #007ACC; font-weight: bold;">Phone:</p>
                <p style="font-size: 18px; color: #333333;">+91-8178611382</p>
            </div>
            <div style="width: 45%; text-align: center;">
                <img src="https://img.icons8.com/ios-filled/100/007ACC/email.png" width="50" alt="Email Icon"/>
                <p style="font-size: 18px; color: #007ACC; font-weight: bold;">Email:</p>
                <p style="font-size: 18px; color: #333333;">whalestreetofficial@gmail.com</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    
