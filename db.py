import sqlite3
import datetime
import hashlib

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class Tutorial:
    '''
    Has a list of external resources, unit_id, title, isImage(main media video or img), main image/video, uid, and paragraph list
    '''
    def save(self):
        pass

    def add(self):
        pass

    def delete(self):
        cur.execute('''DELETE FROM tutorials WHERE id = ?''', (self.id,))
        conn.commit()

    @staticmethod
    def get(id):
        pass


class User:
    '''
    has a name, image, and completed and flagged tutorial lists.
    '''
    def init(self, password, shouldHash=True):
        self.password = password
        if shouldHash:
            # Hash the hash 100 times for additional security!
            for a in range(100):
                hasher = hashlib.sha256()
                hasher.update(self.password.encode())
                self.password = hasher.hexdigest()

    def save(self):
        pass

    def add(self):
        pass

    def delete(self):
        cur.execute('''DELETE FROM users WHERE id = ?''', (self.id,))
        conn.commit()

    def getFlaggedTutorials(self):
        '''
        Get an array of Tutorial Objects corresponding to the user's flagged tutorials
        '''
        cur.execute('''SELECT flagged FROM users WHERE id = ?''', (self.id,))
        row = cur.fetchone()
        flagged = ''
        if row:
            flagged = row[0]
        flagged = flagged.split('|')
        tutorials = []
        for tut_id in flagged:
            t = Tutorial.get(int(tut_id))
            if t:
                tutorials.append(t)
        return tutorials

    def getSuggestedTutorials(self):
        '''
        Get an array of Tutorial Objects corresponding to the incompleted tutorials of the user
        '''
        # Get the completed tutorial ids
        cur.execute('''SELECT completed FROM users WHERE id = ?''', (self.id,))
        row = cur.fetchone()
        completed = ''
        if row:
            completed = row[0]
        completed = completed.split('|')
        # Generate the condition statement for the SQL
        condition = " && ".join(["id != {}".format(int(i)) for i in completed])
        # Pull the tutorials from the database
        cur.execute('''SELECT * FROM tutorials WHERE {}'''.format(condition))
        rows = cur.fetchall()
        tutorials = []
        for row in rows:
            uid, unitId, text, image, isImage = row
            # If there are fewer than 5 tutorials currently in the list
            # then append the tutorial
            if len(tutorials) < 5:
                tutorials.append(Tutorial.get(uid))
        # Return the tutorial list.
        return tutorials

    @staticmethod
    def get(id):
        pass

class Unit:
    '''
    Has a title and uid
    '''
    def save(self):
        pass

    def add(self):
        pass

    def delete(self):
        cur.execute('''DELETE FROM units WHERE id = ?''', (self.id,))
        conn.commit()

    @staticmethod
    def get(id):
        pass

class Resource:
    '''
    has a title, tutorial_id, and a link
    '''
    def save(self):
        pass

    def add(self):
        pass

    def delete(self):
        cur.execute('''DELETE FROM resources WHERE id = ?''', (self.id,))
        conn.commit()

    @staticmethod
    def get(id):
        pass
