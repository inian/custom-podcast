class FeedItem(object):
	"""docstring for FeedItem"""
	def __init__(self, id=None, title=None, link=None, mimeType=None, length=None, description=None):
		super(FeedItem, self).__init__()
		self.id = id
		self.title = title
		self.link = link
		self.type = mimeType
		self.length = length
		self.description = description
	