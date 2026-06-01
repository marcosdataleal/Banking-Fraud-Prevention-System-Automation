# Banking-Fraud-Prevention-System-Automation
BankFlow Auditor is a Python-based banking automation and audit support project developed as an academic capstone initiative. It simulates a realistic financial backoffice workflow by generating synthetic bank accounts and transactions, processing operations such as PIX, TED, bill payments, withdrawals, deposits, and card transactions, and applying automated validation rules to identify inconsistencies such as nonexistent accounts, blocked or closed accounts, invalid values, insufficient balance, duplicated transactions, and unusual transaction amounts.

The project combines business rules, data analysis, risk scoring, anomaly detection, and statistical sampling to help prioritize transactions that should be reviewed by an audit or compliance team. Each transaction receives a processing status, rejection reason when applicable, risk score, and risk level. High-risk and rejected transactions are automatically selected for review, while stratified sampling is used to create a balanced audit sample across different risk levels.

BankFlow Auditor was designed to demonstrate how automation can reduce manual review effort in banking operations while improving traceability, prioritization, and decision support. The solution includes CSV and JSON outputs, an HTML audit report, SQLite persistence, a FastAPI REST API, and an interactive Streamlit dashboard with filters, metrics, charts, processed transactions, and audit samples.

The project is intentionally simple and functional, making it suitable for academic presentation, portfolio use, and as a foundation for future improvements such as PostgreSQL integration, authentication, historical execution tracking, file upload, cloud deployment, and real-time transaction monitoring.

Technologies used: Python, SQL, HTML, CSS, CSV, JSON, SQLite, pandas, NumPy, scikit-learn, IsolationForest, FastAPI, Uvicorn, Streamlit, Plotly, and pytest.
