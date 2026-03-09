# Movie Data Analysis System 🎬

A comprehensive SQLite database and Python analysis tool for movie datasets. This project explores movie trends, genres, and financial data using SQL queries and automated data visualization.

---

## 🏗️ Database Schema (ER Diagram)

The database follows a relational structure to ensure data integrity and minimize redundancy.

![ER Diagram](ER.drawio.pdf)

## 📊 Data Analysis & Visualization

The project includes a series of complex SQL queries (translated for SQLite) that analyze:

* Production Trends: Number of movies produced per year based on budget constraints.

* Genre Evolution: Tracking how different genres (Action, Drama, etc.) trend over decades.

* Financial Insights: Identifying top-grossing actors (e.g., Antonio Banderas) and highest-budget films.

* User Ratings: Statistical analysis of user behavior and movie popularity.

Key Features of the Visualization Tool:

* Automated Bar Charts: Cleans and formats SQL output into readable graphs.

* Time-Series Analysis: Specialized line charts for tracking genre popularity over the last 25 years.

* Smart Formatting: Automatic handling of overlapping labels and large font sizes for better readability.

## 🛠️ Technical Details

* Database: SQLite 3.

    Data Cleaning: Built-in Python functions to handle duplicate entries and integrity constraints during CSV import.

    SQL Dialect: Optimized for SQLite (using strftime for dates and LIMIT for top results).

## 👨‍💻 Author

Aikaterini Vantaraki - Athens University of Economics and Business - Department of Informatics

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.x**
* **Libraries:** `pandas`, `matplotlib`, `sqlite3`

### Installation
Clone the repository:
   ```bash
   git clone [https://github.com/AikVant/sql_queries.git](https://github.com/AikVant/sql_queries.git)
   ```
### 🐍 Environment Setup
It is recommended to use a virtual environment. You can install all dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 🛠️ Database Setup
Note: The repository includes the raw CSV datasets but **not** the generated SQLite database file (`movies_database.db`). 

To generate the database and populate the tables, run the setup script:
```bash
python setup_project.py