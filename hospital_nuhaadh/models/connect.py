import cx_Oracle
from odoo import models, fields

con = cx_Oracle.connect('apps/apps@192.168.2.161:1521/ebsdb')


class TestProject(models.Model):
    _name = "connect.test"
    _description = "Oracle database test intergration"
    _rec_name = "usersname"

    usersname = fields.Char(string="User Name")
    usersid = fields.Char("User ID")

    def insert_button(self):
        try:
            cur = con.cursor()
            cur.arraysize = 100
            cur.execute("select user_name, user_id from fnd_user")
            result = cur.fetchall()
            for xyz in result:
                print("user_name.....", xyz[1])
                self.env.cr.execute(f"INSERT INTO connect_test (usersname, usersid) VALUES {xyz[0], xyz[1]}")
            self.env.cr.commit()
            con.autocommit = True

        finally:
            cur.close()


# con = cx_Oracle.connect('apps/apps@192.168.2.161:1521/ebsdb')
# print("Database version:", con.version)
#
# ver = con.version.split(".")
# print (ver)
# start = time.time()
# cur = con.cursor()
# cur.arraysize = 100
# cur.execute("select user_name, user_id  from fnd_user where user_name like 'A%' " )  #table bigtab is a table with a large number of rows
# res = cur.fetchall()
# print("Two",res)  # uncomment to display the query results
# elapsed = (time.time() - start)
# print(elapsed, " seconds")
# cur.close()
#
# con.close()

# apps/%s@//192.168.2.161:1521/ebsdb
