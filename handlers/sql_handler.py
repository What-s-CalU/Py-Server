'''
    Basic wrapper functions for the sqlite3 library included with python 3. 
    References: https://docs.python.org/3/library/sqlite3.html
    For reading SQL in Visual Studio Code: Use the SQLite extension. 
    For editing SQL in a traditional editor: https://sqlitebrowser.org/dl/
'''

import sqlite3

def sql_execute_command(database, command, shouldCommit=True, shouldResolve=False):
    value = False
    # establish a connection and execute the command
    # safety check should go here in the future
    sql_connection = sqlite3.connect(database)
    sql_cursor     = sql_connection.cursor()
    sql_cursor.execute(command)

    # for INSERT commands
    if(shouldCommit):
        sql_connection.commit()

    # generate resolution table (should support a custom resolve command)
    resolve = sql_cursor.execute("SELECT name FROM sqlite_master")
    
    # return a status unless the invoker wants the resolution table
    if(not(shouldResolve)):
        value = bool(not(resolve.fetchone() is None))
    else:
        value = resolve.fetchall()
    return value



# Subfunctions with plain english names that invoke sql_execute_command()
def sql_execute_search(database, command):
    return sql_execute_command(database, command, False, True)


def sql_execute_insert(database, command, shouldResolve=True):
    return sql_execute_command(database, command, True, shouldResolve)


# running this once creates the .db file if it doesn't exist already. 
# return value is a boolean by default, but can also return the resolution of the command.
def main():
    value = sql_execute_command("tutorial.db", "CREATE TABLE movie(title, year, score)")


# For unit testing (see above)
if __name__ == "__main__":
    main()