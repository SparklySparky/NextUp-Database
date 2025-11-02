import sqlite3

path = "."

def exeggcute(cursor, *commands):
    for command in commands:
        cursor.execute(command)

def startDb():
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            """
            CREATE TABLE IF NOT EXISTS `students` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT,
                `surname` TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS `subjects` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT,
                `teacher` TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS `lists` (
                `student` INTEGER,
                `subject` INTEGER,
                `position` INTEGER NOT NULL,

                PRIMARY KEY (`student`, `subject`),
                FOREIGN KEY (`student`) REFERENCES `students` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`subject`) REFERENCES `subjects` (`id`) ON DELETE CASCADE
            );
            """
        )
    finally:
        conn.close()
    

def getStudents():
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            "SELECT * FROM students"
        )

        results = cursor.fetchall()
    finally:
        conn.close()

    return results

def addStudent(name, surname):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''INSERT INTO students VALUES (null, "{name}", "{surname}")'''
        )
        
        conn.commit()
    finally:
        conn.close()

def updateStudent(id, name, surname):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''UPDATE students SET name = "{name}", surname = "{surname}" WHERE id = {id}'''
        )
        
        conn.commit()
    finally:
        conn.close()

def removeStudent(id):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()
    
    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''DELETE FROM students WHERE id = {id}'''
        )

        conn.commit()
    finally:
        conn.close()

def getSubjects():
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            "SELECT * FROM subjects"
        )

        results = cursor.fetchall()
    finally:
        conn.close()

    return results

def addSubject(name, teacher):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()
    
    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''INSERT INTO subjects VALUES (null, "{name}", "{teacher}")'''
        )

        conn.commit()

    finally:
        conn.close()

def updateSubject(id, name, teacher):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''UPDATE subjects SET name = "{name}", teacher = "{teacher}" WHERE id = {id}'''
        )
        
        conn.commit()
    finally:
        conn.close()

def removeSubject(id):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''DELETE FROM subjects WHERE id = {id}'''
        )

        conn.commit()
    finally:
        conn.close()

def getDraws():
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            "SELECT * FROM lists"
        )

        results = cursor.fetchall()
    finally:
        conn.close()

    return results

def setStudDraw(studentId, subjectId, position):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''INSERT INTO lists VALUES ({studentId}, {subjectId}, {position})'''
        )

        conn.commit()
    finally:
        conn.close()

def removeDraw(studentId, subjectId):
    conn = sqlite3.connect(f'{path}/nextup.db')
    cursor = conn.cursor()

    try:
        exeggcute(
            cursor,
            "PRAGMA foreign_keys = ON",
            f'''DELETE FROM lists WHERE student = "{studentId}" AND subject = "{subjectId}"'''
        )

        conn.commit()
    finally:
        conn.close()