import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

df = pd.read_csv("data/fintech_product_data.csv", parse_dates=["account_created_at", "feature_used_at"])

def query_dataframe(query):
    """
    Intelligently query the fintech dataset with enhanced natural language understanding.
    """
    query_lower = query.lower()

    # Enhanced pattern matching for common business questions
    patterns = {
        'churn': handle_churn_analysis,
        'revenue': handle_revenue_analysis,
        'spending': handle_spending_analysis,
        'feature': handle_feature_analysis,
        'customer': handle_customer_analysis,
        'tier': handle_tier_analysis,
        'segment': handle_segment_analysis,
        'trend': handle_trend_analysis,
        'compare': handle_comparison_analysis
    }

    # Find the best matching pattern
    for pattern, handler in patterns.items():
        if pattern in query_lower:
            try:
                return handler(query, query_lower)
            except Exception as e:
                continue

    # Try direct pandas operations
    try:
        if query.startswith('df.'):
            result = eval(query)
            if hasattr(result, 'to_markdown'):
                return result.head(15).to_markdown()
            else:
                return str(result)
        else:
            result = df.query(query)
            return result.head(15).to_markdown()
    except Exception as e:
        return get_helpful_error_message(e, query)

def handle_churn_analysis(query, query_lower):
    """Handle churn-related queries."""
    if 'tier' in query_lower or 'account_tier' in query_lower:
        result = df.groupby('account_tier')['churned'].agg(['count', 'sum', 'mean']).round(3)
        result.columns = ['total_customers', 'churned_customers', 'churn_rate']
        summary = f"Overall churn rate: {df['churned'].mean():.1%}\n\n"
        return summary + f"Churn Rate by Account Tier:\n{result.to_markdown()}"

    elif 'segment' in query_lower:
        result = df.groupby('customer_segment')['churned'].agg(['count', 'sum', 'mean']).round(3)
        result.columns = ['total_customers', 'churned_customers', 'churn_rate']
        return f"Churn Rate by Customer Segment:\n{result.to_markdown()}"

    elif 'feature' in query_lower:
        feature_churn = df.groupby('product_feature_used')['churned'].agg(['count', 'sum', 'mean']).round(3)
        feature_churn.columns = ['total_customers', 'churned_customers', 'churn_rate']
        return f"Churn Rate by Feature Usage:\n{feature_churn.to_markdown()}"

    else:
        # General churn analysis
        overall_churn = df['churned'].mean()
        by_tier = df.groupby('account_tier')['churned'].mean().round(3)
        by_segment = df.groupby('customer_segment')['churned'].mean().round(3)

        result = f"Overall Churn Rate: {overall_churn:.1%}\n\n"
        result += f"By Tier:\n{by_tier.to_markdown()}\n\n"
        result += f"By Segment:\n{by_segment.to_markdown()}"
        return result

def handle_revenue_analysis(query, query_lower):
    """Handle revenue-related queries."""
    if 'tier' in query_lower:
        result = df.groupby('account_tier')['monthly_revenue'].agg(['count', 'sum', 'mean', 'median']).round(2)
        result.columns = ['customers', 'total_revenue', 'avg_revenue', 'median_revenue']
        return f"Revenue Analysis by Tier:\n{result.to_markdown()}"

    elif 'segment' in query_lower:
        result = df.groupby('customer_segment')['monthly_revenue'].agg(['count', 'sum', 'mean', 'median']).round(2)
        result.columns = ['customers', 'total_revenue', 'avg_revenue', 'median_revenue']
        return f"Revenue Analysis by Segment:\n{result.to_markdown()}"

    else:
        total_revenue = df['monthly_revenue'].sum()
        avg_revenue = df['monthly_revenue'].mean()
        revenue_by_tier = df.groupby('account_tier')['monthly_revenue'].sum().round(2)

        result = f"Total Revenue: ${total_revenue:,.2f}\n"
        result += f"Average Revenue per Customer: ${avg_revenue:.2f}\n\n"
        result += f"Revenue by Tier:\n{revenue_by_tier.to_markdown()}"
        return result

def handle_spending_analysis(query, query_lower):
    """Handle spending pattern queries."""
    if 'tier' in query_lower:
        result = df.groupby('account_tier')['monthly_spend'].agg(['count', 'sum', 'mean', 'median']).round(2)
        result.columns = ['customers', 'total_spend', 'avg_spend', 'median_spend']
        return f"Spending Analysis by Tier:\n{result.to_markdown()}"

    elif 'segment' in query_lower:
        result = df.groupby('customer_segment')['monthly_spend'].agg(['count', 'sum', 'mean', 'median']).round(2)
        result.columns = ['customers', 'total_spend', 'avg_spend', 'median_spend']
        return f"Spending Analysis by Segment:\n{result.to_markdown()}"

    else:
        avg_spend = df['monthly_spend'].mean()
        median_spend = df['monthly_spend'].median()
        spend_by_tier = df.groupby('account_tier')['monthly_spend'].mean().round(2)

        result = f"Average Monthly Spend: ${avg_spend:.2f}\n"
        result += f"Median Monthly Spend: ${median_spend:.2f}\n\n"
        result += f"Average Spend by Tier:\n{spend_by_tier.to_markdown()}"
        return result

def handle_feature_analysis(query, query_lower):
    """Handle feature usage queries."""
    feature_usage = df['product_feature_used'].value_counts()
    feature_revenue = df.groupby('product_feature_used')['monthly_revenue'].mean().round(2)

    result = f"Feature Usage Count:\n{feature_usage.to_markdown()}\n\n"
    result += f"Average Revenue by Feature:\n{feature_revenue.to_markdown()}"
    return result

def handle_customer_analysis(query, query_lower):
    """Handle customer behavior queries."""
    if 'active' in query_lower:
        active_customers = df[df['account_status'] == 'Active'].shape[0]
        total_customers = df.shape[0]
        active_rate = active_customers / total_customers
        return f"Active Customers: {active_customers:,} out of {total_customers:,} ({active_rate:.1%})"

    else:
        status_counts = df['account_status'].value_counts()
        tier_counts = df['account_tier'].value_counts()

        result = f"Customer Status Distribution:\n{status_counts.to_markdown()}\n\n"
        result += f"Tier Distribution:\n{tier_counts.to_markdown()}"
        return result

def handle_tier_analysis(query, query_lower):
    """Handle tier-specific analysis."""
    tier_summary = df.groupby('account_tier').agg({
        'customer_id': 'count',
        'monthly_spend': 'mean',
        'monthly_revenue': 'mean',
        'churned': 'mean',
        'transactions_count': 'mean'
    }).round(2)

    tier_summary.columns = ['customers', 'avg_spend', 'avg_revenue', 'churn_rate', 'avg_transactions']
    return f"Comprehensive Tier Analysis:\n{tier_summary.to_markdown()}"

def handle_segment_analysis(query, query_lower):
    """Handle customer segment analysis."""
    segment_summary = df.groupby('customer_segment').agg({
        'customer_id': 'count',
        'monthly_spend': 'mean',
        'monthly_revenue': 'mean',
        'churned': 'mean',
        'transactions_count': 'mean'
    }).round(2)

    segment_summary.columns = ['customers', 'avg_spend', 'avg_revenue', 'churn_rate', 'avg_transactions']
    return f"Customer Segment Analysis:\n{segment_summary.to_markdown()}"

def handle_trend_analysis(query, query_lower):
    """Handle trend and time-based queries."""
    # Create month-year from account_created_at for trend analysis
    df['month_year'] = df['account_created_at'].dt.to_period('M')
    monthly_signups = df.groupby('month_year').size()

    return f"Monthly Customer Signups Trend:\n{monthly_signups.tail(12).to_markdown()}"

def handle_comparison_analysis(query, query_lower):
    """Handle comparison queries."""
    if 'tier' in query_lower:
        return handle_tier_analysis(query, query_lower)
    elif 'segment' in query_lower:
        return handle_segment_analysis(query, query_lower)
    else:
        # Compare key metrics across different dimensions
        comparison = df.groupby(['account_tier', 'customer_segment']).agg({
            'monthly_spend': 'mean',
            'monthly_revenue': 'mean',
            'churned': 'mean'
        }).round(2)

        return f"Tier vs Segment Comparison:\n{comparison.to_markdown()}"

def get_helpful_error_message(error, query):
    """Provide helpful error messages and suggestions."""
    suggestions = [
        "Try: 'churn rate by tier'",
        "Try: 'revenue analysis by segment'",
        "Try: 'spending patterns'",
        "Try: 'feature usage analysis'",
        "Try: 'customer tier comparison'",
        "Try: 'monthly trends'"
    ]

    return f"Dataset Overview:\n" \
           f"- Total customers: {df.shape[0]:,}\n" \
           f"- Available columns: {', '.join(df.columns)}\n" \
           f"- Date range: {df['account_created_at'].min().strftime('%Y-%m-%d')} to {df['account_created_at'].max().strftime('%Y-%m-%d')}\n\n" \
           f"Query failed: {error}\n\n" \
           f"Suggestions:\n" + "\n".join(suggestions)