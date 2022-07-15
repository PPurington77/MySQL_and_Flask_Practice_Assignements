from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = data['first_name'] + ' ' + data['last_name']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('dojos_and_ninjas_db').query_db(query)
        # Create an empty list to append our instances of friends
        all_ninjas = []
        # Iterate over the db results and create instances of friends with cls.
        for ninja in results:
            all_ninjas.append( cls(ninja) )
        return all_ninjas

    @classmethod
    def create(cls, data ):
        query = "INSERT INTO ninjas ( first_name, last_name, age, created_at, updated_at, dojo_id ) VALUES ( %(first_name)s, %(last_name)s, %(age)s, NOW() , NOW(), %(dojo_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('dojos_and_ninjas_db').query_db( query, data )

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM ninjas WHERE id = %(id)s;"
        result = connectToMySQL('dojos_and_ninjas_db').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE ninjas SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_db').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas_db').query_db(query,data)