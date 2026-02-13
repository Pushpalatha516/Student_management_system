from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to connect to DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Add Student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add_student.html')


# Attendance Page
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM Students").fetchall()

    if request.method == 'POST':
        date = request.form['date']
        for student in students:
            status = request.form.get(f'status_{student["student_id"]}')  # Present or Absent
            conn.execute(
                "INSERT INTO Attendance (student_id, date, status) VALUES (?, ?, ?)",
                (student['student_id'], date, status)
            )
        conn.commit()
        conn.close()
        return redirect('/attendance')

    conn.close()
    return render_template('attendance.html', students=students)


# View All Students
@app.route('/students')
def students():
    conn = get_db_connection()
    students_data = conn.execute("SELECT * FROM Students").fetchall()
    conn.close()
    return render_template('students.html', students=students_data)

# Edit/Update Student
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute(
            "UPDATE Students SET name = ?, email = ?, course = ? WHERE student_id = ?",
            (name, email, course, student_id)
        )
        conn.commit()
        conn.close()
        return redirect('/students')

    conn.close()
    return render_template('edit_student.html', student=student)

# Delete Student
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect('/students')

# Marks Page
@app.route('/marks', methods=['GET', 'POST'])
def marks():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM Students").fetchall()

    if request.method == 'POST':
        subject = request.form['subject']
        for student in students:
            score = request.form.get(f'score_{student["student_id"]}')
            conn.execute(
                "INSERT INTO Marks (student_id, subject, score) VALUES (?, ?, ?)",
                (student['student_id'], subject, score)
            )
        conn.commit()
        conn.close()
        return redirect('/marks')

    conn.close()
    return render_template('marks.html', students=students)


# Dashboard
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    total_students = conn.execute("SELECT COUNT(*) FROM Students").fetchone()[0]
    total_attendance = conn.execute("SELECT COUNT(*) FROM Attendance").fetchone()[0]
    total_marks = conn.execute("SELECT COUNT(*) FROM Marks").fetchone()[0]
    conn.close()
    return render_template('dashboard.html', total_students=total_students,
                           total_attendance=total_attendance, total_marks=total_marks)

@app.route('/delete_all_students')
def delete_all_students():
    conn = get_db_connection()
    conn.execute("DELETE FROM Students")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='Students';")  # reset ID
    conn.commit()
    conn.close()
    return redirect('/students')


if __name__ == '__main__':
    app.run(debug=True)
