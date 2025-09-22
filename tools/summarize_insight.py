
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

INSIGHT_TEMPLATE = """
You are a senior fintech business analyst and data scientist. Analyze the following data and provide comprehensive business insights.

Data Analysis:
{data_analysis}

Context: This is from a fintech company with multiple account tiers (Free, Plus, Premium), customer segments (Student, Professional, Retired), and various product features.

Provide a structured analysis with:

1. **Executive Summary** (2-3 sentences)
   - Key finding and business impact

2. **Critical Insights** (3-4 bullet points)
   - Data-driven observations
   - Business implications
   - Potential risks or opportunities

3. **Strategic Recommendations** (2-3 actionable items)
   - Specific actions based on data
   - Expected business outcomes

4. **Metrics to Monitor**
   - KPIs that need attention
   - Success indicators

Focus on actionable insights that drive revenue growth, reduce churn, and improve customer experience.
"""

COMPARATIVE_TEMPLATE = """
You are a fintech business strategist. Compare the following data points and provide strategic insights.

Comparison Data:
{data_analysis}

Provide:
1. **Key Differences**: What stands out in the comparison?
2. **Performance Leaders**: Which segments/tiers perform best?
3. **Improvement Opportunities**: Where are the gaps?
4. **Strategic Actions**: What should the business do?

Focus on competitive advantages and growth opportunities.
"""

TREND_TEMPLATE = """
You are a fintech growth analyst. Analyze the following trend data and provide forward-looking insights.

Trend Analysis:
{data_analysis}

Provide:
1. **Trend Summary**: What patterns do you see?
2. **Growth Drivers**: What's driving positive trends?
3. **Risk Factors**: What concerning trends exist?
4. **Forecasting**: What might happen next?
5. **Action Plan**: How to capitalize on trends?

Focus on sustainable growth and risk mitigation.
"""

def generate_insights(data_analysis):
    """Generate comprehensive business insights from data analysis."""
    analysis_lower = data_analysis.lower()

    # Choose appropriate template based on analysis type
    if 'comparison' in analysis_lower or 'vs' in analysis_lower or 'compare' in analysis_lower:
        template = COMPARATIVE_TEMPLATE
    elif 'trend' in analysis_lower or 'over time' in analysis_lower or 'monthly' in analysis_lower:
        template = TREND_TEMPLATE
    else:
        template = INSIGHT_TEMPLATE

    prompt = PromptTemplate.from_template(template)
    try:
        response = llm.predict(prompt.format(data_analysis=data_analysis))
        return response
    except Exception as e:
        return generate_fallback_insight(data_analysis)

def generate_fallback_insight(data_analysis):
    """Generate basic insights when LLM fails."""
    insights = []

    if 'churn' in data_analysis.lower():
        insights.append("🔍 **Churn Analysis**: Customer retention requires immediate attention.")
        insights.append("📈 **Recommendation**: Implement targeted retention campaigns for high-risk segments.")
        insights.append("📊 **Monitor**: Monthly churn rates by tier and segment.")

    elif 'revenue' in data_analysis.lower():
        insights.append("💰 **Revenue Insights**: Focus on revenue optimization opportunities.")
        insights.append("📈 **Recommendation**: Prioritize high-value customer segments and tiers.")
        insights.append("📊 **Monitor**: Revenue per customer and lifetime value metrics.")

    else:
        insights.append("📊 **Data Summary**: Key business metrics require strategic focus.")
        insights.append("📈 **Recommendation**: Develop data-driven action plans based on findings.")
        insights.append("📊 **Monitor**: Core KPIs and performance indicators.")

    return "\n\n".join(insights)

# Legacy function for backwards compatibility
def summarize_data(table):
    """Legacy function - redirects to generate_insights."""
    return generate_insights(table)
