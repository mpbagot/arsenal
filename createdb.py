import sqlite3
import datetime

open('database.db', 'w').close()

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
  CREATE TABLE users (
  	id INTEGER NOT NULL,
  	username TEXT NOT NULL,
  	password TEXT NOT NULL,
    completed TEXT,
    flagged TEXT,
    class INTEGER,
    is_teacher BOOLEAN,
  	PRIMARY KEY (id)
);
'''
)

cur.execute('''
    CREATE TABLE classes (
        id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY (id)
    );
''')

cur.execute('''
  CREATE TABLE units (
  	id INTEGER NOT NULL,
  	title TEXT NOT NULL,
  	PRIMARY KEY (id)
);
'''
)

cur.execute('''
  CREATE TABLE tutorials (
  	id INTEGER NOT NULL,
  	unitid INTEGER NOT NULL,
  	text TEXT,
    image TEXT,
    is_image BOOLEAN NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (unitid) REFERENCES units(id) ON DELETE CASCADE
);
'''
)

cur.execute('''
  CREATE TABLE resources (
    id INTEGER NOT NULL,
    tutorial_id INTEGER NOT NULL,
    link TEXT NOT NULL,
    title TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (tutorial_id) REFERENCES tutorials(id) ON DELETE CASCADE
);
'''
)
conn.commit()
