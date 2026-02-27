# PR-Agent 테스트용 샘플 코드

def calculate_discount(price, discount_rate):
    """상품 할인가를 계산합니다."""
    if discount_rate > 1:
        discount_rate = discount_rate / 100
    discounted = price * (1 - discount_rate)
    return discounted

def get_user_data(user_id):
    """사용자 데이터를 가져옵니다."""
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    data = response.json()
    return data

def process_order(items, user_id):
    """주문을 처리합니다."""
    total = 0
    for item in items:
        total = total + item['price'] * item['quantity']
    user = get_user_data(user_id)
    print("주문 처리 완료:", total)
    return total
