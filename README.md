# Fintech Copilot

FintechGPT is an AI-powered Streamlit app that answers product and business questions conversationally using pre-trained fintech product datasets. 

It combines:
- Natural language querying over a structured dataset (Pandas)
- Automated, context-aware visualizations (charts saved on the fly)
- Executive-level insight generation
- A fintech glossary lookup for common metrics and terms

The AI agent intelligently thinks about your question through using multiple tools to analyze data, select appropriate visuals, and summarize key insights.

<p align="center">
  <img alt="Fintech.GPT Home" src="docs/screenshots/home.png" width="800">
</p>

---

## Key Features

- Conversational analytics with memory (last 10 exchanges)
- Smart Analyzer: figures out intent, metrics, and best visualization
- Natural language queries mapped to Pandas operations
- Auto-generated charts for churn, revenue, spending, features, trends, and comparisons
- Executive summaries and recommendations from analysis
- Fintech glossary lookup (CLTV, CAC, NRR, etc.)

---

## Demo Screenshots

- Home view with example prompts

  <img alt="Home" src="docs/screenshots/home.png" width="800">

- Analysis results with insights and chart

  <img alt="Analysis" src="docs/screenshots/analysis.png" width="800">

- Auto-generated chart preview

  <img alt="Chart" src="docs/screenshots/chart.png" width="800">

---

## Quick Start

### Prerequisites

- Python 3.9+ (3.10+ recommended)
- An OpenAI API key (for GPT-4o and embeddings)

### 1) Clone and set up environment

```bash
git clone https://github.com/justinj8/fintech_copilot.git
cd fintech_copilot

# Create & activate a virtual environment (choose one)
# macOS/Linux
python3 -m venv .venv && source .venv/bin/activate
# Windows (PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

If you already have a requirements file, use it. Otherwise, install the core packages needed by the app:

```bash
pip install -U pip
pip install streamlit pandas numpy pillow python-dotenv
pip install langchain langchain-openai langchain-community
pip install faiss-cpu
pip install matplotlib seaborn
```

Notes:
- faiss-cpu is required for glossary vector search via FAISS.

### 3) Configure environment variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```


### 4) Ensure data files exist

The app expects:
- data/fintech_product_data.csv
- data/fintech_glossary.json

These are used by the query engine and glossary lookup.

### 5) Run the app

```bash
streamlit run app.py
```

Open the local URL that Streamlit prints (typically http://localhost:8501).

---

## How It Works

- Agent Orchestration: `langchain_agent.py` initializes a conversational agent with memory and these tools:
  - Smart Analyzer (`tools/smart_analyzer.py`): infers intent, metrics, and visualization strategy.
  - Query DataFrame (`tools/query_dataframe.py`): maps natural language to Pandas analytics over `data/fintech_product_data.csv`.
  - Generate Visualization (`tools/generate_chart.py`): produces context-aware charts and saves `chart.png`.
  - Summarize Insights (`tools/summarize_insight.py`): produces executive summaries and recommendations.
  - Glossary Lookup (`tools/glossary_lookup.py`): embeddings-based definitions for fintech terms using FAISS.

---

## Example Prompts

Try these in the input box:

- What’s driving our churn rate?
- Show me revenue trends
- Which features are popular?
- Compare customer segments
- Churn rate by tier
- Revenue analysis by segment
- Spending patterns among Premium users
- Monthly signup trend over the last 12 months
- Tier vs segment comparison

The sidebar also includes quick example buttons:
- Churn analysis
- Revenue trends
- Feature usage
- Customer segments

---

## Sample Outputs

- Churn analysis by tier

```text
Overall Churn Rate: 7.6%

Churn Rate by Account Tier:
| account_tier   |   total_customers |   churned_customers |   churn_rate |
|:---------------|------------------:|--------------------:|-------------:|
| Free           |              4,210 |                 389 |        0.092 |
| Plus           |              2,980 |                 198 |        0.066 |
| Premium        |              1,120 |                  35 |        0.031 |
```

- Revenue summary

```text
Total Revenue: $1,234,567.89
Average Revenue per Customer: $42.17

Revenue by Tier:
| account_tier   |   monthly_revenue |
|:---------------|------------------:|
| Free           |          123456.78|
| Plus           |          456789.01|
| Premium        |          654322.10|
```

- Executive insight (summarized)

```text
Executive Summary:
Premium users exhibit the lowest churn and highest ARPU, indicating strong product-market fit at the top tier.

Critical Insights:
- Churn in Free is 3x higher than Premium; conversion levers should focus on value unlockers.
- Revenue concentration in Premium suggests opportunity to expand Plus with targeted upsell bundles.
- Feature adoption correlates with retention; "SavingsVault" users retain 20% better.

Recommendations:
- Launch targeted retention offers for Free users showing high decline_rate.
- Bundle "RoundUps" + "SavingsVault" in Plus to lift ARPU and retention.
- Track monthly churn and ARPU by tier; goal: reduce Free churn by 2pp in 90 days.
```

## Project Structure

```text
fintech_copilot/
├─ app.py                      # Streamlit UI
├─ langchain_agent.py          # Agent + tools wiring, memory, system prompt
├─ tools/
│  ├─ query_dataframe.py       # Natural language -> Pandas analytics
│  ├─ generate_chart.py        # Context-aware chart generation (saves chart.png)
│  ├─ summarize_insight.py     # Executive summaries & recommendations
│  ├─ glossary_lookup.py       # FAISS-backed term lookup with OpenAI embeddings
│  └─ smart_analyzer.py        # Intent, metrics, visualization planning
├─ data/
│  ├─ fintech_product_data.csv # Core dataset
│  └─ fintech_glossary.json    # Glossary terms for lookup
├─ docs/
│  └─ screenshots/             
└─ README.md
```

---

## Configuration

Environment variables (via `.env`):
- OPENAI_API_KEY: Required for GPT-4o and embeddings.

Model and behavior:
- Uses `gpt-4o` with low temperature for consistent analytical output.
- Conversation memory window: last 10 exchanges.

---

## Troubleshooting

- FAISS install issues:
  - Try `pip install --only-binary=:all: faiss-cpu`
  - Consider using conda: `conda install -c conda-forge faiss-cpu`
- Mac M1/M2:
  - Use Python 3.10+ and the latest pip.
  - Ensure Xcode command line tools are installed.
- OpenAI API errors:
  - Verify `OPENAI_API_KEY` is set and not rate-limited.

---

## Roadmap Ideas

- Bring-your-own data upload with schema detection
- Multi-file dataset joins and entity resolution
- Saved analyses and dashboards
- Export to PDF/PowerPoint
- RAG over documentation and product specs
