import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

api_key = os.environ["API_FOOTBALL_KEY"]
today = datetime.now(ZoneInfo("America/New_York")).date().isoformat()

url = f"https://v3.football.api-sports.io/fixtures?date={today}"
request = urllib.request.Request(
    url,
    headers={"x-apisports-key": api_key}
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)

if data.get("errors"):
    raise RuntimeError(str(data["errors"]))

fixtures = []

for item in data.get("response", []):
    fixtures.append({
        "id": item["fixture"]["id"],
        "home": item["teams"]["home"]["name"],
        "away": item["teams"]["away"]["name"],
        "homeGoals": item["goals"]["home"],
        "awayGoals": item["goals"]["away"],
        "status": item["fixture"]["status"]["short"],
        "kickoff": item["fixture"]["date"]
    })

output = {
    "date": today,
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "fixtures": fixtures
}

Path("scores.json").write_text(json.dumps(output) + "\n")
print(f"Fetched {len(fixtures)} matches")
