import allure
import jsonschema
import requests
from tests.schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение нового заказа")
    def test_placing_an_order(self):
        with allure.step("Подготовка данных для размещения нового заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса для размещения нового заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка ответа на содержание данных созданного заказа"):
            assert response_json["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "id питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "количество не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], ("статус завершения размещения заказа не совпадает "
                                                                      "с ожидаемым")

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа с id = 1"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id
            assert response.json()['petId'] == 1 #А так правильно сравнивать со значением? Или правильней сравнивать
            # с переменной, по аналогии с assert response.json()["id"] == order_id ?
            assert response.json()['quantity'] == 1
            assert response.json()['status'] == "placed"
            assert response.json()['complete'] == True

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Отправка запроса на удаление заказа с id = 1"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа после удаления заказа с id = 1"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение удаленного заказа с id = 1"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и текста ошибки после получения удаленного заказа с id = 1"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == 'Order not found', "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа и текста ошибки после получения несуществующего заказа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
            assert response.text == 'Order not found', "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_store(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и формата данных инвентаря"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым" #Ассерт падает, т.к /store/inventory
            # отдает 500, поломалось в сваггере :(
            assert isinstance(response.json(), dict), "Вернулся не словарь"
            assert response.json()['approved'] == 57 #Здесь тоже не понимаю так верно сравнивать с конкретным
            # значением, которое по сути лежит в payload функции create_order() в фикстуре? Или правильней в тесте вызвать
            # create_order["approved"] и положить значение 57 в переменную, а здесь сравнивать с переменной уже?

            assert response.json()['delivered'] == 50