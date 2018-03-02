import hnapi
import datetime
import webbrowser
from sty import fg, bg, ef, rs
from urllib.parse import urlparse

class HNPage:
	def __init__(self, api):
		self.api = api
		self.currentPage = None
		self.currentIndex = -1
		self.allLoaded = None

	def _renderPage(self):
		for index, item in enumerate(self.currentPage):
			print("{PostNum}. ".format(PostNum = (self.currentIndex * 10) + index + 1) + ef.bold + "{Title} ".format(Title = self.api.getItem(item).title) + rs.bold + "({URL})".format(URL = parseURL(self.api.getItem(item).url)))
			print(ef.faint + ("{Score} points by {Author} {Time} ago | {Comments} comments\n").format(Score = self.api.getItem(item).score, Author = self.api.getItem(item).by, Time = parseDateTime(self.api.getItem(item).time), Comments = 0 if self.api.getItem(item).kids == None else len(self.api.getItem(item).kids)) + rs.faint)


	def _display(self, storedResponse, displayValue):
		self.allLoaded = [storedResponse[x:x+displayValue] for x in range(0, len(storedResponse), displayValue)]
		self.currentPage = self.allLoaded[0]
		self.currentIndex = 0
		self._renderPage()

	def displayNextPage(self):
		self.currentPage = self.allLoaded[self.currentIndex + 1]
		self.currentIndex += 1
		self._renderPage()

	def displayPreviousPage(self):
		self.currentPage = self.allLoaded[self.currentIndex - 1]
		self.currentIndex -= 1
		self._renderPage()

	def displayTopStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getTopStories(loadValue)
		self._display(tempStorage, displayValue)

	def displayBestStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getBestStories(loadValue)
		self._display(tempStorage, displayValue)		
	
	def displayNewStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getNewStories(loadValue)
		self._display(tempStorage, displayValue)		

	def displayAskStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getAskStories(loadValue)
		self._display(tempStorage, displayValue)

	def displayShowStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getShowStories(loadValue)
		self._display(tempStorage, displayValue)	

	def displayJobStories(self, loadValue = 1000, displayValue = 10):
		tempStorage = self.api.getJobStories(loadValue)
		self._display(tempStorage, displayValue)

	def openURL(self, index):
		val = index - (len(self.currentPage) * self.currentIndex) - 1
		if val in range(0, len(self.currentPage)):
			webbrowser.open((self.api.getItem(self.currentPage[val])).url, new = 2)
		else:
			print("Must be in range")

	def mainLoop(self):
		exit = False
		bg.orange = ('rgb', (255, 102, 0))
		urlVal = []
		print("Press 'h' for help.")
		while(exit == False):
			input_ = input("Enter a command: ")
			if input_ == "t":
				self.displayTopStories()
			elif input_ == "b":
				self.displayBestStories()
			elif input_ == "n":
				self.displayNewStories()
			elif input_ == "a":
				self.displayAskStories()
			elif input_ == "s":
				self.displayShowStories()
			elif input_ == "j":
				self.displayJobStories()
			elif input_ == "i":
				if self.currentIndex == -1:
					continue
				else:
					self.displayNextPage()
			elif input_ == "u":
				if self.currentIndex > 0:
					self.displayPreviousPage()
				else:
					continue
			elif input_.startswith("o "):
				urlVal = input_.split(" ", 1)
				if urlVal[1]:
					if urlVal[1].isdigit():
						self.openURL(int(urlVal[1]))
					else:
						print("Format is: o ##")
				else:
					print("Format is: o ##")
			elif input_ == "h":
				print(bg.orange + "t: Top | b: Best | n: New | a: Ask | s: Show | j: Jobs | o ##: Open URL | u: Prev Page | i: Next Page" + bg.rs)
			else:
				continue


def parseDateTime(date):
	time1 = datetime.datetime.fromtimestamp(date)
	time2 = datetime.datetime.now()

	diff = time2 - time1
	days, seconds = diff.days, diff.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60

	return (str(minutes) + " minutes") if hours == 0 else (str(hours) + " hours")

def parseURL(url):
	parsedURL = urlparse(url)
	parsedDomain = '{uri.netloc}'.format(uri = parsedURL)
	return parsedDomain

def main():
	hackernews = HNPage(hnapi.HN())
	hackernews.mainLoop()

if __name__ == "__main__": 
	main()