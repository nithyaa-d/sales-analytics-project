\# Retail Sales Analytics | Python • PostgreSQL • Data Analysis



An end-to-end retail sales analytics project using Python and PostgreSQL to transform raw transactional data into actionable business insights.



The project covers data cleaning, data quality validation, exploratory data analysis, SQL-based business intelligence, customer analysis, product profitability, and data visualisation.



\## Project Overview



This project analyses the Sample Superstore dataset to understand sales performance, profitability, customer purchasing behaviour, regional trends, and the impact of discount levels.



The objective is to demonstrate a complete analytics workflow, from raw data preparation to business recommendations.



\## Key Business Metrics



| KPI | Result |

|---|---:|

| Total Revenue | $2,297,200.86 |

| Total Profit | $286,397.02 |

| Profit Margin | 12.47% |

| Total Orders | 5,009 |

| Unique Customers | 793 |

| Unique Products | 1,862 |

| Units Sold | 37,873 |

| Average Order Value | $458.61 |



\## Business Insights



\- \*\*Regional performance:\*\* The West region generated the highest revenue ($725,457.82) and profit ($108,418.45).

\- \*\*Category performance:\*\* Technology led revenue with $836,154.03 and profit with $145,454.95.

\- \*\*Profitability opportunity:\*\* Furniture generated $741,999.80 in revenue but had a relatively low profit margin of 2.49%.

\- \*\*Customer retention:\*\* 781 of 793 customers made repeat purchases, representing 98.49% of customers.

\- \*\*Product performance:\*\* Canon imageCLASS 2200 Advanced Copier was the highest-revenue product, generating $61,599.82.

\- \*\*Loss-making products:\*\* Cubify CubeX 3D Printer Double Head Print recorded a loss of $8,879.97.

\- \*\*Discount analysis:\*\* Discount levels of 30% and above were associated with negative aggregate profit in this dataset. This is an observed relationship, not proof of causation.



\## Technology Stack



| Area | Tools |

|---|---|

| Programming | Python |

| Data Analysis | Pandas, NumPy |

| Data Visualisation | Matplotlib, Seaborn |

| Database | PostgreSQL |

| Querying | SQL |

| Development | VS Code, pgAdmin |

| Version Control | Git, GitHub |



\## Project Workflow



1\. \*\*Data ingestion:\*\* Load the raw Superstore dataset.

2\. \*\*Data cleaning:\*\* Standardise column names, parse dates, convert data types, and handle missing values.

3\. \*\*Data quality:\*\* Validate duplicates, missing essential fields, invalid quantities, discounts, and shipping dates.

4\. \*\*Exploratory analysis:\*\* Calculate business KPIs and investigate sales, profit, customers, products, and regions.

5\. \*\*SQL analytics:\*\* Perform aggregations, customer analysis, ranking, cumulative revenue, and time-based analysis.

6\. \*\*Visualisation:\*\* Generate charts to communicate trends and business findings.

7\. \*\*Reporting:\*\* Document findings and analytical outputs.



\## SQL Analysis



The PostgreSQL scripts demonstrate:



\- Business KPI calculations

\- Category and regional performance

\- Monthly revenue trends and year-over-year analysis

\- Top-performing products using window functions

\- Repeat customer analysis

\- Customer ranking

\- Cumulative revenue calculations

\- Shipping performance analysis

\- Product profitability and revenue contribution



\## Visualisations



The project includes the following charts:



\- Monthly sales and profit trends

\- Sales by product category

\- Profit by region

\- Top 10 products by sales

\- Top 10 loss-making products

\- Discount versus profit analysis



Charts are available in `reports/figures/`.



\## Repository Structure



```text

sales-analytics-project/

│

├── data/

│   ├── raw/

│   │   └── superstore.csv

│   └── processed/

│       ├── superstore\_cleaned.csv

│       ├── data\_quality\_report.csv

│       ├── business\_kpis.csv

│       ├── monthly\_trends.csv

│       ├── category\_performance.csv

│       └── regional\_performance.csv

│

├── reports/

│   ├── figures/

│   ├── business\_insights.md

│   ├── sql\_kpi\_results.txt

│   └── sql\_advanced\_results.txt

│

├── sql/

│   ├── 01\_schema.sql

│   ├── 02\_data\_quality.sql

│   ├── 03\_sales\_kpis.sql

│   └── 04\_advanced\_analysis.sql

│

├── src/

│   ├── data\_cleaning.py

│   ├── eda.py

│   └── visualizations.py

│

├── requirements.txt

└── README.md

```



\## How to Run the Project



\### 1. Clone the repository



```bash

git clone https://github.com/nithyaa-d/sales-analytics-project.git

cd sales-analytics-project

```



\### 2. Create a Python environment



```bash

python -m venv venv

```



Activate it on Windows:



```bash

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Run data cleaning



```bash

python src/data\_cleaning.py

```



\### 5. Run exploratory data analysis



```bash

python src/eda.py

```



\### 6. Generate visualisations



```bash

python src/visualizations.py

```



\### 7. Run PostgreSQL analysis



Create a PostgreSQL database named `sales\_analytics`, then execute the SQL scripts in order:



```bash

psql -U postgres -d sales\_analytics -f sql/01\_schema.sql

```



Import the cleaned CSV into the `raw\_superstore` table using PostgreSQL's `\\copy` command:



```sql

\\copy raw\_superstore FROM 'data/processed/superstore\_cleaned.csv' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8');

```



Then execute:



```bash

psql -U postgres -d sales\_analytics -f sql/02\_data\_quality.sql

psql -U postgres -d sales\_analytics -f sql/03\_sales\_kpis.sql

psql -U postgres -d sales\_analytics -f sql/04\_advanced\_analysis.sql

```



\## Project Outcomes



This project demonstrates practical experience in:



\- Python-based data preparation and analysis

\- SQL querying and analytical problem-solving

\- PostgreSQL database management

\- Data quality validation

\- Business KPI development

\- Customer and product performance analysis

\- Data visualisation and reporting

\- Translating analytical results into business recommendations



\## Author



\*\*Nithya Doresha\*\*



Data Analyst | BI Analyst | Analytics Engineer



Gothenburg, Sweden  

Open to relocation anywhere within Sweden.



\[LinkedIn](https://www.linkedin.com/in/nithyad2608/) · \[GitHub](https://github.com/nithyaa-d)

