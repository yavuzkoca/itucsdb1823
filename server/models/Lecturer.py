import datetime
import time
from server import conn, server, jwt, bcrypt
from slugify import slugify
import psycopg2.extras
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity


class Lecturer:
    name = ''
    email = ''
    user_id = ''
    id = 0
    slug = ''
    errors = []
    grade_distributions: []

    def __init__(self, _id=0, name='', email='', user_id=0, slug=''):
        self.id = int(_id)
        self.name = name
        self.email = email
        self.user_id = int(user_id)
        self.errors = []
        self.grade_distributions = []
        self.slug = slug

    def generate_slug(self, name):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        slug = slugify(name)
        slug_is_not_unique = True
        i = 2
        tslug = slug
        while slug_is_not_unique:
            cur.execute("SELECT * FROM lecturers WHERE slug=%s LIMIT 1", (slug,))
            found = cur.fetchone()
            if found is not None:
                slug = tslug + str(i)
                i += 1
            else:
                slug_is_not_unique = False
        return slug

    def get(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers WHERE slug=%s LIMIT 1", (self.slug,))
        lecturer = cur.fetchone()

        cur.execute("SELECT * FROM comments WHERE type_id=%s AND type='lecturers' ORDER BY created_at DESC", (lecturer['id'],))
        comments = cur.fetchall()
        for comment in comments:
            cur.execute("SELECT id, name, slug FROM users WHERE id=%s LIMIT 1", (comment['user_id'],))
            comment['user'] = cur.fetchone()

        lecturer['comments'] = comments

        cur.execute("SELECT * FROM grade_distributions WHERE lecturer_id=%s", (lecturer['id'],))
        self.grade_distributions = cur.fetchall()
        for grade_distribution in self.grade_distributions:
            cur.execute("SELECT * FROM terms WHERE id = %s LIMIT 1", (grade_distribution['term_id'],))
            term = cur.fetchone()
            grade_distribution['term'] = term

            cur.execute("SELECT * FROM courses WHERE id = %s LIMIT 1", (grade_distribution['course_id'],))
            course = cur.fetchone()
            grade_distribution['course'] = course

            cur.execute("SELECT name, slug FROM users WHERE id = %s LIMIT 1", (grade_distribution['user_id'],))
            user = cur.fetchone()
            grade_distribution['user'] = user

        lecturer['grade_distributions'] = self.grade_distributions
        cur.close()
        return lecturer

    def all(self):
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers ORDER BY name ASC")
        lecturers = cur.fetchall()
        cur.close()
        return lecturers

    def create(self):
        ts = time.time()
        created_at = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.slug = self.generate_slug(name=self.name)

        # check uniqueness of the lecturer, create slug from name and check its uniqueness

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM lecturers WHERE email=%s LIMIT 1", (self.email,))
        lecturer = cur.fetchone()
        if lecturer is not None:
            self.errors.append("There is already a lecturer with this email")
            return False

        cur.execute(
            "INSERT INTO lecturers(name, email, user_id, slug, created_at) VALUES(%s, %s, %s, %s, %s) returning id",
            (self.name, self.email, int(self.user_id), self.slug, str(created_at)))

        self.id = cur.fetchone()['id']

        conn.commit()
        cur.close()
        return True

    def delete(self, lecturer_id, user_id):

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""SELECT * FROM lecturers 
            WHERE id = %s AND user_id = %s LIMIT 1""", (lecturer_id, user_id))
        lecturer = cur.fetchone()
        if lecturer is None:
            self.errors.append("No lecturer with that id and user id is found.")
            return False

        cur.execute("""DELETE FROM lecturers WHERE id = %s AND user_id = %s""",
                    (lecturer_id, user_id))

        conn.commit()
        cur.close()
        return True


    def update(self, user_id):

        self.slug = self.generate_slug(name=self.name)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""UPDATE lecturers SET name = %s, slug = %s, 
            email = %s WHERE id = %s AND user_id = %s""", (self.name,
            self.slug, self.email, self.id, self.user_id))
        conn.commit()
        cur.close()
        return True

    def GetErrors(self):
        return self.errors


