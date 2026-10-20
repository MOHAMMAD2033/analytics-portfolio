SELECT region, SUM(sales) AS sales, SUM(profit) AS profit, COUNT(DISTINCT order_id) AS orders FROM sales GROUP BY region ORDER BY sales DESC;
