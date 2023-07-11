import requests
import json
import base64

#from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Get api-key with email and password. Return status code abd api_key in JSON format.
        Status code 200 means that email and password are correct."""
        headers = {
            'email' : email,
            'password' : password
        }

        res = requests.get(self.base_url + '/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def get_pets_list(self, auth_key: json, filter: str) -> json:
        """get list pf pets. """
        headers = {
            'auth_key' : auth_key['key']
        }
        filter = {
            'filter' : filter
        }

        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """This method allows add information about new pet.
        The status code 200 means that pet was successfully added to the database.
        The status code 400 means that provided data is incorrect.
        The status code 404 means that provided auth_key is incorrect"""

        if pet_photo != "":
            pet_photo_file = (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        else:
            pet_photo_file = ''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': pet_photo_file
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        #print('result add/pet = ', result)

        return status, result
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """This method deletes pet with pet_idfrom database
        Status code 200 - pet was removed
        Status code 403 - invalid auth_key"""

        headers = {
            'auth_key': auth_key['key']
        }
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """This method allows update information about pet"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })

        headers = {
            'auth_key': auth_key['key'], 'Content-Type': data.content_type
        }

        res = requests.put(self.base_url + "/api/pets/" + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """This method adds new pet without photo"""
        if age != '':
            data = MultipartEncoder(
                fields={
                    'name': name,
                    'animal_type': animal_type,
                    'age': age,
                })
        else:
            data = MultipartEncoder(
                fields={
                    'name': name,
                    'animal_type': animal_type,

                })

        headers = {
            'auth_key': auth_key['key'], 'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def set_pet_photo(self, auth_key, pet_id, pet_photo):
        """This method allows to add photo of a pet."""
        if pet_photo != "":
            pet_photo_file = (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        else:
            pet_photo_file = ''
        data = MultipartEncoder(
            fields={
               'pet_photo': pet_photo_file
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def encode_file_to_base64(self, file_name: str):
        with open(file_name, 'rb') as file:
            base64_string = base64.b64encode(file.read())
        return 'data:image/jpeg;base64,' + base64_string.decode('utf-8')   #str(base64_string)[2:]