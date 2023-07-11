from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends() # Объект PetFriends

def test_get_api_key_success(email=valid_email, password=valid_password):
    """Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result"""
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_invalid_data(email=valid_email, password = valid_password + '123'):
    '''проверяем ответ сервера на запрос api_key с неправильным паролем. Статус должен быть 403'''
    status, _ = pf.get_api_key(email, password)

    assert status == 403

def test_get_pets_list_success(filter=''):
    """Получаем список всех питомцев (filter='') или питомцев пользователя (filter='my_pets') = """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pets_list(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_pets_list_invalid_auth_key(filter=''):
    '''Проверяем, чот при запросе списка питомцев с неправильным auth_key получаем статус 403'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = auth_key['key'] + '123"'

    status, _ = pf.get_pets_list(auth_key, filter)

    assert status == 403

def test_add_pet_success(name='Котофей', animal_type='котик', age='4', pet_photo='images/cat_cat_face_cats_eyes.jpg'):
    """Проверяем, что можно внести данные на нового питомца"""

    # получаем полный путь фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_pet_invalid_auth_key(name='Котофей', animal_type='котик', age='4', pet_photo='images/cat_cat_face_cats_eyes.jpg'):
    '''Проверяем что при запросе на добавление питомца с неправильным auth_key получаем статус 403'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = auth_key['key'] + '123"'

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403

def test_add_pet_invalid_data(name='Котофей', animal_type='котик', age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, '')

    assert status == 400

def test_delete_pet_success():
    """Проверяем, что можно удалить последнего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')

    # Проверяем, есть ли питомцы у api_key. Если нет, то добавляем нового
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Котофей', 'котик', '4', 'images/cat_cat_face_cats_eyes.jpg')
        _, my_pets = pf.get_pets_list(auth_key, 'my_pets')

    # Берем pet_id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Удаляем питомца с pet_id
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем удаление pet_id
    # Запрашиваем список питомцев
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_invalid_auth_key():
    '''Проверяем что при запросе на удаление питомца с неправильным auth_key получаем статус 403'''
    _, auth_key_valid = pf.get_api_key(valid_email, valid_password)
    auth_key_invalid = {'key': '123456'}


    _, my_pets = pf.get_pets_list(auth_key_valid, 'my_pets')

    # Проверяем, есть ли питомцы у api_key. Если нет, то добавляем нового
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key_valid, 'Котофей', 'котик', '4', 'images/cat_cat_face_cats_eyes.jpg')
        _, my_pets = pf.get_pets_list(auth_key_valid, 'my_pets')

    # Берем pet_id первого питомца
    pet_id = my_pets['pets'][0]['id']

    # Удаляем питомца с pet_id
    status, _ = pf.delete_pet(auth_key_invalid, pet_id)

    assert status == 403

def test_update_pet_info_success(name='Котофеич', animal_type='Котэ', age='5'):
    """Проверяем возможность обновить информацию о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')

    #Если список не пустой, то пробуем обновить данные первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        #Проверяем, что статус 200 и имя соответствуем имени в запросе
        assert status == 200
        assert result['name'] == name
    else:
        # Если нет питомцев, то сообщаем об отсутствии своих питомцев
        raise Exception(f'У {auth_key} нет своих питомцев')

def test_update_pet_info_invalid_auth_key(name='Котофеич', animal_type='Котэ', age='5'):
    '''Проверяем что при запросе на обновление информации о питомце с неправильным auth_key получаем статус 403'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key_invalid = {'key': '123456'}

    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, _ = pf.update_pet_info(auth_key_invalid, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        pf.create_pet_simple(auth_key, name='Котофеич', animal_type='Котэ', age='5')
        status, _ = pf.update_pet_info(auth_key_invalid, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 403

def test_update_pet_info_invalid_data(name='Котофеич', animal_type='Котэ', age='5'):
    '''Проверяем, что при запросе на обновление информации о питомце с неправильными данными получаем статус 400'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')
    pet_id_invalid = '123456'

    if len(my_pets['pets']) > 0:
        status, _ = pf.update_pet_info(auth_key, pet_id_invalid, name, animal_type, age)
    else:
        pf.create_pet_simple(auth_key, name='Котофеич', animal_type='Котэ', age='5')
        status, _ = pf.update_pet_info(auth_key, pet_id_invalid, name, animal_type, age)

    assert status == 400

def test_create_pet_simple_success(name='Котофей', animal_type='котик', age='4'):
    """ Проверяем возможность создать нового питомца (без фотографии)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_invalid_auth_key(name='Котофей', animal_type='котик', age='4'):
    '''Проверяем, что при запросе на добавление нового питомца без фото с неправильным auth)key получаем статус 403'''
    auth_key_invalid = {'key': '123456'}

    status, _ = pf.create_pet_simple(auth_key_invalid, name, animal_type, age)

    assert status == 403

def test_create_pet_simple_invalid_data(name='', animal_type='', age=''):
    '''Проверяем, что при добавлении нового питомца без фото с неправильными данными получаем статус 400'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 400


def test_add_pet_photo_success(pet_photo='images/cat_cat_face_cats_eyes.jpg'):
    """ Проверяем возможность добавить фотографию питомуа в информацию о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')


    # Если список не пустой, то пробуем обновить данные первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что статус 200 и фото соответствуем фото в запросе
        assert status == 200
        assert len(result['pet_photo']) > 0 #== pf.encode_file_to_base64(pet_photo)
    else:
        # Если нет питомцев, то сообщаем об отсутствии своих питомцев
        raise Exception(f'У {auth_key} нет своих питомцев')

def test_add_pet_photo_invalid_auth_key(pet_photo='images/cat_cat_face_cats_eyes.jpg'):
    '''Проверяем, что при попытке добавления фотографии питомца с неправильным auth_key получаем статус 403'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key_invalid = {'key': '123456'}
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')


    # Если список не пустой, то пробуем обновить данные первого питомца
    if len(my_pets['pets']) > 0:
        status, _ = pf.set_pet_photo(auth_key_invalid, my_pets['pets'][0]['id'], pet_photo)

    else:
        pf.create_pet_simple(auth_key, name='Котофеич', animal_type='Котэ', age='5')
        status, _ = pf.set_pet_photo(auth_key_invalid, my_pets['pets'][0]['id'], pet_photo)

    assert status == 403

def test_add_pet_photo_invalid_data():
    '''Проверка, что при попытке добавления фото питомца с неправильными данными получаем статус 400'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, 'my_pets')
    pet_id_invalid = '123456'

    # Если список не пустой, то пробуем обновить данные первого питомца
    if len(my_pets['pets']) > 0:
        status, _ = pf.set_pet_photo(auth_key, pet_id_invalid, '')

    else:
        pf.create_pet_simple(auth_key, name='Котофеич', animal_type='Котэ', age='5')
        status, _ = pf.set_pet_photo(auth_key, pet_id_invalid, pet_photo)

    assert status == 400