"""Tool to extract CSS skeleton from an html structure.

	This tool allows a user to copy a block of html, and a formatted
	css structure will be built and will be added to the clipboard to 
	easily paste into a css file. This is desinged to speed up the build 
	process just a little bit more by reducing typing. Eventually this
	may/could be updated to include other formats needed, such as SCSS
	and LESS. In theory this could work on an entire page at once,
	however, its intention was to make copying quick snippets easier.
	eg: <div class="outer-div"><i class="icon"></i></div> will return
		.outer-div{}
		.outer-div .icon{}

	methods:
		copyText: takes param 'textToCopy' and sets it to the clipboard
		getTextFromRegion: takes params: 'stringLocation' and 'active_view'
			and returns a single selected block of text located at 
			stringLocation aka. (0 , 6) coordinates
"""

import sublime, sublime_plugin	
from html.parser import HTMLParser

class HtmlToCssParser(HTMLParser):
	# TODO: move to extended htmlparser class file

	# TODO: make private
	cssData = ''
	wrapperLevels = []
	currentWrapperLevel = 0 
	wrapperPrepend = ''
	tagBreak = '{\n\n}\n'

	def handle_starttag(self, tag, attrs):
		# increase level

		# wrapper index (or WrapperLevels[wrapperindex] = "icon") will always be equal to the currentWrapper level because,
		# we already have the previous level stored (in cssData and prepend ) so we can just overwrite the current level
		# something like if wrapperIndex = currentWrapperLevel.

		# prepend = WrapperLevels[all] eg 1 + 2 + 3

		print("Encountered a start tag:", tag, attrs)
		self.cssData = self.handleAttributes(attrs)
		print(attrs)

	def handle_endtag(self, tag):
		# decrease level since the current tag scope is over, move to next sibling
		print("Encountered an end tag :", tag)
	def handle_data(self, data):
		# we dont care about any tag inner data, put here for easy extension
		print("Encountered some data  :", data)
	def getData(self):
		return self.cssData
	def handleAttributes(self, attrs):
		rtnstr = ''
		#do stuff
		return rtnstr

class grabclass(sublime_plugin.WindowCommand):

	def clearClipboard(self):
		# validation here if needed
		sublime.set_clipboard(' ')
	
	def copyText(self, textToCopy):
		# validation here if needed
		sublime.set_clipboard(textToCopy)

	def getTextFromRegion(self, stringLocation, active_view):
		text = ''
		text = active_view.substr(stringLocation)
		return text

	def convertFromHtml(self, selectedText, returnFormat):
		rtnstr = ''
		if returnFormat is 'CSS':
			print("Converting To CSS")
			parser = HtmlToCssParser()
			# we overwrite parser class methods above to do what we want here
			parser.feed(selectedText) 
			rtnstr = parser.getData()

		#TOOD: add other parsers for scss and other formats
		return rtnstr

	def run(self):
		# grab anything we need: window, selected text, etc..
		window = self.window
		view = window.active_view()
		selections = view.sel()
		selectedText = ''
		textToCopy = ''

		# this will account for selecting multiple regions at once
		for selection in selections:
			selectedText += '\n' + self.getTextFromRegion(selection, view)

		# Now that we have our selected html, pass to to our converter
		if selectedText:
			textToCopy = self.convertFromHtml(selectedText, 'CSS')

		# clear any previous clipboard item
		self.clearClipboard()

		if textToCopy:
			# and finally copy our result to the clipboard
			self.copyText(textToCopy)