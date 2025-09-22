from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

ANALYSIS_TEMPLATE = """
You are a fintech data analysis expert. Analyze the user's question and provide a structured analysis plan.

User Question: {question}
Context: Fintech dataset with customer data, account tiers, spending, features usage, and churn information.

Provide a JSON response with:
{{
    "intent": "primary goal (analysis, comparison, trend, prediction, etc.)",
    "data_focus": "main data areas to examine",
    "metrics": ["list of key metrics to calculate"],
    "visualization_type": "best chart type (bar, line, scatter, heatmap, pie, etc.)",
    "analysis_depth": "summary|detailed|comprehensive",
    "assumptions": "reasonable assumptions if question is ambiguous",
    "suggested_queries": ["specific data queries needed"],
    "business_context": "why this analysis matters for fintech business"
}}

Examples:
- "What's driving churn?" → comprehensive analysis across segments, tiers, features
- "Show me revenue trends" → time series analysis with line charts
- "Compare customer segments" → comparative analysis with bar/grouped charts
- "Which features are popular?" → frequency analysis with bar charts or pie charts
"""

def analyze_question(question):
    """Intelligently analyze user questions to determine the best analytical approach."""

    prompt = PromptTemplate.from_template(ANALYSIS_TEMPLATE)
    formatted_prompt = prompt.format(question=question)

    try:
        response = llm.predict(formatted_prompt)
        # Try to extract JSON from response
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = response[start:end]
            analysis = json.loads(json_str)
            return json.dumps(analysis, indent=2)
        else:
            # Fallback if JSON extraction fails
            return create_fallback_analysis(question)
    except Exception as e:
        return create_fallback_analysis(question)

def create_fallback_analysis(question):
    """Create a basic analysis when LLM parsing fails."""
    question_lower = question.lower()

    # Determine basic intent
    if any(word in question_lower for word in ['churn', 'retention', 'leave', 'quit']):
        intent = "churn_analysis"
        metrics = ["churn_rate", "retention_rate", "customer_lifetime"]
        viz_type = "bar"
    elif any(word in question_lower for word in ['revenue', 'money', 'profit', 'income']):
        intent = "revenue_analysis"
        metrics = ["monthly_revenue", "revenue_per_customer", "total_revenue"]
        viz_type = "line"
    elif any(word in question_lower for word in ['compare', 'vs', 'versus', 'difference']):
        intent = "comparison"
        metrics = ["comparative_metrics"]
        viz_type = "bar"
    elif any(word in question_lower for word in ['trend', 'over time', 'monthly', 'growth']):
        intent = "trend_analysis"
        metrics = ["time_series_metrics"]
        viz_type = "line"
    else:
        intent = "exploratory"
        metrics = ["descriptive_statistics"]
        viz_type = "bar"

    analysis = {
        "intent": intent,
        "data_focus": "customer_behavior",
        "metrics": metrics,
        "visualization_type": viz_type,
        "analysis_depth": "detailed",
        "assumptions": "Using available dataset columns for analysis",
        "suggested_queries": [f"Analyze data related to: {question}"],
        "business_context": "Understanding customer patterns for business optimization"
    }

    return json.dumps(analysis, indent=2)