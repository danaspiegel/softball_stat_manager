from dmigrations.mysql import migrations as m

migration = m.Migration(sql_up="INSERT INTO mock VALUES (5)", sql_down="")
