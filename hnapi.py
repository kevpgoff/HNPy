import requests
import json

BASE_URL = "https://hacker-news.firebaseio.com/v0/"
ITEM = "item/{}.json"
USER = "user/{}.json"
TOP = "topstories.json"
NEW = "newstories.json"
BEST = "beststories.json"
ASK = "askstories.json"
SHOW = "showstories.json"
JOB = "jobstories.json"
MAXITEM = "maxitem.json"
UPDATES = "updates.json"

class Error(Exception):
	pass

class HTTPError(Error):
	pass

class InvalidItemIDError(Error):
	pass

class InvalidUserIDError(Error):
	pass

class HN(object):
	def __init__(self):
		self.session = requests.Session()

	def _get(self, url):
		response = self.session.get(url)
		if (response.status_code == requests.codes.ok):
			return response
		else:
			raise HTTPError

	def _getParams(self, params):
		return self._get('{BASE_URL}{PARAMS}'.format(BASE_URL = BASE_URL, PARAMS = params))

	def getItem(self, itemID):
		response = self._getParams(ITEM.format(itemID)).json()

		if not response:
			raise InvalidItemIDError
		else:
			return Item(response)

	def getUser(self, userID):
		response = self._getParams(USER.format(userID)).json()

		if not response:
			raise InvalidUserIDError
		else:
			return User(response)

	def getTopStories(self, maxVal = 100):
		return self._getParams(TOP).json()[:maxVal]

	def getBestStories(self, maxVal = 100):
		return self._getParams(BEST).json()[:maxVal]

	def getNewStories(self, maxVal = 100):
		return self._getParams(NEW).json()[:maxVal]

	def getAskStories(self, maxVal = 100):
		return self._getParams(ASK).json()[:maxVal]

	def getShowStories(self, maxVal = 100):
		return self._getParams(SHOW).json()[:maxVal]

	def getJobStories(self, maxVal = 100):
		return self._getParams(JOB).json()[:maxVal]

	def getUpdates(self):
		return self._getParams(UPDATES).json()

	def getMaxItem(self):
		return self._getParams(MAXITEM).json()

class User(object):
	def __init__(self, response):
		self.id = response.get('id')
		self.delay = response.get('delay')
		self.created = response.get('created')
		self.karma = response.get('karma')
		self.about = response.get('about')
		self.submitted = response.get('submitted')
		self.rawjson = json.dumps(response)

	def __repr__(self):
		return '<User ID: {userID}>'.format(userID = self.id)

class Item(object):
	def __init__(self, response):
		self.id = response.get('id')
		self.deleted = response.get('deleted')
		self.type = response.get('type')
		self.by = response.get('by')
		self.time = response.get('time')
		self.text = response.get('text')
		self.dead = response.get('dead')
		self.parent = response.get('parent')
		self.poll = response.get('poll')
		self.kids = response.get('kids')
		self.url = response.get('url')
		self.score = response.get('score')
		self.title = response.get('title')
		self.parts = response.get('parts')
		self.descendants = response.get('descendants')
		self.rawjson = json.dumps(response)

	def __repr__(self):
		return '<Item ID: {itemID}>'.format(itemID = self.id)