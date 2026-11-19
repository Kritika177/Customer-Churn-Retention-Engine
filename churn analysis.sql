CREATE TABLE telco_churn (
    customerID VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(25),
    InternetService VARCHAR(25),
    OnlineSecurity VARCHAR(25),
    OnlineBackup VARCHAR(25),
    DeviceProtection VARCHAR(25),
    TechSupport VARCHAR(25),
    StreamingTV VARCHAR(25),
    StreamingMovies VARCHAR(25),
    Contract VARCHAR(25),
    PaperlessBilling VARCHAR(5),
	PaymentMethod VARCHAR(40),
    MonthlyCharges DECIMAL(10, 2),
    TotalCharges DECIMAL(10, 2),
    Churn VARCHAR(5),
    tenure_Group VARCHAR(25),
    Churn_Flag INT
);
SELECT * FROM telco_churn;
DROP TABLE IF EXISTS telco_churn;
ALTER TABLE telco_churn ALTER COLUMN seniorcitizen TYPE VARCHAR(10);


SELECT 
    COUNT(*) AS total_customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Flag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost
FROM telco_churn;

SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_bill,
    ROUND(SUM(CASE WHEN Churn_Flag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost
FROM telco_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

SELECT 
    InternetService,
    PaymentMethod,
    COUNT(*) AS customer_count,
    ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct
FROM telco_churn
GROUP BY InternetService, PaymentMethod
HAVING COUNT(*) >= 100 AND AVG(Churn_Flag) > 0.35
ORDER BY churn_rate_pct DESC;

WITH ranked_churners AS (
    SELECT 
        customerID,
        Contract,
        Tenure_Group,
        InternetService,
        MonthlyCharges,
        TotalCharges,
        DENSE_RANK() OVER (
            PARTITION BY Contract 
            ORDER BY MonthlyCharges DESC
        ) AS bill_rank
    FROM telco_churn
    WHERE Churn_Flag = 1
)
SELECT * 
FROM ranked_churners
WHERE bill_rank <= 3
ORDER BY Contract, bill_rank;