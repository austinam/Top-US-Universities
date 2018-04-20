import unittest
from final import *
import json
import requests

class TestDatabase(unittest.TestCase):

    #First test function, 5 assert statements, testing that Colleges is correctly set up
    def test_colleges_table(self):
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        select = 'SELECT Name FROM Colleges'
        results = cur.execute(select)
        lst = results.fetchall()
        self.assertIn(('Stanford University',), lst)
        self.assertEqual(len(lst), 150)


        select2 = '''
        SELECT Rank, Name, Location, Acceptance, Enrollment
        FROM Colleges
        WHERE Name = "Duke University"
        '''
        results2 = cur.execute(select2)
        lst2 = results2.fetchall()
        self.assertEqual(lst2[0][2], 'Durham  NC')
        self.assertIn(12, lst2[0])
        self.assertNotEqual(lst2[0][0], 1)

        conn.close()

    #Second test function, testing set up of regions table, 4 assert statements (9 total)
    def test_regions_table(self):
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        select3 = 'SELECT State, Region FROM Regions'
        results3 = cur.execute(select3)
        lst3 = results3.fetchall()
        self.assertIn(('MI', ' midwest'), lst3)
        self.assertEqual(len(lst3), 51)

        select4 = '''
        SELECT State
        FROM Regions
        WHERE Region = ' south'
        '''
        results4 = cur.execute(select4)
        lst4 = results4.fetchall()
        self.assertIn(('TN',), lst4)
        self.assertNotIn(('VT',), lst4)

        conn.close()

    #Third test function, testing join, 2 assert statements, 11 total
    def test_join_tables(self):
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        select5 = '''
        SELECT r.Region, Count(c.Name)
        FROM Regions as r
        JOIN Colleges as c
        ON r.State = c.State
        WHERE r.Region = ' south'
        GROUP BY r.Region
        '''
        results5 = cur.execute(select5)
        lst5 = results5.fetchall()
        self.assertEqual(lst5[0][1], 34)
        self.assertEqual(len(lst5), 1)

        conn.close()

class TestProcessCommand(unittest.TestCase):

    #These test sql queries from process commands (since nothing is returned from those functions other than plotly), 10 assert statements, 21 total
    def test_regions_sql(self):
        sql_st = 'SELECT t.Region, COUNT(t.Name) FROM (SELECT r.Region, c.Name FROM Colleges as c JOIN Regions as r ON c.State = r.State LIMIT 1) as t GROUP BY t.Region'
        out = cur.execute(sql_st)
        output = out.fetchall()
        self.assertEqual(output[0][0], ' west')
        self.assertEqual(output[0][1], 1)

    def test_acp_sql(self):
        sql_st2 = 'SELECT Rank, Acceptance FROM Colleges LIMIT 2'
        out2 = cur.execute(sql_st2)
        output2 = out2.fetchall()
        self.assertEqual(output2[1][0], 2)
        self.assertEqual(output2[1][1], '8%')

    def test_enroll_sql(self):
        sql_st3 = 'SELECT Name, Enrollment FROM Colleges LIMIT 3'
        out3 = cur.execute(sql_st3)
        output3 = out3.fetchall()
        self.assertEqual(output3[2][0], 'Harvard University')
        self.assertEqual(output3[2][1], 7151)

    def test_earnings(self):
        sql_st4 = 'SELECT Name, Median_Income_2years FROM Colleges LIMIT 4'
        out4 = cur.execute(sql_st4)
        output4 = out4.fetchall()
        self.assertEqual(output4[3][0], 'Yale University')
        self.assertEqual(output4[3][1], 60700)

    def test_ratio(self):
        sql_st5 = 'SELECT Name, Number_Students_per_FacultyMember FROM Colleges LIMIT 5'
        out5 = cur.execute(sql_st5)
        output5 = out5.fetchall()
        self.assertEqual(output5[4][0], 'Rice University')
        self.assertEqual(output5[4][1], 6)

class TestCollegeClass(unittest.TestCase):

    #Last class, testing class configuration, 9 asserts, 30 total
    def test_class_constructor(self):
        c1 = College(19, "University of Southern California", "Los Angeles  CA", "17%", "18195", "9", "https://www.niche.com/colleges/university-of-southern-california/cost/", "https://www.niche.com/colleges/university-of-southern-california/after-college/")
        self.assertEqual(c1.rank, 19)
        self.assertEqual(c1.name, "University of Southern California")
        self.assertEqual(c1.location, "Los Angeles  CA")
        self.assertEqual(c1.accept_rate, "17%")
        self.assertEqual(c1.enroll, "18195")
        self.assertEqual(c1.ratio, "9")
        self.assertEqual(c1.price_in, "52283")
        self.assertEqual(c1.price_out, "52283")
        self.assertEqual(c1.median_2_yr_earn, "52800")

unittest.main()
