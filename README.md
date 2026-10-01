# Online Retail Analytics Dashboard

An interactive **Online Retail Analytics** project built with Python, Pandas, Plotly, and Streamlit. The project analyzes transactional e-commerce data and presents key business insights through an interactive dashboard.

## Project Overview

This project transforms raw online retail transactions into actionable business insights covering sales performance, customers, products, countries, order status, and customer segmentation.

The project includes:

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Sales and revenue analysis
- Product performance analysis
- Country-level sales analysis
- Customer analysis
- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation
- Return and cancellation analysis
- Interactive Streamlit dashboard
- Visual business insights

## Dataset

The project uses the **Online Retail** transactional dataset.

Important fields include:

- `InvoiceNo` — Invoice/order identifier
- `StockCode` — Product identifier
- `Description` — Product description
- `Quantity` — Number of items purchased
- `InvoiceDate` — Transaction date and time
- `UnitPrice` — Price per item
- `CustomerID` — Customer identifier
- `Country` — Customer country

Revenue is calculated from:

```text
Revenue = Quantity × UnitPrice
```

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
│
├── notebooks/
│
├── reports/
│
├── src/
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
└── run_dashboard.bat
```

## Dashboard

The Streamlit dashboard provides an interactive view of the retail business.

### Main Dashboard Features

- Revenue and sales KPIs
- Revenue over time
- Sales by country
- Top-performing products
- Customer segmentation
- RFM analysis
- Order status analysis
- Interactive filters
- Responsive visualizations
- Business insights

The dashboard follows a modern **orange, cream, and charcoal** visual theme designed for a clean e-commerce analytics experience.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |
| Matplotlib | Data visualization |
| Scikit-learn | Machine learning and clustering |

## Installation

Clone the repository:

```bash
git clone https://github.com/nouramaherelamin/Online_Retail_Analytics.git
cd Online_Retail_Analytics
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
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

Or, if you are using the provided Windows batch file:

```bash
run_dashboard.bat
```

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

## Data Preparation

The analysis workflow includes common transaction-data preparation steps such as:

1. Loading the dataset.
2. Handling missing values.
3. Removing duplicate records.
4. Checking invalid quantities and prices.
5. Identifying cancellations and returns.
6. Separating non-product transaction codes where applicable.
7. Creating calculated revenue fields.
8. Preparing clean data for analysis and visualization.

## RFM Analysis

Customer behavior is analyzed using RFM:

- **Recency** — How recently a customer purchased.
- **Frequency** — How often a customer purchased.
- **Monetary** — How much revenue a customer generated.

The RFM framework is then used to create customer segments that help describe different purchasing behaviors.

## Business Questions

The project investigates questions such as:

- How does revenue change over time?
- Which countries generate the most sales?
- Which products perform best?
- Which customers generate the most value?
- What customer segments exist?
- How significant are returns and cancellations?
- How does order activity change over time?
- What patterns can be identified from customer purchasing behavior?

## Running the Project

After installing the dependencies, the recommended workflow is:

```bash
# Activate environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run dashboard/app.py
```

# Author
<div align="center">
  
**Noura Maher Elamin**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/nouramaherelamin/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/nouramaherelamin)
