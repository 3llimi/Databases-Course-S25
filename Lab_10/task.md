# Lab 10 - SQL Transactions Testing Documentation

## Setup Verification

### 1. Verify Accounts Table
```sql
SELECT * FROM Accounts;
```
**Output:**
| AccountID | OwnerName | Balance  | Currency | BankCountry |
|-----------|-----------|---------|----------|-------------|
| 1         | Owner 1   | 1500.00 | USD      | USA         |
| 2         | Owner 2   | 1300.00 | EUR      | Germany     |
| 3         | Owner 3   | 100000.00 | RUB    | Russia      |
| 4         | Bank Fees | 0.00    | RUB      | Russia      |

---

### 2. Verify Currency Rates
```sql
SELECT * FROM CurrencyRates;
```
**Output:**
| CurrencyFrom | CurrencyTo | ConversionRate |
|-------------|------------|----------------|
| USD         | EUR        | 0.92           |
| EUR         | USD        | 1.09           |
| USD         | RUB        | 75.00          |
| RUB         | USD        | 0.013          |
| EUR         | RUB        | 81.00          |
| RUB         | EUR        | 0.012          |

---

## Testing Transactions (Part A)

### 3. Execute Transactions
```sql
SELECT PerformTransaction(1, 2, 200);
SELECT PerformTransaction(2, 3, 300);
SELECT PerformTransaction(3, 1, 1000);
```

### 4. Verify Account Balances After Transactions
```sql
SELECT * FROM Accounts;
```
**Output:**
| AccountID | OwnerName | Balance  | Currency | BankCountry |
|-----------|-----------|---------|----------|-------------|
| 1         | Owner 1   | 1313.00 | USD | USA |
| 2         | Owner 2   | 1184.00 | EUR | Germany |
| 3         | Owner 3   | 123300.00 | RUB | Russia |
| 4         | Bank Fees | 0 | RUB | Russia |
---

## Testing Transactions with Fees (Part B)

### 5. Execute Transactions with Fees
```sql
SELECT PerformTransactionWithFee(1, 3, 200);
SELECT PerformTransactionWithFee(2, 1, 300);
SELECT PerformTransactionWithFee(3, 2, 15000);
```

### 6. Verify Account Balances After Fee Transactions
```sql
SELECT * FROM Accounts;
```
**Output (Including Fees):**
| AccountID | OwnerName | Balance  | Currency | BankCountry |
|-----------|-----------|---------|----------|-------------|
| 1         | Owner 1   | 1415.00 | USD | USA |
| 2         | Owner 2   | 1044.00 | EUR | Germany |
| 3         | Owner 3   | 121800.00 | RUB | Russia |
| 4         | Bank Fees | 4995.00 | RUB | Russia |

---
Account 1: Adjusted for 200 USD and 25 USD Fee
<br>
Account 2: Adjusted for 300 EUR and 20 EUR Fee
<br>
Account 3: Adjusted for 15000 RUB and 1500 RUB Fee
<br>
Account 4: Total Fees Collected (converted to ruble)

## Rollback Mechanism Testing

### 7. Rollback Transactions
```sql
SELECT RollbackTransactions();
```

### 8. Verify Accounts Reset
```sql
SELECT * FROM Accounts;
```
**Output:** (Restored initial balances)
| AccountID | OwnerName | Balance  | Currency | BankCountry |
|-----------|-----------|---------|----------|-------------|
| 1         | Owner 1   | 1500.00 | USD      | USA |
| 2         | Owner 2   | 1300.00 | EUR      | Germany |
| 3         | Owner 3   | 100000.00 | RUB    | Russia |
| 4         | Bank Fees | 0.00    | RUB      | Russia |

---

## Conclusion
All transactions and rollback mechanisms function correctly, ensuring proper updates, conversions, and fee calculations.
