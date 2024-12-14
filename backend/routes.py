from app import app, db
from flask import request, jsonify
from models import Friend

# Get all friends
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()   
    return jsonify([friend.to_json() for friend in friends])    

# Create a new friend
@app.route('/api/friends', methods=['POST'])
def create_friend():
    try:
        data = request.get_json()


        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        required_fields = ['name', 'role', 'description', 'gender']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        name = data['name']
        role = data['role']
        description = data['description']
        gender = data['gender']

        #fetch avatar image based on gender 
        if gender == 'male':
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else: 
            img_url = None


        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()

        return jsonify({"msg": "Friend created successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/friends/<int:friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    friend = Friend.query.get(friend_id)

    if not friend:
        return jsonify({"error": "Friend not found"}), 404

    db.session.delete(friend)
    db.session.commit()

    return jsonify({"msg": "Friend deleted successfully"})


#UPDATE a friend profile
@app.route("/api/friends/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error":"Friend not found"}), 404
        
        data = request.json

        friend.name = data.get("name",friend.name)
        friend.role = data.get("role",friend.role)
        friend.description = data.get("description",friend.description)
        friend.gender = data.get("gender",friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500