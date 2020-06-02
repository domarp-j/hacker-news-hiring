import requests
import csv
import re


# "Who is hiring?" Hacker News post ID (June 2020)
POSTING_ID = 23379196

# Search text with following regex patterns (case-insensitive)
LOCATION_PATTERN = "(remote)|(san diego)"
CAREER_PATTERN = "(fullstack)|(full-stack)|(frontend)|(front-end)"
BLACKLIST_PATTERN = "(php)|(wordpress)"

# CSV name
POSTING_CSV = "postings.csv"
BLACKLIST_CSV = "blacklist.csv"

# ==================================================
# Helpers
# ==================================================


def generate_blacklist_cache():
  try:
    blacklist = {}
    with open(BLACKLIST_CSV, 'r') as csv_file:
      for row in csv.reader(csv_file, delimiter=','):
        blacklist[row[0]] = True
    return blacklist
  except FileNotFoundError:
    print("CSV not found. Continuing...")
    return {}


def call_hacker_news_api(id=None):
  return requests.get(
    'https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=id)
  )


# Generate CSV with postings matching criteria above
def write_csv(who_is_hiring={}, blacklist={}):
  with open(POSTING_CSV, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    for comment_id in who_is_hiring["kids"]:
      if str(comment_id) in blacklist:
        print("Ignoring blacklisted post with ID {id}...".format(id=comment_id))
        continue

      print("Fetching post with ID {id}...".format(id=comment_id))
      posting = call_hacker_news_api(id=comment_id)

      if "text" not in posting.json():
        continue

      location_match = re.search(LOCATION_PATTERN, posting.json()["text"].lower())
      career_match = re.search(CAREER_PATTERN, posting.json()["text"].lower())
      blacklist_match = re.search(BLACKLIST_PATTERN, posting.json()["text"].lower())

      if location_match and career_match and not blacklist_match:
        print("Match! Storing in CSV...")
        writer.writerow([
          comment_id,
          posting.json()["text"].replace('\n', "\\n").strip()
        ])


# ==================================================
# Main
# ==================================================

def run():
  print("Storing blacklist in memory...")
  blacklist = generate_blacklist_cache()

  print("Fetching API data for \"Who is hiring?\" post...")
  who_is_hiring = call_hacker_news_api(id=POSTING_ID)

  print("Fetching postings...")
  write_csv(who_is_hiring=who_is_hiring.json(), blacklist=blacklist)

  print("Done!")
