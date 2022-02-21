/* First way prints out all the data in the order of income_diifference  */
SELECT 
    t21.post_code,
    t17.average_income average_income_2017,
    t18.average_income average_income_2018,
    t19.average_income average_income_2019,
    t20.average_income average_income_2020,
    t21.average_income average_income_2021,
	(t21.average_income - t17.average_income)*100.0/ t17.average_income income_difference
   FROM table_2021 t21 
    INNER JOIN 
    table_2020 t20 ON t20.post_code = t21.post_code
    INNER JOIN 
    table_2019 t19 ON t19.post_code = t21.post_code
    INNER JOIN 
    table_2018 t18 ON t18.post_code = t21.post_code
    INNER JOIN 
    table_2017 t17 ON t17.post_code = t21.post_code
	ORDER BY income_difference DESC;

/* Second method provides one exact post_code with maximum income_differnce */	
SELECT query_2.post_code, query_2.income_difference FROM 
(SELECT MAX((t21.average_income - t17.average_income)*100.0/ t17.average_income) income_difference
		FROM table_2021 t21
		INNER JOIN 
    table_2017 t17 ON t17.post_code = t21.post_code) query_1
join (SELECT t21.post_code post_code, (t21.average_income - t17.average_income)*100.0/ t17.average_income income_difference
	 FROM table_2021 t21
	 INNER JOIN 
    table_2017 t17 ON t17.post_code = t21.post_code) query_2
	ON query_1.income_difference = query_2.income_difference

	

	
	
	;
	