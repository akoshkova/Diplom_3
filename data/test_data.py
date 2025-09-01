class TestData:
    VALID_INGREDIENTS = [
        {'name': 'Булка', 'type': 'bun'},
        {'name': 'Соус', 'type': 'sauce'}
    ]

    ORDER_DATA = {
        'ingredients': ['60d3b41abdacab0026a733c6', '60d3b41abdacab0026a733c7']
    }

def user_credentials():
    return {
        'email': 'test_user@example.com',
        'password': 'P@ssw0rd123'
    }