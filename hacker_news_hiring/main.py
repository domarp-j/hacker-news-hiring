import requests
import csv
import re


def call_hacker_news_api(id=None):
  return requests.get(
    'https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=id)
  )


# ==================================================


def run():
  print("Fetching API data for \"Who is hiring?\" post...")
  who_is_hiring = call_hacker_news_api(id=23379196)

  print("Fetching postings...")
  with open('hacker_news_postings.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    for comment_id in who_is_hiring.json()["kids"]:
      posting = call_hacker_news_api(id=comment_id)

      if re.search("(remote)|(san diego)", posting.json()["text"].lower()):
        writer.writerow([
          comment_id,
          posting.json()["text"].replace('\n', ' ').strip()
        ])
