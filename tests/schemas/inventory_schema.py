INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {"type": "integer"},
        "delivered": {"type": "integer"}
        #Какой 3-й статус не понял, т.к в тест-кейсе только эти 2 статуса, а в сваггере поломался этот запрос
    },
    "required": ["approved", "delivered"],
    "additionalProperties": False
}