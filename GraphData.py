import json
import vk_api

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


class MyApi:
    def __init__(self, login, password):
        self.session = vk_api.VkApi(
            login, password,
            # функция для обработки двухфакторной аутентификации
            auth_handler=auth_handler,
            captcha_handler=captcha_handler,
        )
        self.id = None
        try:
            with open("vk_config.v2.json", "r") as read_file:
                self.id = json.load(read_file)[login]['token']["app"+str(self.session.app_id)]["scope_"+str(self.session.scope)]['user_id']
        except BaseException as e:
            print(e)

    def get_self_id(self):
        return self.id

    def get_user_by_id(self, id):
        try:
            self.session.auth(token_only=True)
            vk = self.session.get_api()
            return vk.users.get(user_id=id)[0]
        except vk_api.AuthError as error_msg:
            print(error_msg)

    def get_friends(self):
        try:
            self.session.auth(token_only=True)

            vk = self.session.get_api()
            friends = vk.friends.get(user_id=self.id)
            users = []
            for friend_id in friends['items']:
                try:
                    users.append((self.id, str(friend_id)))
                    for sub_friend in vk.friends.get(user_id=friend_id)['items']:
                        users.append((str(friend_id), str(sub_friend)))
                except vk_api.ApiError:
                    pass
            with open("data.json", "w") as write_file:
                json.dump(users, write_file)
            # print(vk.friends.get(user_id=friends["items"][0]))
        except vk_api.AuthError as error_msg:
            print(error_msg)

api = MyApi("+79156047620", "vkd7dL9Dkvs")
print(api.get_self_id())
# def get_friends(login, password):
#     login, password = '+79156047620', os.getenv("PASSWORD")
#     # login = input("Login:")
#     # password = input("Password:")
#     # vk_session = vk_api.VkApi(
#     #     login, password,
#     #     # функция для обработки двухфакторной аутентификации
#     #     auth_handler=auth_handler,
#     #     captcha_handler=captcha_handler,
#     # )
#
#     try:
#         session.auth(token_only=True)
#         vk = session.get_api()
#         friends = vk.friends.get(user_id=os.getenv("USER_ID"))
#         users = []
#         for friend_id in friends['items']:
#             try:
#                 users.append((os.getenv("USER_ID"), str(friend_id)))
#                 for sub_friend in vk.friends.get(user_id=friend_id)['items']:
#                     users.append((str(friend_id), str(sub_friend)))
#             except vk_api.ApiError:
#                 pass
#         with open("data.json", "w") as write_file:
#             json.dump(users, write_file)
#         # print(vk.friends.get(user_id=friends["items"][0]))
#     except vk_api.AuthError as error_msg:
#         print(error_msg)

# vk_session = vk_api.VkApi('+79156047620', 'mypassword')
# vk_session.auth()
#
# vk = vk_session.get_api()

# env = load_dotenv()
# print(os.getenv("CLIENT_ID"),os.getenv("CLIENT_SECRET"))
# code = requests.get(f'https://oauth.vk.com/authorize?client_id={os.getenv("CLIENT_ID")}&display=page&redirect_uri=http://example.com/callback&scope=friends&response_type=code&v=5.131')
# res = requests.get(f'https://oauth.vk.com/access_token?client_id={os.getenv("CLIENT_ID")}&client_secret={os.getenv("CLIENT_SECRET")}&redirect_uri=http://mysite.ru&code=7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a')
# print(res.json())