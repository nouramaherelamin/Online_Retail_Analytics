# Online Retail Analytics Dashboard

An end-to-end Online Retail Analytics project built with Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, and Streamlit. The project analyzes transactional e-commerce data and transforms it into meaningful business insights through data cleaning, exploratory analysis, visualization, customer analysis, and an interactive dashboard.

## Project Overview

This project analyzes transactional data from a UK-based online retail business covering the period from 01/12/2010 to 09/12/2011. The original UCI Online Retail Dataset contains 541,909 transactions and includes real-world data-quality challenges such as missing values, cancelled invoices, returned products, zero-price transactions, and negative quantities.

A 10% sample of the original dataset was used for the analysis.

The complete workflow follows:

Raw Data → Sampling → Data Cleaning → Data Preparation → Revenue Calculation → EDA → Visualization → Insights → Business Recommendations → Interactive Dashboard

The project was developed as part of the Roadmap.sh E-commerce Data Analysis Project.

## Objectives

The main objectives of this project are to:

- Clean and prepare real-world transactional data.
- Calculate transaction-level revenue.
- Analyze sales performance over time.
- Examine revenue distribution across countries.
- Analyze customer purchasing behavior.
- Identify top-performing products.
- Identify returns and cancelled orders.
- Create informative data visualizations.
- Perform RFM analysis and customer segmentation.
- Present business insights through an interactive Streamlit dashboard.
- Translate analytical findings into actionable business recommendations.

## Dataset

The analysis is based on the UCI Online Retail Dataset.

| Detail | Value |
|---|---|
| Dataset | UCI Online Retail Dataset |
| Source | UCI Machine Learning Repository |
| Original Rows | 541,909 |
| Features | 8 |
| Business Type | UK-based Online Retail |
| Period | 01/12/2010 – 09/12/2011 |
| Sample Used | 10% of the original dataset |

Dataset source: https://archive.ics.uci.edu/dataset/352/online+retail

## Dataset Features

| Column | Description |
|---|---|
| InvoiceNo | Unique identifier for each invoice/transaction |
| StockCode | Unique identifier for each product |
| Description | Product name or description |
| Quantity | Number of units purchased |
| InvoiceDate | Date and time of the transaction |
| UnitPrice | Price per unit |
| CustomerID | Unique identifier for each customer |
| Country | Customer's country |

## Data Cleaning and Preparation

Several data-cleaning steps were performed before the analysis:

- Handling missing values.
- Converting columns to appropriate data types.
- Converting InvoiceDate to datetime.
- Identifying negative quantities as returns.
- Identifying cancelled invoices.
- Identifying zero-price transactions.
- Checking inconsistent and invalid values.
- Preparing a reliable dataset for revenue and sales analysis.

## Revenue Calculation

A new Revenue feature was calculated at the transaction level:

```text
Revenue = Quantity × UnitPrice
```

This metric was used to analyze:

- Total revenue
- Revenue by country
- Monthly revenue
- Product revenue
- Customer revenue
- Revenue concentration

## Exploratory Data Analysis

The analysis covers several dimensions of the retail business.

### Sales Performance

- Total revenue
- Total orders
- Monthly revenue
- Monthly order volume
- Average revenue per customer

### Geographic Analysis

- Revenue by country
- Orders by country
- Revenue concentration across countries

### Product Analysis

- Top products by quantity sold
- Top products by revenue
- Product revenue contribution
- Comparison between product popularity and revenue performance

### Customer Analysis

- Unique customers
- Customer revenue
- High-value customers
- Revenue concentration among customers
- RFM analysis
- Customer segmentation

### Returns and Cancellations

- Returned quantities
- Return rate
- Cancelled invoices
- Impact of returns on sales performance

## Key Performance Metrics

The following metrics were obtained from the 10% sample used in the analysis:

| Metric | Value |
|---|---:|
| Total Revenue | 9,726,006.954 |
| Total Orders | 24,446 |
| Unique Customers | 4,372 |
| Highest Revenue Month | November 2011 |
| November 2011 Revenue | ≈ 1.46M |
| Top 5 Countries Revenue Contribution | ≈ 93.91% |
| Return Rate | ≈ 1.82% |
| Average Revenue per Customer | ≈ 1,893.53 |
| Top 10 Products Revenue Contribution | ≈ 10.86% |

Note: These metrics represent the analyzed sample and should not be interpreted as full-dataset totals.

## RFM Analysis

Customer behavior is analyzed using RFM:

- Recency — How recently a customer purchased.
- Frequency — How often a customer purchased.
- Monetary — How much revenue a customer generated.

The RFM framework is used to create customer segments and understand different purchasing behaviors.

## Dashboard

The project includes an interactive Streamlit dashboard that provides a visual overview of retail performance.

### Main Dashboard Features

- Revenue and sales KPIs
- Revenue over time
- Sales by country
- Top-performing products
- Customer segmentation
- RFM analysis
- Order status analysis
- Return and cancellation analysis
- Interactive filters
- Responsive visualizations
- Business insights

The dashboard follows a modern orange, cream, and charcoal visual theme designed for a clean e-commerce analytics experience.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |
| Scikit-learn | Machine learning and clustering |
| Jupyter Notebook | Analysis and documentation |

## Project Structure

```text
Online_Retail_Analytics/
│
├── dashboard/
│   ├── assets/
│   │   ├── icons/
│   │   └── images/
│   ├── data/
│   ├── .streamlit/
│   ├── app.py
│   ├── requirements.txt
│   └── THEME_README.md
│
├── data/
├── notebooks/
├── reports/
├── src/
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
└── run_dashboard.bat
```

## Installation

Clone the repository:

```bash
git clone https://github.com/nouramaherelamin/Online_Retail_Analytics.git
cd Online_Retail_Analytics
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

From the project root:

```bash
streamlit run dashboard/app.py
```

Or use the provided Windows batch file:

```bash
run_dashboard.bat
```

The dashboard will normally be available at:

```text
http://localhost:8501
```

## Business Questions

The project investigates questions such as:

- How does revenue change over time?
- Which countries generate the most sales?
- Which products perform best?
- Which customers generate the most revenue?
- What customer segments exist?
- How significant are returns and cancellations?
- How does order activity change over time?
- What patterns can be identified from customer purchasing behavior?

## Key Insights

### Geographic Performance

The United Kingdom generates the majority of the revenue in the analyzed transactions. A relatively small number of countries account for most of the revenue, with the top five countries contributing approximately 93.91% of analyzed revenue.

### Monthly Performance

November 2011 recorded the highest monthly revenue, reaching approximately 1.46M in the analyzed sample.

### Customer Behavior

Revenue is not distributed evenly across customers. A relatively small group of customers contributes a substantial share of total revenue, highlighting the importance of understanding high-value customer behavior.

### Product Performance

Product popularity and revenue performance are not always the same. Some products may have high quantities sold while contributing less revenue, while other products can generate substantial revenue despite lower sales volume.

### Returns

Returns represent approximately 1.82% of the analyzed transactions according to the project's return-rate calculation. Monitoring returned products can help identify potential issues related to product demand, quality, descriptions, pricing, or customer expectations.

## Business Recommendations

Based on the analytical findings, several business actions can be considered:

1. Focus on high-performing markets using country-level revenue analysis.
2. Develop retention and loyalty strategies for high-value customers.
3. Promote products based on revenue contribution as well as quantity sold.
4. Monitor products with unusually high return volumes.
5. Use monthly sales patterns to support inventory planning, promotional campaigns, forecasting, and resource allocation.
6. Evaluate product performance using multiple metrics rather than quantity alone.

## 🌐 Project Website

[View Project Website](https://nouramaherelamin-online-retail-e-commerce-analysisl.vercel.app/)

## What I Learned

This project strengthened my understanding of the complete data analysis workflow, from working with raw transactional data to communicating analytical findings.

Through this project, I practiced:

- Data cleaning and preprocessing
- Handling missing and inconsistent data
- Working with datetime data
- Feature engineering
- Revenue calculation
- Exploratory Data Analysis
- Grouping and aggregation with Pandas
- Data visualization
- Customer and product analysis
- Geographic analysis
- RFM analysis and customer segmentation
- Translating analytical results into business insights

Most importantly, the project helped me understand how raw transactional data can be transformed into information that supports data-driven business decisions.

## Conclusion

The Online Retail Analytics project demonstrates how real-world transactional data can be transformed into meaningful business insights.

The analysis covers:

- Revenue distribution
- Geographic performance
- Monthly sales
- Customer behavior
- Product performance
- Returns and cancellations
- RFM customer segmentation

The project also provides a foundation for further analysis such as sales forecasting, market basket analysis, and predictive modeling.

# Author
<div align="center">
  
**Noura Maher Elamin**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/nouramaherelamin/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/nouramaherelamin)
