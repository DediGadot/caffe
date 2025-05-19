import zipfile
import pandas as pd


def _read_acmi_text(path: str) -> str:
    """Return ACMI text from path, handling zipped files."""
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            # look for first file ending with .acmi or .txt
            for name in z.namelist():
                if name.lower().endswith(('.acmi', '.txt')):
                    with z.open(name) as f:
                        return f.read().decode('utf-8', errors='ignore')
            # fall back: read first file
            first = z.namelist()[0]
            with z.open(first) as f:
                return f.read().decode('utf-8', errors='ignore')
    else:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()


def parse_acmi(path: str) -> pd.DataFrame:
    """Parse a Tacview ACMI file and return a DataFrame of events."""
    text = _read_acmi_text(path)
    events = []
    for line in text.splitlines():
        if 'Event=' in line or 'EVENT=' in line:
            event_data = {}
            for part in line.split(','):
                if '=' in part:
                    k, v = part.split('=', 1)
                    event_data[k.strip()] = v.strip()
            event = event_data.get('Event') or event_data.get('EVENT')
            if not event:
                continue
            try:
                lat = float(event_data.get('Lat', event_data.get('LAT', '0')))
                lon = float(event_data.get('Lon', event_data.get('LON', '0')))
            except ValueError:
                lat = 0
                lon = 0
            pilot = event_data.get('Pilot') or event_data.get('PILOT') or ''
            formation = event_data.get('Formation') or event_data.get('GROUP') or ''
            events.append({'event': event, 'lat': lat, 'lon': lon,
                           'pilot': pilot, 'formation': formation})
    return pd.DataFrame(events)

