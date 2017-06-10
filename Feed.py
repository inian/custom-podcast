from feedgen.feed import FeedGenerator

class Feed(object):
    """docstring for Feed"""

    def __init__(self, title=None, link=None, description=None):
        super(Feed, self).__init__()
        self.title = title
        self.link = link
        self.description = description
        self.items = []

    def addEntry(self, fi):
        self.items.append(fi)

    def writeFeed(self, filepath):
        fg = FeedGenerator()

        fg.load_extension('podcast')
        fg.podcast.itunes_category('Technology', 'Podcasting')
        fg.podcast.itunes_author('Inian')
        fg.podcast.itunes_subtitle(self.description)
        fg.podcast.itunes_summary(self.description)
        fg.podcast.itunes_image(
            "https://static.pexels.com/photos/174/coffee-apple-iphone-laptop.jpg")

        fg.title(self.title)
        fg.link(href=self.link, rel='alternate')
        fg.description(self.description)

        for item in self.items:
            fe = fg.add_entry()
            fe.id(item.id)
            fe.title(item.title)
            # fe.link({"href": item.link})
            fe.description(item.description)
            fe.enclosure(item.link, item.length, item.type)

        fg.rss_str(pretty=True)
        fg.rss_file(filepath)
