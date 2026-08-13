import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5432/berka")

query = """
SELECT d.client_id, t.date, t.amount
FROM trans t
JOIN disp d ON d.account_id = t.account_id
WHERE t.k_symbol NOT LIKE '%%UROK%%' OR t.k_symbol IS NULL
"""

df = pd.read_sql(query, engine)
frequency = df.groupby('client_id').size()
monetary = df.groupby('client_id')['amount'].sum()



query = """
SELECT c.client_id,
       DATE '1998-12-31' - TO_DATE(latest.date::TEXT, 'YYMMDD') AS recency
FROM client c
JOIN disp d ON d.client_id = c.client_id
JOIN (
    SELECT account_id, date,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY date DESC) AS rn
    FROM trans
    WHERE k_symbol NOT LIKE '%%UROK%%' OR k_symbol IS NULL
) latest ON latest.account_id = d.account_id
WHERE latest.rn = 1
"""

df = pd.read_sql(query, engine)

recency = df



rfm = pd.DataFrame({
    'frequency': frequency,
    'monetary': monetary,
})

rfm = pd.merge(rfm, recency, how='inner', left_on=['client_id'], right_on=['client_id'])



rfm.to_csv('data/rfm_features.csv', index=False)