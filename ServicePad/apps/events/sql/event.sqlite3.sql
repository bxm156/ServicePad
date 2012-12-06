/* create different events at the server start, these events are just for testing */
/* for the time being all the events are owned by the first user */

/* NOTE THESE EVENTS ARE ONLY ADDED TO SQLITE3! THEY ARE NOT ADDED TO PRODUCTION SERVER! SEE event.mysql.sql */
INSERT INTO events_event (id, name, short_description, long_description, address, city, state, postalzip, public, category_id, start_time, end_time, list_date, owner_id)
    VALUES (1,
        "HORSE",
        "I'M A HORSE",
        "SUCK MY DICK, I'M A HORSE",
        'here',
        'there',
        'IN',
        111111,
        "True",
        1,
        '11-11-2012',
        '11-13-2012',
        '11-11-2012',
        0);
INSERT INTO events_event (id, name, short_description, long_description, address, city, state, postalzip, public, category_id, start_time, end_time, list_date, owner_id)
    VALUES (2,
        "Dog Shelter",
        "Walk dogs",
        "We're going to the dog shelter to walk dogs. Help the dogs enjoy themselves and have a bit of fun",
        "9500 Sweet Valley Dr.",
        "Cleveland",
        "OH",
        44125,
        "True",
        1,
        "1-05-2013",
        "1-08-2013",
        "1-05-2013",
        0); 
INSERT INTO events_event (id, name, short_description, long_description, address, city, state, postalzip, public, category_id, start_time, end_time, list_date, owner_id)
    VALUES (3,
        "Clean up Wade Lagoon",
        "Make Wade Lagoon a beautiful place",
        "Pickup trash and turn the wade lagoon into the beautiful place we all know it can be!",
        "Martin Luther King Jr Dr",
        "Cleveland",
        "OH",
        44106,
        "True",
        1,
        "1-20-2013",
        "1-23-2013",
        "1-20-2013",
        0);
