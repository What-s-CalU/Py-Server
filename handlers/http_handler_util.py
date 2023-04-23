import handlers.sql_handler       as sql_h
import handlers.threading_handler as thread_h
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

# takes a user_id integer paramater and a category_id integer paramater and inserts a subcription into the user_Category_sbuscription table
def insert_new_user_category_subscription(user_id, category_id):
    thread_h.s_print(f"user_id: {user_id}, category_id: {category_id}")
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


def delete_user_event(event_id):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        DELETE FROM EVENTS
        WHERE
            ID = ?
        """,
        (
           event_id,
        )
    )
    



# function to insert a new event into the database
def query_all_calu_events():
    events_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT
            EVENTS.TITLE as title
        FROM EVENTS
        WHERE
            USER_ID IS NULL
        """,
        ()
    )
    return events_query.fetchall()



# function to insert a new event into the database
def insert_new_calu_event(start_time, end_time, title, description, category_id, is_custom, user_id, flag, events_updated, do_not_fill):
    value = False

    if(not(start_time == None or end_time == None or title == None or description == None or category_id == None or is_custom == None)):

            was_found = False

            for event_title in query_all_calu_events():
                if(str(event_title[0]) == title):
                    was_found = True

            

            if(not(was_found)):
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    """
                    INSERT INTO EVENTS 
                    (
                        START_TIME, 
                        END_TIME,
                        TITLE,
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
                        ?
                    )
                    """,
                    (
                        start_time,
                        end_time,
                        title,
                        " ",
                        category_id,
                        is_custom,
                        user_id,
                        flag
                    )
                )

                if(not(do_not_fill)):
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        """
                        UPDATE EVENTS
                        SET
                            DESCRIPTION = ?
                        WHERE
                            TITLE = ? AND
                            USER_ID is NULL
                        """,
                        (
                            description,
                            title
                        )
                    )

                thread_h.s_print("[SCRAPER] [EVENT] <Added event \"{}\".>".format(title))
            else:
                needs_updated = True
                for event_title in events_updated:
                    if(event_title == title):
                        needs_updated = False
                
                # Always replaces events with their most up to date counterparts. 
                if(needs_updated):
                    events_updated.append(title)
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        """
                        UPDATE EVENTS
                        SET
                            START_TIME  = ?,
                            END_TIME    = ?,
                            TITLE       = ?,
                            CATEGORY_ID = ?,
                            IS_CUSTOM   = ?,
                            USER_ID     = ?,
                            FLAG        = ?
                        WHERE
                            TITLE = ? AND
                            USER_ID is NULL
                        """,
                        (
                            start_time,
                            end_time,
                            title,
                            category_id,
                            is_custom,
                            user_id,
                            flag,
                            title
                        )
                    )

                    if(not(do_not_fill)):
                        sql_h.sql_execute_safe_insert(
                            "database/root.db",
                            """
                            UPDATE EVENTS
                            SET
                                DESCRIPTION = ?
                            WHERE
                                TITLE = ? AND
                                USER_ID is NULL
                            """,
                            (
                                description,
                                title
                            )
                        )

                    thread_h.s_print("[SCRAPER] [EVENT] <Updated event \"{}\".>".format(title))
                    # value = True
                else:
                    thread_h.s_print("[SCRAPER] [EVENT] <Already updated event \"{}\"; skipping.>".format(title))
    return value
 


# function to insert a new event into the database
def insert_new_event(start_time, end_time, title, description, category_id, is_custom, user_id, flag):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        INSERT INTO EVENTS 
        (
            START_TIME, 
            END_TIME, 
            TITLE, 
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
            ?
        )""",
        (
            start_time,
            end_time,
            title,
            description,
            category_id,
            is_custom,
            user_id,
            flag
        )
    )

    event_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT ID
        FROM EVENTS
        WHERE START_TIME = ? AND
              END_TIME = ? AND
              TITLE = ? AND
              DESCRIPTION = ? AND
              CATEGORY_ID = ? AND
              IS_CUSTOM = ? AND
              USER_ID = ?
        """,
        (
            start_time,
            end_time,
            title,
            description,
            category_id,
            is_custom,
            user_id
        )
    )

    event_id_result = event_id_query.fetchone()
    thread_h.s_print(event_id_result)
    return {'ID': event_id_result[0]}


 
# function to insert a new event into the database
def edit_event(start_time, end_time, title, description, category_id, is_custom, user_id, flag, event_id):
    
    
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        UPDATE EVENTS SET
            START_TIME=?,
            END_TIME=?,
            TITLE=?,
            DESCRIPTION=?,
            CATEGORY_ID=?,
            IS_CUSTOM=?,
            USER_ID=?,
            FLAG=?
            WHERE ID=?""",
        (
            start_time,
            end_time,
            title,
            description,
            category_id,
            is_custom,
            user_id,
            flag,
            event_id
        )
    )

    event_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT ID
        FROM EVENTS
        WHERE START_TIME = ? AND
              END_TIME = ? AND
              TITLE = ? AND
              DESCRIPTION = ? AND
              CATEGORY_ID = ? AND
              IS_CUSTOM = ? AND
              USER_ID = ?
        """,
        (
            start_time,
            end_time,
            title,
            description,
            category_id,
            is_custom,
            user_id
        )
    )

    event_id_result = event_id_query.fetchone()
    thread_h.s_print(event_id_result)
    return {'ID': event_id_result[0]}



def insert_new_category(user_id, color, name):
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        INSERT INTO CATEGORIES 
        (
            USER_ID, 
            COLOR, 
            NAME
        )
        VALUES 
        (
            ?,
            ?, 
            ?
        )""",
        (
            user_id,
            color,
            name
        )
    )

    category_id_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT ID
        FROM CATEGORIES
        WHERE USER_ID = ? AND
              COLOR = ? AND
              NAME = ?
        """,
        (
            user_id,
            color,
            name
        )
    )

    category_id = category_id_query.fetchone()[0]
    return category_id

# function which returns a list of dicts of events user is subscribed to
def get_user_subscribed_events(user_id):
    # Fetch events from the database
    events_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT EVENTS.ID as id,
               EVENTS.START_TIME as start_time,
               EVENTS.END_TIME as end_time,
               EVENTS.TITLE as title,
               EVENTS.DESCRIPTION as description,
               CATEGORIES.ID AS categoryID,
               EVENTS.IS_CUSTOM as isCustom,
               EVENTS.FLAG as flag
        FROM EVENTS
        JOIN USER_CATEGORY_SUBSCRIPTIONS ON EVENTS.CATEGORY_ID = USER_CATEGORY_SUBSCRIPTIONS.CATEGORY_ID
        JOIN CATEGORIES ON EVENTS.CATEGORY_ID = CATEGORIES.ID
        WHERE USER_CATEGORY_SUBSCRIPTIONS.USER_ID = ?
        """,
        (user_id,)
    )
    events_result = events_query.fetchall()
    thread_h.s_print(events_result)
    # Convert the result to a list of dicts
    events = query_result_to_dict_list(events_result, events_query.description)

    return events

def get_user_subscribed_categories(user_id):
    # Fetch categories from the database
    categories_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT CATEGORIES.ID as id,
               CATEGORIES.NAME as name,
               CATEGORIES.COLOR as color,
               CATEGORIES.USER_ID as user_id
        FROM CATEGORIES
        JOIN USER_CATEGORY_SUBSCRIPTIONS ON CATEGORIES.ID = USER_CATEGORY_SUBSCRIPTIONS.CATEGORY_ID
        WHERE USER_CATEGORY_SUBSCRIPTIONS.USER_ID = ?
        """,
        (user_id,)
    )
    categories_result = categories_query.fetchall()
    thread_h.s_print(categories_result)
    # Convert the result to a list of dicts
    categories = query_result_to_dict_list(categories_result, categories_query.description)

    return categories

def get_categories_with_subscription_status(user_id):
    # Get categories with null user_id and their subscription status
    categories_query = sql_h.sql_execute_safe_search(
         "database/root.db",
        """
        SELECT  C.ID as id,
                C.NAME as name,
                C.COLOR as color,
                C.USER_ID as user_id,
               CASE WHEN UCS.CATEGORY_ID IS NOT NULL THEN 1 ELSE 0 END AS is_subscribed
        FROM CATEGORIES C
        LEFT JOIN USER_CATEGORY_SUBSCRIPTIONS UCS ON C.ID = UCS.CATEGORY_ID AND UCS.USER_ID = ?
        WHERE C.USER_ID IS NULL
        """,
        (user_id,)
    )
    categories_result = categories_query.fetchall()

    categories = query_result_to_dict_list(categories_result, categories_query.description)

    thread_h.s_print(categories)
    return categories

def get_calu_category_events(category_id):
    # Fetch events from the database
    events_query = sql_h.sql_execute_safe_search(
        "database/root.db",
        """
        SELECT EVENTS.ID as id,
               EVENTS.START_TIME as start_time,
               EVENTS.END_TIME as end_time,
               EVENTS.TITLE as title,
               EVENTS.DESCRIPTION as description,
               EVENTS.CATEGORY_ID AS categoryID,
               EVENTS.IS_CUSTOM as isCustom,
               EVENTS.FLAG as flag
        FROM EVENTS
        WHERE EVENTS.CATEGORY_ID = ?
        """,
        (category_id,)
    )
    events_result = events_query.fetchall()
    thread_h.s_print(events_result)
    # Convert the result to a list of dicts
    events = query_result_to_dict_list(events_result, events_query.description)

    return events

def delete_category_and_associated_data(user_id, category_id):
    # Delete user subscriptions associated with the category_id
    delete_user_category_subscription(user_id, category_id)

    # Delete events associated with the category_id
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        DELETE FROM EVENTS
        WHERE CATEGORY_ID = ?
        """,
        (category_id,)
    )

    # Delete the category
    sql_h.sql_execute_safe_insert(
        "database/root.db",
        """
        DELETE FROM CATEGORIES
        WHERE ID = ?
        """,
        (category_id,)
    )

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
