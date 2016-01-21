"""


1. fetch http://redbarradio.net/archives
2. Get every URL that starts with http://redbarradio.net/archives/*
3. start threads to fetch each one of these pages

"""
import json
import os
import requests
import grequests

from lxml import html


class Scraper(object):
    def __init__(self):
        self.session = self.get_session()

    def scrape(self):
        pass

    def process_archive_page(self, url):
        pass

    def get_session(self):
        session = requests.session()

        username = os.environ.get("RBR_USERNAME")
        password = os.environ.get("RBR_PASSWORD")

        result = session.post("https://redbarradio.net/login", {
            "log": username,
            "pwd": password,
        })

        #import ipdb; ipdb.set_trace()

        assert result.status_code == 200, "Unable to login?"
        return session

    def get_archive_urls(self):
        if os.path.exists("archive_urls.json"):
            return json.loads(open("archive_urls.json", "r").read())
        else:
            archives_page = self.session.get("https://redbarradio.net/archives")
            doc = html.fromstring(archives_page.content)
            pages = []
            for link in doc.cssselect('a'):
                if "href" in link.attrib and link.attrib["href"].startswith("https://redbarradio.net/archives/"):
                    pages.append(link.attrib["href"])
            with open("archive_urls.json", "w") as archive_file:
                archive_file.write(json.dumps(pages))
            return pages

    def scrape_archives(self):
        pages = self.get_archive_urls()
        rs = (grequests.get(u, session=self.session) for u in pages)
        all_show_notes = {}
        for result in grequests.imap(rs):
            print("On URL ->", result.url)
            doc = html.fromstring(result.content)
            all_show_notes[result.url.split("/")[-1]] = {
                "title": doc.cssselect("header h2 a")[0].text_content(),
                "notes": doc.cssselect(".post-contents.cf p")[1].text_content().strip(),
                "date": "{} {}".format(
                    doc.cssselect(".date .day")[0].text_content(),
                    doc.cssselect(".date .month")[0].text_content()
                )
            }
        with open("show_notes.json", "w") as show_notes_file:
            show_notes_file.write(json.dumps(all_show_notes))
        print("Done and saved!")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape_archives()
