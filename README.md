# ☕ jug_barcamp2ics

A small tool for generating an ICS file from the [Entwickelbar](https://entwickelbar.github.io/) schedule by the [Java User Group Düsseldorf](https://rheinjug.de/) and creates a calendar file you can import into your favorite calendar app.

## Dependencies

This tool requires the following Python packages: bs4, requests

You can install them via pip:

```python
pip install beautifulsoup4 requests
```

## Note

In the main.py script, the date for the next event must be set manually. Open the file and update the date variable to the desired date before running the script.

Example:
```python
URL = "https://entwickelbar.github.io/"
date = datetime.date(2025, 9, 13)
```

## Disclaimer

This project is independent and has no affiliation with the event or the user group.
