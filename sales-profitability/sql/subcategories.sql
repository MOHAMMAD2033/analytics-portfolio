SELECT sub_category, SUM(sales) AS sales, SUM(profit) AS profit, SUM(profit)/NULLIF(SUM(sales),0) AS profit_margin FROM sales GROUP BY sub_category ORDER BY profit;
