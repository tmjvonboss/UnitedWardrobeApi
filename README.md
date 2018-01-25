# UnitedWardrobeApi
![LOGO HERE THO](https://www.staticuw.com/assets/images/fb-header-2.jpg)
Asynchronous Python 3.6 API of United Wardrobe (https://unitedwardrobe.com)

## Why?
I just felt like it...

## How?
Android + Xposed + SSLUnpinning + Debug Proxy Premium

## Feedback to the developers of this app
When reverse engineering the API I noticed a few things such as:
+ Double User-Agent header when  making requests to some endpoints but not all (heartbeat, products have double UA)... (UWAndroid + OKHttp/3.8.0)
+ Always sends your own user_id, I don't know why you guys send the user_id if it doesn't matter what value it is (message/comment spoofing is impossible, so why send the user_id)
+ The app claims to be protecting private details, but often the username of a user contains either their full name (format: [first][last]_[userid]) or facebook id (which can be linked to their profile in this format: https://fb.com/[id])

## Usage
See the main.py in this repository, it works just fine
What you do with your code is your business, not mine.
