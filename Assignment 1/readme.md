# DB25 Assignment 1 – Database Optimization Using Indexes

## 📘 Overview

This repository contains my submission for Assignment 1 of the DB25 course at Innopolis University (Spring 2025). The focus of this assignment is on optimizing the performance of SQL queries using indexes in PostgreSQL.

## 📋 Assignment Details

- **Topic**: Database Optimization Using Indexes
- **Database**: Flights Database (`demo-medium-en-20170815`)
- **DBMS**: PostgreSQL 17.4

### 🔗 Dataset Download

You can download the dataset used in this assignment here:  
[Flights Database – demo-medium-en-20170815](https://edu.postgrespro.com/demo-medium-en-20170815.zip)

## ✅ Objective

Analyze and enhance the performance of **five SQL queries** (four SELECT and one UPDATE) by designing and applying a single set of indexes. The goal is to reduce query costs by using efficient indexing strategies.

## 🗃️ Deliverables

- A single `.sql` file that:
  - Contains only `CREATE INDEX` statements
  - Does not exceed **1000 lines** or **1000 indexes**
  - Has **no duplicate index names**
  - Is executable without errors on a fresh PostgreSQL instance


## 🧠 Optimization Strategy

- Indexes were chosen based on query patterns including:
  - JOIN conditions
  - WHERE clause filters
  - GROUP BY and ORDER BY clauses
  - Window functions and recursive CTEs
- The same index set is applied for **all five queries**.

## 🧪 Testing Instructions

To test the script:

1. Download and set up the Flights database.
2. Run the provided SQL file on a fresh installation.
3. Verify that:
   - No errors occur
   - All indexes are created successfully
4. Run the five queries and compare the `EXPLAIN` cost before and after indexing.


## 🧑‍💻 Author

- [Ahmed Baha Eddine Alimi]
- DB25 – Spring 2025
- Innopolis University

## 📎 License

This project is for academic purposes only.
