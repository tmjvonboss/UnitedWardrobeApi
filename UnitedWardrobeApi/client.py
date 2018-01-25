from .api import Api
from .models import UWException


class Client:

    def __init__(self, username, password, device="OnePlus ONEPLUS A300 REL"):
        self.api = Api(device)
        self.username = username
        self.password = password

    async def login(self):
        await self.api.init()
        self.profile = await self.api.login(self.username, self.password)
        self.cart = await self.api.get_cart()

    async def message(self, user_id, message):
        return await self.api.message(self.profile.id, user_id, message)

    async def get_conversation(self, user_id):
        result = await self.api.get_conversation(self.profile.id, user_id)
        if result["success"] is False:
            raise UWException(result["msg"])
        else:
            return result

    async def get_conversations(self):
        result = await self.api.get_conversations(self.profile.id)
        if result["success"] is False:
            raise UWException(result["msg"])
        else:
            return result

    async def follow(self, user_id):
        result = await self.api.follow(self.profile.id, user_id)
        if result["success"] is False:
            raise UWException(result["msg"])
        else:
            return result

    async def defollow(self, user_id):
        result = await self.api.defollow(self.profile.id, user_id)
        if result["success"] is False:
            raise UWException(result["msg"])
        else:
            return result

    async def add_comment(self, product_id, comment):
        result = await self.api.add_comment(self.profile.id, product_id, comment)
        if result["success"] is False:
            raise UWException(result["msg"])
        else:
            return result


