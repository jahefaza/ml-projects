import os
import requests

class TokenManager:
    def __init__(self, server, token_file, refresh_file):
        self.server = server
        self.token_file = token_file
        self.refresh_file = refresh_file
        self.token = None
    
    # --------------------------
    # Main Entry: Return Token
    # --------------------------

    def get_valid_token(self):
        self.token = self._load_token()
        if self.token and self._check_token_validity(self.token):
            print('Token valid')
            return self.token

        print('Token invalid try to refresh ...')
        refreshed = self._refresh_token()
        if refreshed:
            return refreshed

        raise SystemExit('Both token and refresh failed') 

    # ---------------
    # Load Token
    # ---------------

    def _load_token(self):
        if os.path.exists(self.token_file):
            print(f"Checking token file at: {self.token_file}")
            with open(self.token_file, 'r') as f:
                token = f.read().strip()
                if token:
                    print('Access token loaded')
                    return token
        print ('No token found')
        return None
    
    # --------------------
    # Load Refresh Token
    # --------------------

    def _refresh_token(self):
        refresh_api =  f'{self.server}/api/auth/token'

        if not os.path.exists(self.refresh_file):
            print('No refresh token')
            return None
        with open(self.refresh_file, 'r') as f:
            refresh = f.read().strip()
            print('Refresh token loaded')
        if not refresh:
            print('Refresh token empty')
            return None
        
        try:
            response = requests.post(refresh_api, json={'refreshToken': refresh})
            
            if response.status_code == 200:
                data = response.json()
                new_token = data.get('token')

                if new_token:
                    with open(self.token_file,'w') as f:
                        f.write(new_token)
                    print('Access token refreshed')
                    self.token = new_token
                    return new_token
                
                print('Refresh succeed but No Token')
                return None
            
            print(f'Refresh Failed: {response.status_code} - {response.text}')
            return None

        except Exception as e:
            print(f'Error during refresh {e}')
            return None
    
    # ---------------------
    # Check Validity Token
    # ---------------------

    def _check_token_validity(self, token):
        url = f'{self.server}/api/auth/user'
        headers = {'X-Authorization':f'Bearer {token}'}

        try:
            r = requests.get(url, headers=headers)
            return r.status_code == 200
        except:
            return False