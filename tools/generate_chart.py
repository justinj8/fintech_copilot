
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("data/fintech_product_data.csv", parse_dates=["account_created_at", "feature_used_at"])

# Set style for better-looking charts
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def smart_visualize(data_description):
    """
    Create intelligent visualizations based on data analysis context.
    Input should be a description of what to visualize.
    """
    try:
        # Parse the data description to determine best visualization
        description_lower = data_description.lower()

        # Determine chart type and data based on description
        if 'churn' in description_lower:
            return create_churn_visualizations(data_description)
        elif 'revenue' in description_lower:
            return create_revenue_visualizations(data_description)
        elif 'spending' in description_lower:
            return create_spending_visualizations(data_description)
        elif 'feature' in description_lower:
            return create_feature_visualizations(data_description)
        elif 'trend' in description_lower or 'time' in description_lower:
            return create_trend_visualizations(data_description)
        elif 'comparison' in description_lower or 'compare' in description_lower:
            return create_comparison_visualizations(data_description)
        else:
            # Default to overview dashboard
            return create_overview_dashboard()

    except Exception as e:
        return f"Visualization failed: {e}. Try describing what you'd like to see visualized."

def create_churn_visualizations(description):
    """Create churn-focused visualizations."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Churn Analysis Dashboard', fontsize=16, fontweight='bold')

    # 1. Churn rate by tier
    churn_by_tier = df.groupby('account_tier')['churned'].mean()
    ax1.bar(churn_by_tier.index, churn_by_tier.values, color=sns.color_palette("viridis", len(churn_by_tier)))
    ax1.set_title('Churn Rate by Account Tier')
    ax1.set_ylabel('Churn Rate')
    ax1.tick_params(axis='x', rotation=45)

    # 2. Churn rate by segment
    churn_by_segment = df.groupby('customer_segment')['churned'].mean()
    ax2.bar(churn_by_segment.index, churn_by_segment.values, color=sns.color_palette("plasma", len(churn_by_segment)))
    ax2.set_title('Churn Rate by Customer Segment')
    ax2.set_ylabel('Churn Rate')
    ax2.tick_params(axis='x', rotation=45)

    # 3. Spending distribution: churned vs retained
    churned_spend = df[df['churned'] == True]['monthly_spend']
    retained_spend = df[df['churned'] == False]['monthly_spend']
    ax3.hist([retained_spend, churned_spend], bins=20, alpha=0.7, label=['Retained', 'Churned'], color=['green', 'red'])
    ax3.set_title('Monthly Spend Distribution: Churned vs Retained')
    ax3.set_xlabel('Monthly Spend ($)')
    ax3.set_ylabel('Count')
    ax3.legend()

    # 4. Feature usage and churn
    feature_churn = df.groupby('product_feature_used')['churned'].mean().fillna(0)
    ax4.barh(range(len(feature_churn)), feature_churn.values, color=sns.color_palette("coolwarm", len(feature_churn)))
    ax4.set_yticks(range(len(feature_churn)))
    ax4.set_yticklabels(feature_churn.index)
    ax4.set_title('Churn Rate by Feature Usage')
    ax4.set_xlabel('Churn Rate')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_revenue_visualizations(description):
    """Create revenue-focused visualizations."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Revenue Analysis Dashboard', fontsize=16, fontweight='bold')

    # 1. Revenue by tier
    revenue_by_tier = df.groupby('account_tier')['monthly_revenue'].sum()
    ax1.pie(revenue_by_tier.values, labels=revenue_by_tier.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Total Revenue Distribution by Tier')

    # 2. Average revenue per customer by segment
    avg_revenue_segment = df.groupby('customer_segment')['monthly_revenue'].mean()
    ax2.bar(avg_revenue_segment.index, avg_revenue_segment.values, color=sns.color_palette("viridis", len(avg_revenue_segment)))
    ax2.set_title('Average Revenue per Customer by Segment')
    ax2.set_ylabel('Average Revenue ($)')
    ax2.tick_params(axis='x', rotation=45)

    # 3. Revenue vs Spending scatter
    ax3.scatter(df['monthly_spend'], df['monthly_revenue'], alpha=0.6, c=df['account_tier'].map({'Free': 0, 'Plus': 1, 'Premium': 2}), cmap='viridis')
    ax3.set_xlabel('Monthly Spend ($)')
    ax3.set_ylabel('Monthly Revenue ($)')
    ax3.set_title('Revenue vs Spending Relationship')

    # 4. Revenue by feature usage
    feature_revenue = df.groupby('product_feature_used')['monthly_revenue'].sum().fillna(0)
    ax4.barh(range(len(feature_revenue)), feature_revenue.values, color=sns.color_palette("plasma", len(feature_revenue)))
    ax4.set_yticks(range(len(feature_revenue)))
    ax4.set_yticklabels(feature_revenue.index)
    ax4.set_title('Total Revenue by Feature')
    ax4.set_xlabel('Total Revenue ($)')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_spending_visualizations(description):
    """Create spending-focused visualizations."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Spending Analysis Dashboard', fontsize=16, fontweight='bold')

    # 1. Spending distribution by tier
    for tier in df['account_tier'].unique():
        tier_data = df[df['account_tier'] == tier]['monthly_spend']
        ax1.hist(tier_data, alpha=0.6, label=tier, bins=20)
    ax1.set_title('Spending Distribution by Tier')
    ax1.set_xlabel('Monthly Spend ($)')
    ax1.set_ylabel('Count')
    ax1.legend()

    # 2. Average spending by segment
    avg_spend_segment = df.groupby('customer_segment')['monthly_spend'].mean()
    ax2.bar(avg_spend_segment.index, avg_spend_segment.values, color=sns.color_palette("coolwarm", len(avg_spend_segment)))
    ax2.set_title('Average Spending by Customer Segment')
    ax2.set_ylabel('Average Spend ($)')
    ax2.tick_params(axis='x', rotation=45)

    # 3. Spending vs Transactions
    ax3.scatter(df['transactions_count'], df['monthly_spend'], alpha=0.6, c=df['customer_segment'].map({'Student': 0, 'Professional': 1, 'Retired': 2}), cmap='Set1')
    ax3.set_xlabel('Transaction Count')
    ax3.set_ylabel('Monthly Spend ($)')
    ax3.set_title('Spending vs Transaction Count')

    # 4. Top spenders by tier (boxplot)
    sns.boxplot(data=df, x='account_tier', y='monthly_spend', ax=ax4)
    ax4.set_title('Spending Distribution by Tier (Boxplot)')
    ax4.set_ylabel('Monthly Spend ($)')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_feature_visualizations(description):
    """Create feature usage visualizations."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Feature Usage Analysis', fontsize=16, fontweight='bold')

    # 1. Feature popularity
    feature_counts = df['product_feature_used'].value_counts()
    ax1.pie(feature_counts.values, labels=feature_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Feature Usage Distribution')

    # 2. Feature usage by tier
    feature_tier = pd.crosstab(df['product_feature_used'], df['account_tier'])
    feature_tier.plot(kind='bar', stacked=True, ax=ax2, color=sns.color_palette("viridis", 3))
    ax2.set_title('Feature Usage by Account Tier')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='Account Tier')

    # 3. Average revenue by feature
    feature_revenue = df.groupby('product_feature_used')['monthly_revenue'].mean()
    ax3.bar(range(len(feature_revenue)), feature_revenue.values, color=sns.color_palette("plasma", len(feature_revenue)))
    ax3.set_xticks(range(len(feature_revenue)))
    ax3.set_xticklabels(feature_revenue.index, rotation=45)
    ax3.set_title('Average Revenue by Feature')
    ax3.set_ylabel('Average Revenue ($)')

    # 4. Feature vs Spending correlation
    feature_spend = df.groupby('product_feature_used')['monthly_spend'].mean()
    ax4.barh(range(len(feature_spend)), feature_spend.values, color=sns.color_palette("coolwarm", len(feature_spend)))
    ax4.set_yticks(range(len(feature_spend)))
    ax4.set_yticklabels(feature_spend.index)
    ax4.set_title('Average Spending by Feature')
    ax4.set_xlabel('Average Spend ($)')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_trend_visualizations(description):
    """Create trend and time-based visualizations."""
    df['month_year'] = df['account_created_at'].dt.to_period('M')

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Trends and Time Analysis', fontsize=16, fontweight='bold')

    # 1. Customer signups over time
    monthly_signups = df.groupby('month_year').size()
    ax1.plot(range(len(monthly_signups)), monthly_signups.values, marker='o', linewidth=2)
    ax1.set_title('Customer Signups Over Time')
    ax1.set_ylabel('New Customers')
    ax1.set_xlabel('Month')
    ax1.grid(True, alpha=0.3)

    # 2. Revenue trends by tier
    revenue_trends = df.groupby(['month_year', 'account_tier'])['monthly_revenue'].sum().unstack(fill_value=0)
    for tier in revenue_trends.columns:
        ax2.plot(range(len(revenue_trends)), revenue_trends[tier], marker='o', label=tier, linewidth=2)
    ax2.set_title('Revenue Trends by Tier')
    ax2.set_ylabel('Revenue ($)')
    ax2.set_xlabel('Month')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Churn rate trends
    churn_trends = df.groupby('month_year')['churned'].mean()
    ax3.plot(range(len(churn_trends)), churn_trends.values, marker='o', color='red', linewidth=2)
    ax3.set_title('Churn Rate Trends')
    ax3.set_ylabel('Churn Rate')
    ax3.set_xlabel('Month')
    ax3.grid(True, alpha=0.3)

    # 4. Feature adoption over time
    feature_time = df.groupby(['month_year', 'product_feature_used']).size().unstack(fill_value=0)
    feature_time.plot(kind='area', stacked=True, ax=ax4, alpha=0.7)
    ax4.set_title('Feature Adoption Over Time')
    ax4.set_ylabel('Usage Count')
    ax4.set_xlabel('Month')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_comparison_visualizations(description):
    """Create comparison-focused visualizations."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Comparative Analysis Dashboard', fontsize=16, fontweight='bold')

    # 1. Tier comparison heatmap
    tier_metrics = df.groupby('account_tier').agg({
        'monthly_spend': 'mean',
        'monthly_revenue': 'mean',
        'churned': 'mean',
        'transactions_count': 'mean'
    }).round(2)

    im1 = ax1.imshow(tier_metrics.T, cmap='viridis', aspect='auto')
    ax1.set_xticks(range(len(tier_metrics.index)))
    ax1.set_xticklabels(tier_metrics.index)
    ax1.set_yticks(range(len(tier_metrics.columns)))
    ax1.set_yticklabels(tier_metrics.columns)
    ax1.set_title('Tier Metrics Heatmap')
    plt.colorbar(im1, ax=ax1)

    # 2. Segment comparison
    segment_metrics = df.groupby('customer_segment').agg({
        'monthly_spend': 'mean',
        'monthly_revenue': 'mean',
        'churned': 'mean'
    })

    x = np.arange(len(segment_metrics.index))
    width = 0.25
    ax2.bar(x - width, segment_metrics['monthly_spend'], width, label='Avg Spend', alpha=0.8)
    ax2.bar(x, segment_metrics['monthly_revenue'], width, label='Avg Revenue', alpha=0.8)
    ax2.bar(x + width, segment_metrics['churned'] * 1000, width, label='Churn Rate (x1000)', alpha=0.8)
    ax2.set_xlabel('Customer Segment')
    ax2.set_xticks(x)
    ax2.set_xticklabels(segment_metrics.index)
    ax2.set_title('Segment Metrics Comparison')
    ax2.legend()

    # 3. Card type performance
    card_performance = df.groupby('card_type').agg({
        'monthly_spend': 'mean',
        'monthly_revenue': 'mean'
    })

    ax3.scatter(card_performance['monthly_spend'], card_performance['monthly_revenue'],
               s=200, alpha=0.7, c=['red', 'blue', 'green'])
    for i, txt in enumerate(card_performance.index):
        ax3.annotate(txt, (card_performance['monthly_spend'].iloc[i], card_performance['monthly_revenue'].iloc[i]))
    ax3.set_xlabel('Average Monthly Spend')
    ax3.set_ylabel('Average Monthly Revenue')
    ax3.set_title('Card Type Performance Matrix')

    # 4. Feature vs Tier matrix
    feature_tier_matrix = pd.crosstab(df['product_feature_used'], df['account_tier'], normalize='columns')
    im4 = ax4.imshow(feature_tier_matrix.values, cmap='Blues', aspect='auto')
    ax4.set_xticks(range(len(feature_tier_matrix.columns)))
    ax4.set_xticklabels(feature_tier_matrix.columns)
    ax4.set_yticks(range(len(feature_tier_matrix.index)))
    ax4.set_yticklabels(feature_tier_matrix.index)
    ax4.set_title('Feature Usage by Tier (Normalized)')
    plt.colorbar(im4, ax=ax4)

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

def create_overview_dashboard():
    """Create a comprehensive overview dashboard."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Fintech Business Overview Dashboard', fontsize=16, fontweight='bold')

    # 1. Customer distribution by tier
    tier_counts = df['account_tier'].value_counts()
    ax1.pie(tier_counts.values, labels=tier_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Customer Distribution by Tier')

    # 2. Revenue and spend correlation
    ax2.scatter(df['monthly_spend'], df['monthly_revenue'], alpha=0.6, c=df['churned'].map({False: 'green', True: 'red'}))
    ax2.set_xlabel('Monthly Spend ($)')
    ax2.set_ylabel('Monthly Revenue ($)')
    ax2.set_title('Revenue vs Spend (Red=Churned)')

    # 3. Key metrics by segment
    segment_summary = df.groupby('customer_segment').agg({
        'monthly_spend': 'mean',
        'churned': 'mean'
    })

    x = np.arange(len(segment_summary.index))
    ax3.bar(x, segment_summary['monthly_spend'], alpha=0.7, label='Avg Spend')
    ax3_twin = ax3.twinx()
    ax3_twin.plot(x, segment_summary['churned'], color='red', marker='o', linewidth=3, label='Churn Rate')
    ax3.set_xlabel('Customer Segment')
    ax3.set_xticks(x)
    ax3.set_xticklabels(segment_summary.index)
    ax3.set_ylabel('Average Spend ($)', color='blue')
    ax3_twin.set_ylabel('Churn Rate', color='red')
    ax3.set_title('Spending and Churn by Segment')

    # 4. Account status overview
    status_counts = df['account_status'].value_counts()
    ax4.bar(status_counts.index, status_counts.values, color=['green', 'orange', 'red'])
    ax4.set_title('Account Status Distribution')
    ax4.set_ylabel('Count')

    plt.tight_layout()
    plt.savefig('chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    return "chart.png"

# Legacy function for backwards compatibility
def generate_chart(x_col, y_col, chart_type="bar"):
    """Legacy chart generation function."""
    try:
        plt.figure(figsize=(12, 8))
        if chart_type == "bar":
            if df[x_col].dtype == 'object':
                data_agg = df.groupby(x_col)[y_col].mean()
                plt.bar(data_agg.index, data_agg.values, color=sns.color_palette("viridis", len(data_agg)))
            else:
                sns.barplot(data=df, x=x_col, y=y_col)
        elif chart_type == "line":
            sns.lineplot(data=df, x=x_col, y=y_col, marker='o')
        elif chart_type == "scatter":
            sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.6)
        elif chart_type == "hist":
            sns.histplot(data=df, x=x_col, bins=20)
        elif chart_type == "box":
            sns.boxplot(data=df, x=x_col, y=y_col)

        plt.title(f"{chart_type.title()} Chart: {y_col} by {x_col}", fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        return "chart.png"
    except Exception as e:
        return f"Chart generation failed: {e}"
