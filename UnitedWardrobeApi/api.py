import aiohttp
import base64
from .models import Profile, Product, Comment, Cart, UWException


APP_VERSION = "2.2.9"
USER_AGENT = "UWAndroid"
HOST = "https://unitedwardrobe.com/api"
PLATFORM = "android"
LOCALE = "nl_NL"


class Api:

    def __init__(self, device):
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": USER_AGENT,
            "X-Platform": PLATFORM,
            "X-Locale": LOCALE,
            "X-Version": APP_VERSION,
            "X-Device": device
        }
        self.session_id = None
        self.session = None
        self.authorization = None

    async def init(self):
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def heartbeat(self):
        if self.session_id is None:
            data = {"utm_source": "google-play", "utm_medium": "organic"}
        else:
            data = {"session_id": self.session_id}
        async with self.session.post(url="%s/track/heartbeat" % HOST, data=data) as r:
            result = await r.json()
            if result["session_id"] != self.session_id:
                self.session_id = result["session_id"]
                self.headers["X-UW-Session-ID"] = self.session_id
                self.session.close()
                self.session = aiohttp.ClientSession(headers=self.headers)

    async def login(self, username, password):
        async with self.session.post(url="%s/login" % HOST, data={"username": username, "password": password}) as r:
            result = await r.json()
            try:
                user = Profile(result["user"])
                prep = "%s:%s" % (user.username, result["token"])
                self.authorization = "Basic %s" % (base64.b64encode(prep.encode("utf-8")).decode("utf-8"))
                self.headers["Authorization"] = self.authorization
                self.session.close()
                self.session = aiohttp.ClientSession(headers=self.headers)
                return user
            except KeyError:
                raise UWException(result["msg"])

    async def register(self, email, password, first_name, last_name, day, month, year, gender, country, language):
        async with self.session.post(url="%s/register" % HOST, data={"email": email, "password": password, "first_name": first_name, "last_name": last_name, "day": day, "month": month, "year": year, "gender": gender, "country": country, "language": language}) as r:
            return await r.json()

    async def update_user_attribute(self, attribute, value):
        async with self.session.post(url="%s/user/update/" % HOST, data={"data[%s]" % attribute: value}) as r:
            return await r.json()

    async def get_raw_favorites(self, user_id):
        async with self.session.post(url="%s/user/raw_favorites/" % HOST, data={"user_id": user_id}) as r:
            return await r.json()

    async def get_raw_following(self, user_id):
        async with self.session.post(url="%s/user/following/" % HOST, data={"user_id": user_id}) as r:
            return await r.json()

    async def get_cart(self):
        async with self.session.get(url="%s/cart" % HOST) as r:
            return await r.json()

    async def get_notifications(self, offset, limit):
        async with self.session.post(url="%s/notifications/get/" % HOST, data={"offset": offset, "limit": limit}) as r:
            return await r.json()

    async def get_product(self, product_id):
        async with self.session.post(url="%s/product/get/" % HOST, data={"product_id": product_id}) as r:
            result = await r.json()
            return Product(result)

    async def get_product_comments(self, product_id):
        async with self.session.post(url="%s/product/comments" % HOST, data={"product_id": product_id, "tags_supported": True}) as r:
            result = await r.json()
            return [Comment(m) for m in result]

    async def follow(self, follower, to_follow):
        async with self.session.post(url="%s/follow/" % HOST, data={"user_id": follower, "follow_id": to_follow}) as r:
            return await r.json()

    async def defollow(self, follower, to_defollow):
        async with self.session.post(url="%s/follow/defollow/" % HOST, data={"user_id": follower, "follow_id": to_defollow}) as r:
            return await r.json()

    async def get_user_data(self, user_id):
        async with self.session.post(url="%s/user/public_get/" % HOST, data={"user_id": user_id}) as r:
            return await r.json()

    async def get_conversations(self, user_id):
        async with self.session.post(url="%s/conversations/" % HOST, data={"user_id": user_id}) as r:
            return await r.json()

    async def get_conversation(self, from_user_id, to_user_id):
        async with self.session.post(url="%s/conversation/" % HOST, data={"user_id": from_user_id, "other_user": to_user_id}) as r:
            return await r.json()

    async def message(self, from_user_id, to_user_id, message):
        async with self.session.post(url="%s/conversation/post/" % HOST, data={"user_id": from_user_id, "other_user": to_user_id, "message": message}) as r:
            return await r.json()

    async def get_products(self, category=None, order=None, state=None, sub_category=None, gender=None, offset=0, limit=30):
        data = {
            "offset": offset,
            "limit": limit,
            "order_direction": "ASC"
        }
        if category is not None:
            data["filters[category]"] = category
        if sub_category is not None:
            data["filters[subcategory]"] = sub_category
        if order is not None:
            data["filters[order_by]"] = order
        if state is not None:
            data["filters[state]"] = state
        if gender is not None:
            data["filters[gender]"] = gender
        async with self.session.post(url="%s/products/" % HOST, data=data) as r:
            result = await r.json()
            return [Product(p) for p in result["products"]]

    async def add_comment(self, user_id, product_id, comment):
        async with self.session.post(url="%s/messages/add_comment/" % HOST, data={"user_id": user_id, "product_id": product_id, "comment": comment}) as r:
            return await r.json()
