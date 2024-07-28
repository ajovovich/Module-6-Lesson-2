from flask import Flask , jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ('name', 'phone')



def get_db_connection():
    db_name = "fitnesscenter"
    user = 'root'
    password = 'Tuckerstriker12'
    host = '127.0.0.1'

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        if conn.is_connected():
            print('Connected to MySQL database successfully')
            return conn

    except Error as e:
        print(f'Error: {e}')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@app.route('/')
def home():
    return 'Welmcome!'

#Task 2: Implementing CRUD Operations for Members

@app.route("/members", methods=['GET'])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        customers = cursor.fetchall()

        return customers_schema.jsonify(customers)
    except Exception as e:
        print(f'Erorr: {e}')
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members", methods=['POST'])
def add_member():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_customer = (customer_data['name'], customer_data['phone'])

        query = "INSERT INTO Members (name, phone) VALUES (%s, %s)"

        cursor.execute(query, new_customer)
        conn.commit()

        return jsonify({"message": "New customer added successfully"}), 201

    except Error as e:
        print(f'Error: {e}')

        return jsonify({"error": "Internal Servor Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=['PUT'])
def update_member(id):
    try:
        member_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['phone'],id)

        query = "UPDATE Members SET name = %s, phone = %s WHERE id = %s"

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Member info has been updated"})
    except Error as e:
        print(f'Error: {e}')

        return jsonify({"error": "Internal Server Error"}) , 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed}"}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)

        cursor.execute("SELECT * FROM Members where id = %s", member_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        query = "DELETE FROM Members where id =%s"
        cursor.execute(query, member_to_remove)
        conn.commit()

        return jsonify({"message": "Customer removed successfully"}), 200
    
    except Error as e:
        print(f'Error: {e}')
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


#Task 3:Managing Workout Sessions

class WorkoutSessionsSchema(ma.Schema):
    member_id = fields.Integer(required = True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    description = fields.String(required=True)

    class Meta:
        fields = ('id', 'member_id', 'date', 'time', 'description')

workout_session_schema = WorkoutSessionsSchema
workout_sessions_schema = WorkoutSessionsSchema(many=True)




@app.route("/workoutsessions", methods=['POST'])
def schedule_workout():
    try:
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout = (workout_data['member_id'], workout_data['date'], workout_data['time'], workout_data['description'])

        query = "INSERT INTO workoutsessions (member_id, date, time, description) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, new_workout)
        conn.commit()

        return jsonify({"message": "New workout added successfully"}), 201

    except Error as e:
        print(f'Error: {e}')

        return jsonify({"error": "Internal Servor Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions/<int:id>", methods=["PUT"])
def update_workout(id):
    try:
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f'Error: {e}')
        return jsonify(e.messages), 400
    
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_workout = (workout_data['member_id'], workout_data['date'], workout_data['time'], workout_data['description'], id)

        query = "UPDATE workoutsessions SET member_id = %s,date = %s, time = %s, description = %s WHERE id = %s"

        cursor.execute(query, updated_workout)
        conn.commit()

        return jsonify({"message": "Workout sessions has been successfully updated"}), 200

    except Error as e:
        print(f'Error: {e}')

        return jsonify({"error": "Internal Servor Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions", methods=['GET'])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Workoutsessions"

        cursor.execute(query)
        
        workouts = cursor.fetchall()

        return workout_sessions_schema.jsonify(workouts), 200
    except Error as e:
        print(f'An error has occured: {e}')
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:member_id>/workouts", methods=['GET'])
def get_workouts_for_member(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))

        workouts = cursor.fetchall()

        if not workouts:
            return jsonify({"error": "No workout sessions found for this member"}), 404

        return workout_sessions_schema.jsonify(workouts), 200
    except Error as e:
        print(f'Error: {e}')
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# if __name__ == '__main__':
#     app.run(debug=True)