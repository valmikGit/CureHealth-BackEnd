# import random
# from django.core.cache import cache

# def send_otp_to_mobile(mobile, user_Obj):
#     if cache.get(mobile):
#         return False, cache.ttl(mobile)
#     try:
#         otp_To_be_Sent = random.randint(1000, 9999)
#         cache.set(key=mobile, value=user_Obj, timeout=60)
#         user_Obj.otp = otp_To_be_Sent
#         user_Obj.save()
#         return True, 0
#     except Exception as e:
#         print(e)