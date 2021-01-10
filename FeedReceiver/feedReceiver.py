import feedparser


class FeedReceiver:

    def check_feeds(self,link):
        self.NewsFeed = feedparser.parse(link)
    def get_feeds(self):
        return self.NewsFeed.entries
