# finalproject

Data source: Niche College Rankings
•	https://www.niche.com/colleges/search/best-colleges/
•	Contains information on the top universities. From this site I crawled into the different colleges sites and scraped data there, then crawled further into each specific college website to sites about tuition and income after graduation. There is not an api key or any requirements necessary to access data from this page. 

After this information was scraped, it was added to a csv file with all relevant information on the top 150 colleges. 

A separate function took information on all 51 states and what region they were in. This was loaded into a csv. 

These two csv files were loaded into a database. The foreign key of the colleges database is state, and was linked to the regions table.

Important functions/classes:

College class - makes instance of all data related to one college 

The main functions are:
	get_data() - scrapes data from website
    load_school_data() - loads data to college_data.csv
    create_region_csv() - loads data into regions.csv
    create_region_table(regions_csv) - creates region table from csv
    create_colleges(schools_csv) - creates colleges table from csv
    foreign_key() - creates foreign key
    different process commands functions for different types of user input
    interactive() - does the interactive portion of the code

Presentation options for users: 
•	User is given the option of how many schools they would like to search for. Then the following options are:
   - Breakdown of top universities by region (pie-chart)
   - Breakdown of top universities by tuition per year (either in-state or out of state option) (scatter plot)
   - Breakdown of top universities by acceptance rate (line graph)
   - Breakdown of top universities by total enrollment (scatter plot)
   - Breakdown of top universities by student:faculty ratio (histogram)
   - Breakdown of median income after graduation (scatter plot)

When the user inputs the option, the database will be queried and this information is used to create the graph in plotly. 

For plotly the user must create an account and get an api key (directions in link) - 
https://plot.ly/python/getting-started/


Helpful information for the user----

First Input:

The options available to the user for the first input is a number 1 through 150.

The program contains information on the top 150 schools in the US. If you enter ’10’
you will get information about the top 10 schools (by ranking).

Second Input: will return graphical displays of information about the number of columns selected in the first input.

The options for the second input are:

- regions: this will return a pie-chart showing the breakdown of where the the top x colleges and universities are located. The four regions are west, south, midwest, and northeast.

- acceptance: this will return a line graph that shows the different acceptance rates for the top x number of colleges and universities.

- enrollment: this will return a scatter plot of the different undergraduate enrollment numbers for the top x colleges and universities.

- income: this will return a scatter plot of the median income of students 2 years after graduation for the top x number of colleges and universities.

- student:faculty: this will return a bar graph of how many students there are per faculty member at the top x colleges and universities. 
 
- tuition: this will return a scatter plot of tuition at the top x colleges and universities. The user will be asked for a third input at this point:

	- Third Input: The user will be asked if they want to see data on in-state 		  tuition or out-of-state tuition. Enter ‘in’ for in-state tuition or ‘out’ 
	  for out-of-state tuition. 

After you see a graphical display out data you must again enter how many colleges you would like to see information on, and then what type again.

Enter ‘exit’ to quit the program. 

------

Things to be downloaded by the user to run the program (pip install x)
1) requests
2) json
3) BeautifulSoup
4) csv
5) plotly
6) sqlite3


