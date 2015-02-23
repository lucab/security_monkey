#     Copyright 2014 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from security_monkey.views import AuthenticatedService
from security_monkey.views import __check_auth__
from security_monkey.views import USERS_FIELDS
from security_monkey.datastore import Account
from security_monkey.datastore import User
from security_monkey import db
from security_monkey import api

from flask.ext.restful import marshal, reqparse
from flask.ext.login import current_user


class UsersGet(AuthenticatedService):
    def __init__(self):
        super(UsersGet, self).__init__()

    def get(self):
        """
            .. http:get:: /api/1/users

            Get a list of available users.

            **Example Request**:

            .. sourcecode:: http

                GET /api/1/users HTTP/1.1
                Host: example.com
                Accept: application/json

            **Example Response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: application/json

                {
                    "users": [
                        {
                            "active": true,
                            "id": 1,
                            "email": "infrsec@rocket-internet.de"
                        },
                        {
                            "active": true,
                            "id": 2,
                            "email": "lucab@debian.org"
                        }
                    ]
                }

            :statuscode 200: no error
            :statuscode 401: Authentication Error. Please Authenticate.
        """
        auth, retval = __check_auth__(self.auth_dict)
        if auth:
            return retval

        return_dict = {}
        return_dict['auth'] = self.auth_dict
        return_dict['users'] = []
        # TODO: (maybe) filter by group-level once roles are in place
        users = User.query.all()
        for user in users:
            sub_marshaled = marshal(user.__dict__, USERS_FIELDS)
            return_dict['users'].append(sub_marshaled)
        return return_dict, 200

