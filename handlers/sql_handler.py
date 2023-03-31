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
    sql_return     = sql_cursor.execute(command)

    # for INSERT commands
    if(shouldCommit):
        sql_connection.commit()
    
    # return a status unless the invoker wants the resolution table
    # if not, the return type becomes BOOL
    if(not(shouldResolve)):
        value = bool(not(sql_return.fetchone() is None) or (sql_cursor.rowcount > 0))
    else:
        value = sql_return

    # clean up connections. 
    sql_cursor.close()
    sql_connection.close()
    return value



# Subfunctions with plain english names that invoke sql_execute_command()
def sql_execute_search(database, command):
    return sql_execute_command(database, command, False, True)


def sql_execute_insert(database, command, shouldResolve=False):
    return sql_execute_command(database, command, True, shouldResolve)


# running this once creates the .db file if it doesn't exist already. 
# return value is a boolean by default, but can also return the resolution of the command.
def main():
    value = sql_execute_command("tutorial.db", "CREATE TABLE movie(title, year, score)")


# For unit testing (see above)
if __name__ == "__main__":
    main()