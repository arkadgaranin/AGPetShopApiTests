import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet/", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_with_full_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"

            assert response_json["category"]["id"] == payload["category"]["id"], ("id категории питомца не совпадает "
                                                                                  "с ожидаемым")
            assert response_json["category"]["name"] == payload["category"]["name"], ("название категории питомца "
                                                                                      "не совпадает с ожидаемым")

            assert response_json["photoUrls"][0] == payload["photoUrls"][0], ("ссылка на фото питомца не совпадает "
                                                                              "с ожидаемым")

            assert response_json["tags"][0]["id"] == payload["tags"][0]["id"], ("id тега питомца не совпадает "
                                                                                "с ожидаемым")
            assert response_json["tags"][0]["name"] == payload["tags"][0]["name"], ("название тега питомца не совпадает "
                                                                                    "с ожидаемым")

            assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet, update_pet):
        with allure.step("Получение ID созданного питомца и остальных его данных"):
            pet_id = create_pet["id"]
            pet_name = create_pet["name"]
            pet_status = create_pet["status"]

        with allure.step("Получение ID обновленного питомца"):
            update_pet_id = update_pet["id"]

        with allure.step("Отправка запроса на получение информации обновленного питомца по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{update_pet_id}")

        with allure.step("Проверка статуса ответа и обновленных данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] != pet_id
            assert response.json()["name"] != pet_name
            assert response.json()["status"] != pet_status

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа после удаления питомца"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение удаленного питомца по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа после получения удаленного питомца"):
            assert response.status_code == 404