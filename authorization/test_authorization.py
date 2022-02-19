import unittest
import authorization
from authorization import authorization
import os
import json
from unittest.mock import patch

class TestAuthorization(unittest.TestCase):

    def test_auto_create_sys_config_file(self):
        home_path = os.getenv("HOME")
        config_path = f'{home_path}/.config/code_clinic'
        authorization.auto_create_sys_config_file()
        self.assertTrue(os.path.exists(f'{config_path}/.sys_config.json'))
        os.remove(f'{config_path}/.sys_config.json') 
       

    def test_client_authorization(self):
       pass


    def test_select_scope(self):
        scope_file = ['https://www.googleapis.com/auth/calendar.events.readonly']
        scope = authorization.select_scope("student")
        self.assertEqual(scope,scope_file)


    def test_read_user_config_file(self):
        home_path = os.getenv("HOME")
        config_path = f'{home_path}/.config/code_clinic'
        data = {"user_type":"student","email":"test1@gmail.com"}
        with open(f'{config_path}/.config.json','w') as file_: 
            json.dump(data,file_)
        output = authorization.read_user_config_file()
        self.assertEqual("student",output)
        os.remove(f'{config_path}/.config.json')


    def test_revoke_tokens(self):
        pass