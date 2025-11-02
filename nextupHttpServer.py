from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import sqlite3
import nextupdb
import re
import random

#DO NOT CHANGE
path = "pathoftheserver"

class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search("/students", self.path):
            try:
                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        elif re.search("/draw", self.path):
            try:
                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        elif re.search("/ping", self.path):
            try:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                self.wfile.write(bytes("This is a NextUp server", "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/dump", self.path):
            try:
                # Get all data from the database
                students = nextupdb.getStudents()
                subjects = nextupdb.getSubjects()
                draws = nextupdb.getDraws()

                # Format students data
                students_data = []
                for stud in students:
                    students_data.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                # Format subjects data
                subjects_data = []
                for subj in subjects:
                    subjects_data.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                # Format draws data
                draws_data = []
                for draw in draws:
                    draws_data.append(
                        {
                            "studentId": draw[0],
                            "subjectId": draw[1],
                            "position": draw[2]
                        }
                    )

                with open(f'{path}/password.txt', 'r') as file:
                    content = file.read()

                admin = self.path.replace("/dump?password=", "") == content

                # Combine all data into one response
                response = {
                    "admin": admin,
                    "students": students_data,
                    "subjects": subjects_data,
                    "draws": draws_data,
                }

                json_resp = json.dumps(response, indent=2)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
            except Exception as e:
                print(f"Dump error: {e}")
                self.send_response(500)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if re.search("/students", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.addStudent(response["studentName"], response["studentSurname"])

                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.addSubject(response["subjectName"], response["teacher"])

                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        elif re.search("/draw", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                students = nextupdb.getStudents()
                lists = nextupdb.getDraws()

                drawSubject = response["subjectId"]
                drawNumber = response["drawNumber"]

                studNotDrawn = []
                for stud in students:
                    studNotDrawn.append(stud[0])
                
                stAlrDrwPos = []

                for stud in lists:
                    if stud[1] == drawSubject:
                        studNotDrawn.remove(stud[0])
                        stAlrDrwPos.append(stud[2])

                stAlrDrwPos.sort()

                random.shuffle(studNotDrawn)

                studDrawn = studNotDrawn[:drawNumber]

                print(studDrawn)
    
                if len(stAlrDrwPos) == 0:
                    for stud in studDrawn:
                        nextupdb.setStudDraw(stud, drawSubject, 1 + studDrawn.index(stud))
                else:
                    for stud in studDrawn:
                        nextupdb.setStudDraw(stud, drawSubject, stAlrDrwPos[len(stAlrDrwPos) - 1] + 1 + studDrawn.index(stud))

                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if re.search("/students", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))
                
                nextupdb.removeStudent(response["id"])

                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.removeSubject(response["id"])

                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/draw", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.removeDraw(response["studentId"], response["subjectId"])

                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_PATCH(self):
        if re.search("/students", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.updateStudent(response["id"],response["studentName"], response["studentSurname"])

                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.updateSubject(response["id"],response["subjectName"], response["teacher"])

                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except sqlite3.Error as er:
                print(er.sqlite_errorcode)
                print(er.sqlite_errorname)
                self.send_response(400)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

def startServer():
    server = HTTPServer(("", 4444), NeuralHTTP)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.1.1.1'
    finally:
        s.close()

    print(f'Server Avviato, IP: {IP}')

    server.serve_forever()
    server.server_close()