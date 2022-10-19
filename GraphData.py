import json
import vk_api

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


class MyApi:
    def __init__(self, login, password):
        self.session = vk_api.VkApi(
            login, password,
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
        except vk_api.AuthError as error_msg:
            print(error_msg)

