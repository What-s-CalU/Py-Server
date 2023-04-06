import handlers.sql_handler as sql_h

# takes a string paramater and returns the user_id of that string in the database
def get_user_id(username):
    user_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        "SELECT ID FROM USERS WHERE NAME IS ?",
        (username)
    )
    user_id_result = user_id_query.fetchone()

    if user_id_result is None:
        return None
    else:
        return user_id_result[0]


# takes a string paramater and a user_id and returns the category_id of the category associated with that name and user
def get_category_id(category, user_id):
    category_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT ID
        FROM CATEGORIES
        WHERE NAME IS ? AND USER_ID IS ?
        """,
        (category, user_id)
    )
    category_id_result = category_id_query.fetchone()

    if category_id_result is None:
        return None
    else:
        return category_id_result[0]

# takes a string paramater and a user_id integer and inserts a new category associated with a user_id into the categories table
def insert_new_category(category, user_id):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        INSERT INTO CATEGORIES 
        (
            NAME,
            USER_ID
        ) 
        VALUES 
        (
            ?,
            ?
        )
        """,
        (category, user_id)
    )

# takes a user_id integer paramater and a category_id integer paramater and inserts a subcription into the user_Category_sbuscription table
def insert_new_user_category_subscription(user_id, category_id):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        INSERT INTO USER_CATEGORY_SUBSCRIPTIONS
        (
            USER_ID,
            CATEGORY_ID
        )
        VALUES
        (
            ?,
            ?
        )""",
        (
            user_id,
            category_id
        )
    )

# function to insert a new event into the database
def insert_new_event(start_time, end_time, title, color, description, category_id, is_custom, user_id, flag):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        INSERT INTO EVENTS 
        (
            START_TIME, 
            END_TIME, 
            TITLE, 
            COLOR, 
            DESCRIPTION, 
            CATEGORY_ID, 
            IS_CUSTOM, 
            USER_ID, 
            FLAG
        )
        VALUES 
        (
            ?,
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?
        )""",
        (
            start_time,
            end_time,
            title,
            color,
            description,
            category_id,
            is_custom,
            user_id,
            flag
        )
    )
