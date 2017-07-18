import sqlite3
import datetime
import hashlib
import random

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class Tutorial:
    '''
    Has a list of external resources, unit_id, title,
    isImage(main media video or img), main image/video, uid, and paragraph list
    '''
    def __init__(self, unitid, text, image, is_image=True, id=None):
        self.text = eval(text)
        self.unit_id = unitid
        self.image = image
        self.is_image = is_image
        self.id = id

    def __str__(self):
        return 'Tutorial(UnitID={}, image={}, is_image={}, id={})'.format(
                    self.unit_id, self.image, self.is_image, self.id)

    def save(self):
        if self.id is None:
            self.add()
        else:
            cur.execute('''UPDATE tutorials SET text = ?, unitid = ?, image = ?, is_image = ? WHERE id = ?''',
                        (str(self.text), self.unit_id, self.image, self.is_image, self.id))
        conn.commit()

    def add(self):
        cur.execute('''INSERT INTO tutorials (unitid, text, image, is_image) VALUES (?, ?, ?, ?)''',
                    (self.unit_id, str(self.text), self.image, self.is_image))
        self.id = cur.lastrowid

    def delete(self):
        cur.execute('''DELETE FROM tutorials WHERE id = ?''', (self.id,))
        conn.commit()

    def getResources(self):
        cur.execute('''SELECT id, tutorial_id FROM resources WHERE tutorial_id = ?''', (self.id, ))
        rows = cur.fetchall()
        resources = []
        for row in rows:
            uid, tutorial_id = row
            resources.append(Resource.get(uid))
        return resources

    @staticmethod
    def get(id):
        cur.execute('''SELECT * FROM tutorials WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row is None:
            return None
        id, unitid, text, image, is_image = row
        return Tutorial(unitid, text, image, bool(is_image), id)


class User:
    '''
    has a name, image, is_teacher, class (part of, not leading) and completed and flagged tutorial lists.
    '''
    def __init__(self, name, password, completed=[], flagged=[], current_class=None, is_teacher=False, id=None, should_hash=True):
        self.name = name
        self.id = id
        self.completed = completed
        self.flagged = flagged
        self.is_teacher = is_teacher
        self.current_class = current_class
        self.password = password
        if should_hash:
            # Hash the hash 10000 times for additional security!
            for a in range(10000):
                hasher = hashlib.sha256()
                hasher.update(self.password.encode())
                self.password = hasher.hexdigest()

    def __str__(self):
        return 'User(name={}, password={}, completed={}, flagged={}, isTeacher={}, class={}, id={})'.format(
        self.name, self.password, self.completed, self.flagged, self.is_teacher, self.current_class, self.id)

    def save(self):
        '''
        Save the user into the database.
        '''
        if self.id is None:
            self.add()
        else:
            cur.execute('''UPDATE users SET password = ?, completed = ?, flagged = ?, class = ? WHERE id = ?''',
                    (self.password, '|'.join(self.completed), '|'.join(self.flagged),self.current_class, self.id))

        conn.commit()

    def add(self):
        cur.execute('''INSERT INTO  users (username, password, completed, flagged, is_teacher, class)
                    VALUES (?, ?, ?, ?, ?, ?);''',
                    (self.name, self.password, '|'.join(self.completed), '|'.join(self.flagged),
                    self.is_teacher, self.current_class))
        self.id = cur.lastrowid

    def delete(self):
        cur.execute('''DELETE FROM users WHERE id = ?''', (self.id,))
        conn.commit()

    def getFlaggedTutorials(self):
        '''
        Get an array of Tutorial Objects corresponding to the user's flagged tutorials
        '''
        tutorials = []
        for tut_id in self.flagged:
            t = Tutorial.get(int(tut_id))
            if t:
                tutorials.append(t)
        return tutorials

    def getSuggestedTutorials(self):
        '''
        Get an array of Tutorial Objects corresponding to the incompleted tutorials of the user
        '''
        # Generate the condition statement for the SQL
        condition = " && ".join(["id != {}".format(int(i)) for i in self.completed])
        # Pull the tutorials from the database
        cur.execute('''SELECT id, image FROM tutorials WHERE ?''', (condition,))
        rows = cur.fetchall()
        tutorials = []
        for row in rows:
            uid, image = row
            # If there are fewer than 5 tutorials currently in the list
            # then append the tutorial
            if len(tutorials) < 5:
                tutorials.append(Tutorial.get(uid))
        # Return the tutorial list.
        return tutorials

    def getCompletedTutorials(self):
        '''
        Get an array of Tutorial Objects corresponding to the completed tutorials of the user.
        '''
        # Generate the condition statement for the SQL
        condition = " && ".join(["id = {}".format(int(i)) for i in self.completed])
        # Pull the tutorials from the database
        cur.execute('''SELECT id, image FROM tutorials WHERE ?''', (condition,))
        rows = cur.fetchall()
        tutorials = []
        for row in rows:
            uid, image = row
            tutorials.append(Tutorial.get(uid))
        # Return the tutorial list.
        return tutorials

    def getTutorials(self):
        '''
        Get the Tutorial objects for the student details page
        '''
        flagged = self.getFlaggedTutorials()
        completed = self.getCompletedTutorials()
        cur.execute('''SELECT id, image from tutorials''')
        rows = cur.fetchall()
        # Get all of the tutorials into an array
        tutorials = []
        for row in rows:
            uid, image = row
            tutorials.append(Tutorial.get(uid))
        # Get all of the incompleted and unflagged tutorials
        tutorials_not_special = []
        for t in tutorials:
            g = True
            # Check if the tutorial is completed or flagged
            for a in completed+flagged:
                if a.id == t.id:
                    g = False
                    break
            # If it's not, append it to the new array
            if g:
                tutorials_not_special.append(t)
        return (flagged, completed+tutorials_not_special)

    @staticmethod
    def get(id):
        cur.execute('''SELECT * FROM users WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row is None:
            return None
        uid, name, password, completed, flagged, current_class, is_teacher = row
        flagged = [int(a) for a in flagged.split('|') if a]
        completed = [int(a) for a in completed.split('|') if a]
        is_teacher = bool(is_teacher)
        return User(name, password, completed, flagged, current_class, is_teacher, uid, False)

    @staticmethod
    def getByName(name):
        cur.execute('''SELECT * FROM users WHERE username = ?''', (name,))
        row = cur.fetchone()
        if row is None:
            return None
        uid, name, password, completed, flagged, current_class, is_teacher = row
        flagged = [int(a) for a in flagged.split('|') if a]
        completed = [int(a) for a in completed.split('|') if a]
        is_teacher = bool(is_teacher)
        return User(name, password, completed, flagged, current_class, is_teacher, uid, False)

class Class:
    '''
    has an id, teacher_id
    '''
    def __init__(self, teacher_id, password=None, id=None):
        self.id = id
        self.password = password
        self.teacher_id = teacher_id

    def __str__(self):
        return 'Class(teacher_id={}, password={}, id={})'.format(self.teacher_id, self.id)

    def save(self):
        if self.id is None:
            self.add()
        else:
            cur.execute('UPDATE classes SET teacher_id = ? WHERE id = ?', (self.teacher_id, self.id))
        conn.commit()

    def add(self):
        self.password = Class.getUniquePassword() if self.password is None else self.password
        cur.execute('''INSERT INTO classes (teacher_id, password) VALUES (?, ?)''', (self.teacher_id, self.password))
        self.id = cur.lastrowid

    def delete(self):
        cur.execute('''DELETE FROM classes WHERE id = ?''', (self.id,))
        conn.commit()

    def getStudents(self):
        cur.execute('''SELECT id, username FROM users WHERE class = ?''', (self.id,))
        rows = cur.fetchall()
        students = []
        for row in rows:
            id, username = row
            students.append(User.get(id))
        return students

    @staticmethod
    def get(id):
        cur.execute('''SELECT * FROM classes WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row is None:
            return None
        uid, teacher_id, password = row
        return Class(teacher_id, password, uid)

    @staticmethod
    def getByPassword(password):
        cur.execute('''SELECT * FROM classes WHERE password = ?''', (password,))
        row = cur.fetchone()
        if row is None:
            return None
        uid, teacher_id, password = row
        return Class(teacher_id, password, uid)

    @staticmethod
    def getUniquePassword():
        password = generatePassword()
        while Class.getByPassword(password):
            password = generatePassword()
        return password

class Unit:
    '''
    Has a title and uid
    '''
    def __init__(self, title, id=None):
        self.title = title
        self.id = id

    def __str__(self):
        return "Unit(title={}, id={})".format(self.title, self.id)

    def save(self):
        if self.id is None:
            self.add()
        else:
            cur.execute('''UPDATE units SET title = ? WHERE id = ?''', (self.title, self.id))
        conn.commit()

    def add(self):
        cur.execute('''INSERT INTO units (title) VALUES (?)''', (self.title,))
        self.id = cur.lastrowid

    def delete(self):
        cur.execute('''DELETE FROM units WHERE id = ?''', (self.id,))
        conn.commit()

    def getTutorials(self):
        cur.execute('''SELECT id, unitid FROM tutorials WHERE unitid = ?''', (self.id,))
        rows = cur.fetchall()
        tutorials = []
        for row in rows:
            uid, unitid = row
            tutorials.append(Tutorial.get(uid))
        return tutorials

    @staticmethod
    def get(id):
        cur.execute('''SELECT * FROM units WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row is None:
            return None
        id, title = row
        return Unit(title, id)

class Resource:
    '''
    has a title, tutorial_id, and a link
    '''
    def __init__(self, tutorial_id, link, title, id=None):
        self.id = id
        self.tutorial_id = tutorial_id
        self.link = link
        self.title = title

    def __str__(self):
        return 'Resource(tutorial={}, link="{}", title={})'.format(self.tutorial_id, self.link, self.title)

    def save(self):
        if self.id is None:
            self.add()
        else:
            cur.execute('''UPDATE resources SET tutorial_id = ?, link = ?, title = ? WHERE id = ?''',
                        (self.tutorial_id, self.link, self.title, self.id))
        conn.commit()

    def add(self):
        cur.execute('''INSERT INTO resources (tutorial_id, link, title) VALUES (?, ?, ?)''',
                    (self.tutorial_id, self.link, self.title))
        self.id = cur.lastrowid

    def delete(self):
        cur.execute('''DELETE FROM resources WHERE id = ?''', (self.id,))
        conn.commit()

    @staticmethod
    def get(id):
        cur.execute('''SELECT * FROM resources WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row is None:
            return None
        uid, tutorial_id, link, title = row
        return Resource(tutorial_id, link, title, uid)

def generatePassword():
    text = ''
    # Generate a random string of digits
    for a in range(random.randint(4, 10)):
        text += str(random.randint(0, 9))
    # Hash it to further randomise it
    for a in range(random.randint(1, 5)):
        hasher = hashlib.sha256()
        hasher.update(text.encode())
        text = hasher.hexdigest()
    # Return the first 8 characters
    return text[:8]


if __name__ == "__main__":
    #do testing here
    admin = User('Admin', 'meh', is_teacher=True)
    admin.save()
    print(admin)
    admin2 = User.get(1)
    print(admin2)
    c = Class(1)
    c.save()
    print(c)
    c2 = Class.get(1)
    print(c2)
    u = Unit('Title')
    u.save()
    print(u)
    u2 = Unit.get(1)
    print(u2)
    t = Tutorial(1, "['bleh', 'meh']", '')
    t.save()
    print(t)
    t2 = Tutorial(1, "['meh', 'bleh']", '')
    t2.save()
    print(t2)
    r = Resource(1, 'facebook.com', 'trash')
    r.save()
    print(r)
    r2 = Resource(1, 'github.com', 'best social media')
    r2.save()
    print(r2)
    r3 = Resource(2, 'meh.com', 'meh')
    r3.save()
    print(Tutorial.get(1).getResources())
    print(Tutorial.get(2).getResources())
