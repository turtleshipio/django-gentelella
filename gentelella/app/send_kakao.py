from app.kakao import OrderCreator
from app import utils

sender = OrderCreator()

phones = [
    '01088958454', #염승헌
]

notify_id = utils.get_uuid(70)
order_id = notify_id[:7]
retailer_name = "블랙위스커"
prd1 = "상품명"
prd_count = 1

sender.set_msg(order_id=order_id, retailer_name=retailer_name,
               prd1=prd1, prd_count = prd_count,
               notify_id=notify_id)

for p in phones:
    sender.send_kakao_msg(p)