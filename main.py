from UnitedWardrobeApi import Client
import asyncio


def main():
    loop = asyncio.get_event_loop()
    client = Client("EMAIL", "PASSWORD")
    loop.run_until_complete(client.login())
    print(loop.run_until_complete(client.api.get_products()))


if __name__ == '__main__':
    main()
