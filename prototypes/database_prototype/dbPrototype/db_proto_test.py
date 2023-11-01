"""
importing python class that handles db operation
this python program is used exclusively to test DbProto
"""
import db_proto as db

recipe_dict = [
    {"recipe": "test1", "ingredients": ["chicken", "peas"], "url": "123"},
    {"recipe": "test2", "ingredients": ["chicken", "peas"], "url": "1234"},
    {"recipe": "test3", "ingredients": ["chicken", "rice"], "url": "12345"},
]
#
user_list = ["chicken", "peas", "rice"]

dbOps = db.DbProto("database_prototype/dbPrototype/protoDB.db")


def main():
    """
    main function
    """
    # create all tables
    dbOps.cur.execute(dbOps.sql_create_recipe_table_stmt)
    dbOps.cur.execute(dbOps.sql_create_ingredients_table_stmt)
    dbOps.cur.execute(dbOps.sql_create_recipe_ingredients_table_stmt)
    dbOps.cur.execute(dbOps.sql_create_user_ingredients_stmt)

    # populate tables with data
    dbOps.populate_recipes(recipe_dict)
    dbOps.populate_ingredients(recipe_dict)
    dbOps.populate_recipe_ingredients(recipe_dict)
    dbOps.populate_user_ingreds(user_list)

    # queries
    dbOps.cur.execute("select * from recipes")
    for i in dbOps.cur.fetchall():
        print(i)
    print("\n")
    dbOps.cur.execute("select * from ingredients")
    for i in dbOps.cur.fetchall():
        print(i)
    print("\n")
    dbOps.cur.execute("select * from recipe_ingredients")
    for i in dbOps.cur.fetchall():
        print(i)
    print("\n")
    dbOps.cur.execute(dbOps.sql_retrieve_recipes_stmt)
    for i in dbOps.cur.fetchall():
        print(i)

    dbOps.cur.execute("drop table recipes")
    dbOps.cur.execute("drop table ingredients")
    dbOps.cur.execute("drop table recipe_ingredients")


main()
