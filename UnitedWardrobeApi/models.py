import json
import aiohttp


class ObjectBase(object):

    def __init__(self, json_object):
        self.__dict__ = json_object

    def default(self, o):
        return o._asdict()

    def _asdict(self):
        return self.__dict__

    def load_json(self, json_object):
        self.__dict__ = json_object

    def dump_json(self):
        return json.dumps(self.__dict__, default=self.default)

    def __repr__(self):
        return self.dump_json()


class Profile(ObjectBase):

    def __init__(self, profile):
        super().__init__(profile)
        if self.profile == "":
            self.profile = "default.jpg"
        if self.cover == "":
            self.cover = "default.jpg"
        self.profile = Image("https://www.staticuw.com/image/profile/%s" % self.profile, self.profile)
        self.cover = Image("https://www.staticuw.com/image/cover/%s" % self.cover, self.cover)


class Cart(ObjectBase):

    def __init__(self, cart):
        super().__init__(cart)


class Currency(ObjectBase):

    def __init__(self, currency):
        super().__init__(currency)


class Product(ObjectBase):

    def __init__(self, product):
        super().__init__(product)
        try:
            self.user = User(self.user)
            self.image = Image("https://www.staticuw.com/image/product/larger/%s" % self.image, self.image)
            self.images = [Image("https://www.staticuw.com/image/product/larger/%s" % image, image) for image in self.images.split(",")]
        except:
            pass

    async def save_images(self, path=""):
        try:
            await self.user.save_images(path)
            await self.image.download(path)
            for img in self.images:
                await img.download(path)
        except:
            pass


class Comment(ObjectBase):

    def __init__(self, comment):
        super().__init__(comment)
        self.user = User(self.user)


class User(ObjectBase):

    def __init__(self, user):
        super().__init__(user)
        if self.profile == "":
            self.profile = "default.jpg"
        self.profile = Image("https://www.staticuw.com/image/profile/%s" % self.profile, self.profile)
        try:
            if self.cover == "":
                self.cover = "default.jpg"
            self.cover = Image("https://www.staticuw.com/image/cover/%s" % self.cover, self.cover)
        except:
            pass

    async def save_images(self, path):
        await self.profile.download(path)
        await self.cover.download(path)


class Image:

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def _asdict(self):
        return self.__dict__

    async def download(self, path=""):
        with aiohttp.ClientSession() as c:
            async with await c.get(url=self.url) as r:
                img = await r.read()
                with open(path + self.name, "wb") as f:
                    f.write(img)

    def __repr__(self):
        return self.url


class UWException(Exception):

    def __init__(self, args):
        Exception.__init__(self, args)
