
<div align="center">

# AI Data Analyst

### Intelligent Data Analytics Platform Powered by Artificial Intelligence

**Transform Raw Data into Meaningful Insights and Smarter Business Decisions.**

<br>

<img src="assets/Home.png" alt="AI Data Analyst Home Page" width="100%">

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Application-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-8A2BE2)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)

</div>

---

## Overview

**AI Data Analyst** is an intelligent data analytics platform built with Python and Streamlit that combines traditional data analysis with Artificial Intelligence.

The application enables users to upload structured datasets, explore data, identify quality issues, perform cleaning operations, generate interactive visualizations, and obtain AI-powered analytical insights.

It also introduces natural-language interaction with datasets, allowing users to ask questions and explore their data through an AI assistant.

The main objective is to make data analysis more accessible, efficient, and insightful by transforming raw data into actionable business intelligence.

---

## Application Preview

### Main Dashboard

The main interface provides an overview of the platform and its analytical capabilities.

<p align="center">
  <img src="assets/Home.png" alt="AI Data Analyst Home Page" width="100%">
</p>

### Analytics Dashboard

Explore dataset statistics, business metrics, and analytical information through an interactive dashboard.

<p align="center">
  <img src="assets/Dashboard.png" alt="AI Data Analyst Analytics Dashboard" width="100%">
</p>

---

## Core Features

### 1. Interactive Analytics Dashboard

- Display important Key Performance Indicators (KPIs).
- Analyze essential dataset statistics.
- Explore numerical and categorical variables.
- Present important business metrics.
- Provide an overview of uploaded datasets.

### 2. Data Exploration

- Upload CSV and Excel files.
- Preview dataset records.
- Inspect columns and data types.
- Explore statistical summaries.
- Analyze dataset dimensions.
- Understand the structure of raw data.

### 3. Data Cleaning & Preparation

- Detect missing values.
- Identify duplicate records.
- Remove unnecessary whitespace.
- Apply data-cleaning operations.
- Handle data quality issues.
- Compare data quality before and after cleaning.

### 4. Interactive Data Visualization

- Generate interactive charts.
- Explore numerical distributions.
- Analyze categorical variables.
- Identify relationships between columns.
- Visualize patterns and analytical results.
- Use Plotly for interactive visualizations.

### 5. AI-Powered Data Insights

- Generate analytical summaries using AI.
- Interpret dataset statistics.
- Identify important business patterns.
- Highlight potential risks and opportunities.
- Generate data-driven recommendations.
- Explain analytical findings using natural language.

### 6. AI Data Chat

- Ask questions about uploaded datasets.
- Interact with data using natural language.
- Request analytical explanations.
- Explore business performance.
- Obtain AI-generated answers based on available dataset information.

---

## Technology Stack

| Technology | Role |
|---|---|
| Python | Core application development |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Streamlit | Interactive web application |
| Plotly | Interactive data visualization |
| Groq API | AI-powered insights and data chat |
| Python-dotenv | Environment variable management |

---

## Project Architecture

```text
AI-Data-Analyst/
│
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_profiler.py
│   ├── data_cleaner.py
│   ├── visualizer.py
│   └── ai_analyst.py
│
├── assets/
│   ├── Home.png
│   └── Dashboard.png
│
├── sample_data/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation & Setup

Follow these steps to run AI Data Analyst locally.

### Prerequisites

- Python 3.10 or higher.
- pip package manager.
- A Groq API key for AI-powered functionality.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Data-Analyst.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Data-Analyst
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your own API key.

**Important:** Never publish your API key or `.env` file.

### 7. Launch the Application

```bash
streamlit run app.py
```

The application will be available in your local browser.

---

## Example Use Cases

AI Data Analyst can be used for:

- Sales and revenue analysis.
- Customer behavior analysis.
- Business performance monitoring.
- Financial dataset exploration.
- Data quality assessment.
- Identifying trends and patterns.
- Generating analytical summaries.
- Supporting data-driven decisions.

---

## Security & Data Privacy

- API credentials are managed through environment variables.
- Sensitive configuration files should remain excluded from version control.
- The `.env` file must never be uploaded to GitHub.
- Users should avoid uploading confidential datasets to external AI services.

---

## Future Development Roadmap

The following improvements are planned for future versions:

- [ ] SQL database integration.
- [ ] Advanced Exploratory Data Analysis (EDA).
- [ ] Predictive analytics and forecasting.
- [ ] Machine Learning model integration.
- [ ] Automated PDF and Excel report generation.
- [ ] Advanced AI analytical agents.
- [ ] Business Intelligence recommendations.
- [ ] User authentication and analysis history.
- [ ] Advanced statistical analysis.
- [ ] Data export and reporting enhancements.

---

## Skills Demonstrated

This project demonstrates practical experience in:

- Python Programming.
- Data Analysis and Data Preparation.
- Exploratory Data Analysis (EDA).
- Data Cleaning and Data Quality.
- Data Visualization.
- Business Intelligence.
- Artificial Intelligence Integration.
- Large Language Model (LLM) APIs.
- Interactive Application Development.
- Translating Data into Business Insights.

---

## Project Information

| Attribute | Details |
|---|---|
| Project Name | AI Data Analyst |
| Category | Data Analytics & Artificial Intelligence |
| Language | Python |
| Application Framework | Streamlit |
| AI Integration | Groq API |
| Development Status | Active Development |
| Repository | GitHub |

---

<div align="center">

## Built with Python, Data Analytics & AI

**Making Data Analysis Smarter, Faster, and More Accessible.**

</div>
