# Tacview Analyzer App

This is a simple Flask web application for analyzing Tacview DCS World recordings.

## Features

- Upload `.acmi` or zipped Tacview files.
- Summarize events per pilot and per formation.
- Display most important events on an interactive map.
- Click event names to focus on the corresponding map marker.

## Requirements

Install dependencies in a virtual environment:

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Then open `http://localhost:5000` in your web browser.

## Notes

The application now includes a simple ACMI parser capable of extracting basic event information (event name, pilot, formation and coordinates). It does not implement the full Tacview specification but works with common event lines found in typical recordings.
