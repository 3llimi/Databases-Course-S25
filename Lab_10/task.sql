-- Part A: Account Setup and Basic Transactions
CREATE TABLE Accounts (
    AccountID SERIAL PRIMARY KEY,
    OwnerName VARCHAR(100),
    Balance DECIMAL(15,2),
    Currency VARCHAR(3),
    BankCountry VARCHAR(50) DEFAULT NULL
);

INSERT INTO Accounts (OwnerName, Balance, Currency, BankCountry) VALUES
    ('Owner 1', 1500, 'USD', 'USA'),
    ('Owner 2', 1300, 'EUR', 'Germany'),
    ('Owner 3', 100000, 'RUB', 'Russia'),
    ('Bank Fees', 0, 'RUB', 'Russia');

-- Currency Conversion Table
CREATE TABLE CurrencyRates (
    CurrencyFrom VARCHAR(3),
    CurrencyTo VARCHAR(3),
    ConversionRate DECIMAL(10,4),
    PRIMARY KEY (CurrencyFrom, CurrencyTo)
);

INSERT INTO CurrencyRates VALUES
    ('USD', 'EUR', 0.92),
    ('EUR', 'USD', 1.09),
    ('USD', 'RUB', 75.00),
    ('RUB', 'USD', 0.013),
    ('EUR', 'RUB', 81.00),
    ('RUB', 'EUR', 0.012);

-- Transactions Table
CREATE TABLE Transactions (
    TransactionID SERIAL PRIMARY KEY,
    AccountFrom INT,
    AccountTo INT,
    Amount DECIMAL(15,2),
    ConvertedAmount DECIMAL(15,2),
    Fee DECIMAL(15,2) DEFAULT 0,
    Currency VARCHAR(3),
    FOREIGN KEY (AccountFrom) REFERENCES Accounts(AccountID),
    FOREIGN KEY (AccountTo) REFERENCES Accounts(AccountID)
);

-- Transaction Procedure
CREATE OR REPLACE FUNCTION PerformTransaction(sender INT, receiver INT, amt DECIMAL(15,2)) RETURNS VOID AS $$
DECLARE 
    senderCurrency VARCHAR(3);
    receiverCurrency VARCHAR(3);
    convRate DECIMAL(10,4);
    convertedAmt DECIMAL(15,2);
BEGIN
    SELECT Currency INTO senderCurrency FROM Accounts WHERE AccountID = sender;
    SELECT Currency INTO receiverCurrency FROM Accounts WHERE AccountID = receiver;
    SELECT cr.ConversionRate INTO convRate 
    FROM CurrencyRates cr
    WHERE cr.CurrencyFrom = senderCurrency AND cr.CurrencyTo = receiverCurrency;
    
    convertedAmt := amt * convRate;
    
    UPDATE Accounts SET Balance = Balance - amt WHERE AccountID = sender;
    UPDATE Accounts SET Balance = Balance + convertedAmt WHERE AccountID = receiver;
    
    INSERT INTO Transactions (AccountFrom, AccountTo, Amount, ConvertedAmount, Currency) 
    VALUES (sender, receiver, amt, convertedAmt, senderCurrency);
END;
$$ LANGUAGE plpgsql;

-- Execute Transactions
SELECT PerformTransaction(1, 2, 200);
SELECT PerformTransaction(2, 3, 300);
SELECT PerformTransaction(3, 1, 1000);

-- Part B: Advanced Transactions with Fees
CREATE OR REPLACE FUNCTION PerformTransactionWithFee(sender INT, receiver INT, amt DECIMAL(15,2)) RETURNS VOID AS $$
DECLARE 
    senderCurrency VARCHAR(3);
    receiverCurrency VARCHAR(3);
    senderCountry VARCHAR(50);
    convRate DECIMAL(10,4);
    convertedAmt DECIMAL(15,2);
    feeAmt DECIMAL(15,2);
    feeConverted DECIMAL(15,2);
BEGIN
    SELECT Currency, BankCountry INTO senderCurrency, senderCountry FROM Accounts WHERE AccountID = sender;
    SELECT Currency INTO receiverCurrency FROM Accounts WHERE AccountID = receiver;
    SELECT cr.ConversionRate INTO convRate 
    FROM CurrencyRates cr
    WHERE cr.CurrencyFrom = senderCurrency AND cr.CurrencyTo = receiverCurrency;
    
    -- Determine Fee
    IF senderCountry = 'USA' THEN feeAmt := 25;
    ELSIF senderCountry = 'Germany' THEN feeAmt := 20;
    ELSIF senderCountry = 'Russia' THEN feeAmt := 1500;
    ELSE feeAmt := 0;
    END IF;
    
    -- Convert Fee to RUB before adding to Account 4
    SELECT cr.ConversionRate INTO feeConverted 
    FROM CurrencyRates cr
    WHERE cr.CurrencyFrom = senderCurrency AND cr.CurrencyTo = 'RUB';
    
    feeConverted := feeAmt * COALESCE(feeConverted, 1);
    
    convertedAmt := amt * convRate;
    
    UPDATE Accounts SET Balance = Balance - amt - feeAmt WHERE AccountID = sender;
    UPDATE Accounts SET Balance = Balance + convertedAmt WHERE AccountID = receiver;
    UPDATE Accounts SET Balance = Balance + feeConverted WHERE AccountID = 4;
    
    INSERT INTO Transactions (AccountFrom, AccountTo, Amount, ConvertedAmount, Fee, Currency) 
    VALUES (sender, receiver, amt, convertedAmt, feeAmt, senderCurrency);
END;
$$ LANGUAGE plpgsql;

-- Execute Transactions with Fees
SELECT PerformTransactionWithFee(1, 3, 200);
SELECT PerformTransactionWithFee(2, 1, 300);
SELECT PerformTransactionWithFee(3, 2, 15000);

-- Rollback Mechanism
CREATE OR REPLACE FUNCTION RollbackTransactions() RETURNS VOID AS $$
BEGIN
    DELETE FROM Transactions;
    UPDATE Accounts SET Balance = 1500 WHERE AccountID = 1;
    UPDATE Accounts SET Balance = 1300 WHERE AccountID = 2;
    UPDATE Accounts SET Balance = 100000 WHERE AccountID = 3;
    UPDATE Accounts SET Balance = 0 WHERE AccountID = 4;
END;
$$ LANGUAGE plpgsql;

-- To rollback, execute:
-- SELECT RollbackTransactions();
