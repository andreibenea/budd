# Personal Finance Tracker - CLI

###### PCAP-31 Exam Prep Project

## Description

A command-line budget management application built in Python that helps you track income, expenses, and spending
patterns.

## Features

Some already implemented, some still a work in progress. This document will be updated as needed.

- Account Management: Track your balance with incomes and expenses
- Transaction History: View detailed records of all financial activities with timestamps
- Categorized Spending: Organize transactions by type (Food, Rent, Transportation, etc.)
- Data Persistence: Automatic saving and loading of account data using JSON storage
- Rich Terminal Interface: Beautiful formatted tables and colored output for better readability

### Installation

#### Prerequisites

- Python 3.10 or higher
- pip package manager

#### Setup

1. Clone the repository:

```
git clone git@github.com:andreibenea/budd.git>
cd personalFinanceTracker
```

2. Create and activate virtual environment:

```
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

### Usage

Run the application:

```
python3 main.py
```

Follow the on-screen menu to:

- Check your current balance
- Add income
- Add expenses
- View transaction history
- Categorize your spending

### Project Structure
```
finance_tracker/
├── main.py # Entry point, main menu
├── models/
│ ├── __init__.py
│ ├── transaction.py # Transaction, Income, Expense classes
│ ├── account.py # Account class
│ └── budget.py # Budget class
├── utils/
│ ├── __init__.py
│ ├── file_handler.py # Save/load data (CSV/JSON)
│ ├── validators.py # Input validation
│ ├── formatters.py # Display formatting
│ ├── messages.py # Custom messages
│ └── exceptions.py # Custom exceptions
├── data/
│ ├── transactions.csv # Stored transaction data
│ └── budget.json # Stored budget data
└── README.md

```

### Technologies Used

- Python 3.x
- Rich - Terminal formatting and tables
- JSON - Data storage

### Development

This project was built as a learning exercise focusing on:

- Object-oriented programming principles
- File I/O and data persistence
- Exception handling
- Clean code architecture
- Terminal user interfaces