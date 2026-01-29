from flask import Blueprint, request, render_template, jsonify
from app.extensions import mongo
from datetime import datetime
import pytz
import tzlocal


webhook = Blueprint('Webhook', __name__)

# UI Page
@webhook.route("/")
def home():
    return render_template("index.html")

# Webhook Receiver
@webhook.route("/webhook/receiver", methods=["POST"])
def receiver():
    payload = request.json
    event = request.headers.get("X-GitHub-Event")

    doc = None

    # PUSH EVENT
    if event == "push":
        doc = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": "",
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }

    # PULL REQUEST EVENT
    elif event == "pull_request":
        pr = payload["pull_request"]

        action_type = "MERGE" if pr["merged"] else "PULL_REQUEST"

        doc = {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action_type,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow()
        }

    if doc:
        # prevent duplicates
        if not mongo.db.events.find_one({"request_id": doc["request_id"], "action": doc["action"]}):
            mongo.db.events.insert_one(doc)

    return {"status": "saved"}, 200

@webhook.route("/events")
def events():
    data = mongo.db.events.find().sort("timestamp", -1).limit(20)

    # Get machine's local timezone automatically
    local_tz = tzlocal.get_localzone()

    formatted = []

    for e in data:
        # Attach UTC timezone to stored timestamp
        utc_time = e["timestamp"].replace(tzinfo=pytz.utc)

        # Convert to local machine timezone
        local_time = utc_time.astimezone(local_tz)

        # Format nicely
        time_str = local_time.strftime("%d %b %Y %I:%M %p")

        if e["action"] == "PUSH":
            text = f'{e["author"]} pushed to {e["to_branch"]} on {time_str}'
        elif e["action"] == "PULL_REQUEST":
            text = f'{e["author"]} submitted a pull request from {e["from_branch"]} to {e["to_branch"]} on {time_str}'
        elif e["action"] == "MERGE":
            text = f'{e["author"]} merged branch {e["from_branch"]} to {e["to_branch"]} on {time_str}'

        formatted.append(text)

    return jsonify(formatted)


    return jsonify(formatted)
