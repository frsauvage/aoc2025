"""
Advent of Code utilities for fetching problem texts.
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_session_token():
    """Get AoC session token from aocd config."""
    token_path = Path.home() / '.config' / 'aocd' / 'token'
    return open(token_path).read().strip()


def fetch_problem_part1(year: int, day: int) -> str:
    """
    Fetch Part 1 problem text from Advent of Code website.

    Args:
        year: The year of the puzzle
        day: The day of the puzzle

    Returns:
        The Part 1 problem description as formatted text
    """
    url = f"https://adventofcode.com/{year}/day/{day}"

    session = requests.Session()
    session.cookies.set('session', get_session_token())

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = session.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the first article tag (Part 1)
    article = soup.find('article', class_='day-desc')

    return article.get_text(separator='\n', strip=True) if article else "Part 1 not found"


def fetch_problem_part2(year: int, day: int, max_retries: int = 3) -> str:
    """
    Fetch Part 2 problem text from Advent of Code website.

    Args:
        year: The year of the puzzle
        day: The day of the puzzle
        max_retries: Maximum number of attempts before giving up (default: 3)

    Returns:
        The Part 2 problem description as formatted text
    """
    url = f"https://adventofcode.com/{year}/day/{day}"

    session = requests.Session()
    session.cookies.set('session', get_session_token())

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all article tags
            articles = soup.find_all('article', class_='day-desc')

            # We want the second article (Part 2)
            if len(articles) < 2:
                if attempt < max_retries - 1:
                    continue  # Try again
                return "Part 2 not available yet. Complete Part 1 first!"

            return articles[1].get_text(separator='\n', strip=True)

        except Exception as e:
            if attempt < max_retries - 1:
                continue  # Try again
            raise  # Re-raise the exception after all retries exhausted

    return "Part 2 not available yet."


# Additional helper functions
def parse_grid(data):
    """Parse input into 2D grid (list of lists)."""
    return [list(line) for line in data.strip().split('\n')]


def parse_lines(data):
    """Parse input into list of lines."""
    return data.strip().split('\n')


def parse_blocks(data):
    """Parse input into blocks separated by empty lines."""
    return data.strip().split('\n\n')


def parse_ints(line):
    """Extract all integers from a line (positive and negative)."""
    import re
    return list(map(int, re.findall(r'-?\d+', line)))

