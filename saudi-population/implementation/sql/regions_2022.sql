SELECT region,population,1.0*population/SUM(population) OVER() AS national_share FROM population WHERE year=2022 ORDER BY population DESC;
