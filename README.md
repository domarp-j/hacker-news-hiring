# Hacker News Hiring Script

This is a small Python script that uses the [Hacker News API](https://github.com/HackerNews/API) to fetch job postings from a Hacker News "Who is hiring?" post that match certain search criteria.

## Dependencies

Your system's Python version should match the version specified in `pyproject.toml`.

For now, this script requires using [poetry](https://python-poetry.org/) to run the job finder script.

## Usage

1. Pull down this repository to your local machine.
1. Run `poetry install` to install dependencies.
1. Run the job search script `poetry run find-jobs` from within the root directory. This will create a CSV file containing relevant job postings.
1. (Optional) Add a `blacklist.csv` file if you want any posts to be excluded from the output CSV. It only needs a single row containing the Hacker News IDs of posts that should be ignored.
