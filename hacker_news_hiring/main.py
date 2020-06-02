import requests
import csv
import re


# "Who is hiring?" Hacker News post ID (June 2020)
POSTING_ID = 23379196

# Search text with following regex patterns (case-insensitive)
LOCATION_PATTERN = "(remote)|(san diego)"
CAREER_PATTERN = "(fullstack)|(full-stack)|(frontend)|(front-end)|(software engineer)"

# CSV name
CSV_NAME = "hacker_news_postings.csv"


# ==================================================
# Helpers
# ==================================================


def call_hacker_news_api(id=None):
  return requests.get(
    'https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=id)
  )


# Create an in-memory cache containing HN posts that have already been queried
def store_existing_csv_data():
  try:
    comment_ids = {}
    with open(CSV_NAME) as csv_file:
      for row in csv.reader(csv_file, delimiter=','):
        comment_ids[row[0]] = True
    return comment_ids
  except FileNotFoundError:
    print("CSV not found.")
    return {}


# Generate CSV with postings matching criteria above
def write_csv(who_is_hiring={}):
  with open(CSV_NAME, 'a+') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    for comment_id in who_is_hiring["kids"]:
      print("Fetching post with ID {id}...".format(id=comment_id))
      posting = call_hacker_news_api(id=comment_id)

      if "text" not in posting.json():
        continue

      location_match = re.search(LOCATION_PATTERN, posting.json()["text"].lower())
      career_match = re.search(CAREER_PATTERN, posting.json()["text"].lower())

      if location_match and career_match:
        print("Match! Storing in CSV...")
        writer.writerow([
          comment_id,
          posting.json()["text"].replace('\n', "\\n").strip()
        ])


# ==================================================
# Main
# ==================================================

def run():
  print("Fetching API data for \"Who is hiring?\" post...")
  who_is_hiring = call_hacker_news_api(id=POSTING_ID)

  print("Fetching postings...")
  write_csv(who_is_hiring=who_is_hiring.json())

  print("Done!")
