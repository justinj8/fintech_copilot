import pandas as pd

df = pd.read_csv("data/fintech_product_data.csv", parse_dates=["account_created_at", "feature_used_at"])

def query_dataframe(query):
    """
    Query the fintech dataset. Available columns:
    - customer_id: unique customer identifier
    - account_created_at: when account was created (datetime)
    - account_status: Active, Suspended, Closed
    - kyc_completed: True/False
    - card_activated: True/False
    - card_type: Credit, Debit, Virtual
    - monthly_spend: spending amount
    - transactions_count: number of transactions
    - product_feature_used: CryptoRewards, RoundUps, DirectDeposit, BillPay, SavingsVault
    - feature_used_at: when feature was used (datetime)
    - account_tier: Free, Plus, Premium
    - decline_rate: transaction decline rate
    - customer_segment: Student, Professional, Retired
    - monthly_revenue: revenue from customer
    - churned: True/False if customer churned

    For churn rate by tier example: use groupby operations or pandas syntax like:
    - df.groupby('account_tier')['churned'].mean() for churn rates
    - df[df['account_tier'] == 'Premium'] for filtering
    """

    # Handle common analytical queries with pandas operations
    query_lower = query.lower()

    if 'churn rate by tier' in query_lower or 'churn by tier' in query_lower:
        result = df.groupby('account_tier')['churned'].agg(['count', 'sum', 'mean']).round(3)
        result.columns = ['total_customers', 'churned_customers', 'churn_rate']
        return f"Churn Rate by Account Tier:\n{result.to_markdown()}"

    if 'churn rate' in query_lower and 'segment' in query_lower:
        result = df.groupby('customer_segment')['churned'].agg(['count', 'sum', 'mean']).round(3)
        result.columns = ['total_customers', 'churned_customers', 'churn_rate']
        return f"Churn Rate by Customer Segment:\n{result.to_markdown()}"

    # Try direct pandas query syntax
    try:
        if query.startswith('df.'):
            result = eval(query)
            if hasattr(result, 'to_markdown'):
                return result.head(10).to_markdown()
            else:
                return str(result)
        else:
            result = df.query(query)
            return result.head(10).to_markdown()
    except Exception as e:
        return f"Dataset info:\nColumns: {list(df.columns)}\nShape: {df.shape}\nQuery failed: {e}\n\nTry queries like:\n- account_tier == 'Premium'\n- monthly_spend > 1000\n- churned == True\n- df.groupby('account_tier')['churned'].mean()"
