import handlers.sql_handler as sql_h

# takes a string paramater and returns the user_id of that string in the database
def get_user_id(username):
    user_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        "SELECT ID FROM USERS WHERE NAME IS ?",
        (username,)
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
def delete_user_category_subscription(user_id, category_id):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        DELETE FROM USER_CATEGORY_SUBSCRIPTIONS
        WHERE
            USER_ID = ? AND
            CATEGORY_ID = ?
        """,
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

# function which returns a list of dicts of events user is subscribed to
def get_user_subscribed_events(user_id):
    # Fetch events from the database
    events_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT EVENTS.START_TIME as start_time,
               EVENTS.END_TIME as end_time,
               EVENTS.TITLE as title,
               EVENTS.COLOR as color,
               EVENTS.DESCRIPTION as description,
               CATEGORIES.NAME AS category,
               EVENTS.IS_CUSTOM as isCustom
        FROM EVENTS
        JOIN USER_CATEGORY_SUBSCRIPTIONS ON EVENTS.CATEGORY_ID = USER_CATEGORY_SUBSCRIPTIONS.CATEGORY_ID
        JOIN CATEGORIES ON EVENTS.CATEGORY_ID = CATEGORIES.ID
        WHERE USER_CATEGORY_SUBSCRIPTIONS.USER_ID = ?
        """,
        (user_id,)
    )
    events_result = events_query.fetchall()
    print(events_result)
    # Convert the result to a list of dicts
    events = query_result_to_dict_list(events_result, events_query.description)

    return events

def get_categories_with_subscription_status(user_id):
    # Get categories with null user_id
    null_user_categories_query = '''
        SELECT ID, NAME
        FROM CATEGORIES
        WHERE USER_ID IS NULL
    '''
    null_user_categories_result = sql_h.sql_execute_safe_search("database/root.db", null_user_categories_query, ()).fetchall()

    # Get the user's subscribed categories
    subscribed_categories_query = '''
        SELECT CATEGORY_ID
        FROM USER_CATEGORY_SUBSCRIPTIONS
        WHERE USER_ID = ?
    '''
    subscribed_categories_result = sql_h.sql_execute_safe_search("database/root.db", subscribed_categories_query, (user_id,)).fetchall()

    # Convert the results to sets for easier processing
    null_user_categories = {(row[0], row[1]) for row in null_user_categories_result}
    subscribed_category_ids = {row[0] for row in subscribed_categories_result}

    # Process the results to create the final list of categories with subscription status
    categories_data = []
    for category_id, category_name in null_user_categories:
        is_subscribed = int(category_id in subscribed_category_ids)
        categories_data.append({'id': category_id, 'name': category_name, 'is_subscribed': is_subscribed})

    print(categories_data)
    return categories_data

def get_calu_category_events(category_name):
    # Fetch events from the database
    events_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT EVENTS.START_TIME as start_time,
               EVENTS.END_TIME as end_time,
               EVENTS.TITLE as title,
               EVENTS.COLOR as color,
               EVENTS.DESCRIPTION as description,
               CATEGORIES.NAME AS category,
               EVENTS.IS_CUSTOM as isCustom
        FROM EVENTS
        JOIN CATEGORIES ON EVENTS.CATEGORY_ID = CATEGORIES.ID
        WHERE EVENTS.IS_CUSTOM = 0 AND CATEGORIES.NAME = ?
        """,
        (category_name,)
    )
    events_result = events_query.fetchall()
    print(events_result)
    # Convert the result to a list of dicts
    events = query_result_to_dict_list(events_result, events_query.description)

    return events

# function to convert query result into list of dict
def query_result_to_dict_list(query_result, query_description):
    events_list = []
    column_names = []
    
    # Get the column names from the query description
    for column in query_description:
        column_names.append(column[0])

    # Iterate through each row and column in the query result
    for row in query_result:
        event_dict = {}
        
        for i in range(len(column_names)):
            column_name = column_names[i]
            event_dict[column_name] = row[i]
        
        events_list.append(event_dict)

    return events_list
