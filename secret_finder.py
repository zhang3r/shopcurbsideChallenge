from urllib.request import urlopen
import requests

class secret_finder:

    def __init__(self):
        self.base_url = 'http://challenge.shopcurbside.com'

    def get_session_id(self):
        session_request = urlopen(self.base_url+'/get-session')
        session_byte = session_request.read()
        session_id = session_byte.decode("utf-8")
        return session_id

    def get_secret(self):
        header = {"Session": self.get_session_id()}
        stack = []
        secret = []
        response = requests.get(self.base_url+'/start', headers=header)
        response_json = response.json()
        for link in reversed(response_json['next']):
            stack.append(link)
        while stack:
            next_ = stack.pop()
            #too lazy to count to 10
            header = {"Session": self.get_session_id()}
            next_response = requests.get(self.base_url+'/'+next_, headers=header)
            next_response_json = next_response.json()

            #Spelling mistakes -___-
            next_text = 'next'
            next_text = 'nExt' if 'nExt' in next_response_json else next_text
            next_text = 'neXT' if 'neXT' in next_response_json else next_text
            if next_text in next_response_json:
                #why is next not always a list!? D:<
                if isinstance(next_response_json[next_text],list):
                    for link in reversed(next_response_json[next_text]):
                        stack.append(link)
                else:
                    stack.append(next_response_json[next_text])
           
            if 'secret' in next_response_json:
                secret.append(next_response_json['secret'])
               

        return ''.join(secret)

def main():
    my_secret = secret_finder()
    print("Secret is: "+my_secret.get_secret())

if __name__ == '__main__':
    main()

