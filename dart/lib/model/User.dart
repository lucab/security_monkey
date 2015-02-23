library security_monkey.user;

import 'dart:convert';

class User {

    int id;
    String email = "";
    bool active = false;


    User.fromMap(Map data) {
        print("User Constructor Received $data");
        id = data['id'];
        active = data['active'];
        email = data['email'];
    }

    String toJson() {
        Map objmap = {
            "id": id,
            "email": email,
            "active": active,
        };
        return JSON.encode(objmap);
    }

}

