#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from lib.crawler import Spider
from lib.auth import Auth
import os

authentication = Auth(
	url = "http://192.168.0.19/login.php",
	method = "POST",
	restricted_url = "http://192.168.0.19/index.php")
authentication.set_payload({
	'Login': 'Login',
	'username': 'admin',
	'password': 'password'
})
authentication.authenticate()
authentication.change_cookie_value('security','low')

url = "http://192.168.0.19"
banned_urls = ["vulnerabilities/csrf/"]
crwaler = Spider(url, authentication, banned_urls)
crwaler.run()
