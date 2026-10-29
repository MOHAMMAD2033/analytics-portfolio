SELECT segment,COUNT(*) AS customers,SUM(monetary) AS sales,SUM(profit) AS profit,AVG(recency_days) AS avg_recency,AVG(frequency) AS avg_frequency FROM rfm GROUP BY segment ORDER BY sales DESC;
