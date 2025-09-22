
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from tools import query_dataframe, generate_chart, summarize_insight, glossary_lookup, smart_analyzer

llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

tools = [
    Tool(
        name="Smart Analyzer",
        func=smart_analyzer.analyze_question,
        description="Intelligently analyze user questions and determine the best approach for data analysis, visualization, and insights. Use this FIRST for any user question to understand intent and context."
    ),
    Tool(
        name="Query DataFrame",
        func=query_dataframe.query_dataframe,
        description="Execute data queries on fintech dataset. Supports natural language queries, pandas operations, and statistical analysis."
    ),
    Tool(
        name="Generate Visualization",
        func=generate_chart.smart_visualize,
        description="Create intelligent visualizations (bar charts, line plots, heatmaps, scatter plots, etc.) based on data type and analysis goals."
    ),
    Tool(
        name="Summarize Insights",
        func=summarize_insight.generate_insights,
        description="Generate comprehensive business insights and executive summaries from data analysis."
    ),
    Tool(
        name="Glossary Lookup",
        func=glossary_lookup.search_term,
        description="Look up fintech business terms, metrics, and definitions (CLTV, CAC, NRR, etc.)."
    )
]

# Enhanced memory for better context awareness
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=10  # Keep last 10 exchanges
)

# System prompt for enhanced reasoning
system_prompt = """You are an expert fintech data analyst and business intelligence assistant.

Your capabilities:
- Deep understanding of fintech metrics, KPIs, and business models
- Advanced data analysis and statistical reasoning
- Intelligent visualization selection based on data types and user intent
- Context-aware responses that build on conversation history
- Ability to handle ambiguous questions by asking clarifying questions or making reasonable assumptions

Approach:
1. ALWAYS start with Smart Analyzer to understand the user's intent
2. Use context from conversation history to provide relevant insights
3. Choose appropriate visualizations based on data type and analysis goal
4. Provide actionable business insights, not just data summaries
5. Ask clarifying questions when needed, but also make intelligent assumptions
6. Consider multiple angles: customer behavior, business impact, trends, and recommendations

Dataset Context: Fintech product data including customer demographics, account tiers, spending patterns, feature usage, and churn data."""

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": system_prompt,
        "extra_prompt_messages": [{"type": "system", "content": system_prompt}]
    },
    handle_parsing_errors=True,
    max_iterations=5
)
