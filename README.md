# **GitHub Webhook Event Monitoring System**

## **Overview**

This project is a real-time GitHub repository activity monitoring system. It captures repository events using **GitHub Webhooks**, stores the event data in **MongoDB Atlas**, and displays the latest activity on a web dashboard that refreshes every **15 seconds**.

The system demonstrates backend integration, webhook handling, secure configuration management, database storage, timezone-aware rendering, and frontend data presentation using a production-style architecture.

---

## **Features**

* Captures GitHub **Push**, **Pull Request**, and **Merge** events
* Stores structured event data in **MongoDB Atlas**
* Prevents duplicate event storage
* Displays repository activity in a dashboard UI
* Automatically refreshes event feed every 15 seconds
* Converts UTC timestamps to the **machine’s local timezone**
* Secure configuration using **environment variables**
* Modular Flask application using **Blueprints**
* Cloud database integration

---

## **Architecture Flow**

GitHub Repository (action-repo)
→ GitHub Webhook Event
→ Flask Webhook Endpoint (`/webhook/receiver`)
→ MongoDB Atlas (Event Storage in UTC)
→ Flask API (`/events`)
→ Frontend Dashboard (Polling every 15 seconds)

---

## **Tech Stack**

| Layer             | Technology Used       |
| ----------------- | --------------------- |
| Backend           | Flask (Python)        |
| Database          | MongoDB Atlas (Cloud) |
| Frontend          | HTML, CSS, JavaScript |
| Integration       | GitHub Webhooks       |
| Tunneling         | ngrok (local testing) |
| Timezone Handling | pytz, tzlocal         |

---

## **Supported GitHub Events**

### **Push Event**

**Format:**
`{author} pushed to {to_branch} on {timestamp}`

### **Pull Request Event**

**Format:**
`{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`

### **Merge Event**

**Format:**
`{author} merged branch {from_branch} to {to_branch} on {timestamp}`

---

## **API Endpoints**

| Endpoint            | Method | Description                             |
| ------------------- | ------ | --------------------------------------- |
| `/`                 | GET    | Loads the dashboard UI                  |
| `/webhook/receiver` | POST   | Receives GitHub webhook events          |
| `/events`           | GET    | Returns formatted event data for the UI |

---

## **Database Schema**

Each event document stored in MongoDB contains:

| Field       | Description                          |
| ----------- | ------------------------------------ |
| request_id  | Unique event identifier              |
| author      | GitHub user who performed the action |
| action      | PUSH / PULL_REQUEST / MERGE          |
| from_branch | Source branch (if applicable)        |
| to_branch   | Target branch                        |
| timestamp   | UTC time of event                    |

---

## **Timezone Handling**

All timestamps are stored in **UTC** for consistency.
When events are sent to the UI, they are converted to the **local timezone of the machine** running the Flask application using **tzlocal**. This ensures proper display while maintaining database standardization.

---

## **Environment Configuration**

This project uses environment variables for secure configuration.

Create a file named **`.env`** in the project root and add:

```
MONGO_URI=your_mongodb_connection_string
```

**Example:**

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/github_events?retryWrites=true&w=majority
```

The `.env` file is excluded from Git using `.gitignore`.

---

## **How to Run Locally**

### **1. Clone the repository**

```
git clone <your-webhook-repo-link>
cd webhook-repo
```

### **2. Create virtual environment**

```
python -m venv venv
venv\Scripts\activate
```

### **3. Install dependencies**

```
pip install -r requirements.txt
```

### **4. Create `.env` file**

Add your MongoDB Atlas connection string.

### **5. Run the Flask server**

```
python run.py
```

Server runs at:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## **Connecting GitHub Webhooks**

### **1. Start ngrok**

```
ngrok http 5000
```

### **2. Copy the HTTPS forwarding URL**

### **3. Configure webhook in action-repo**

Go to **Settings → Webhooks → Add Webhook**

* **Payload URL:**
  `https://your-ngrok-url/webhook/receiver`
* **Content Type:** `application/json`
* **Events:** Push, Pull Requests

---

## **Testing the System**

Perform the following in the action-repo:

* Commit code (Push event)
* Create a Pull Request
* Merge a Pull Request

The dashboard will update automatically every 15 seconds.

---

## **Project Structure**

```
app/
 ├── __init__.py
 ├── extensions.py
 ├── templates/index.html
 ├── static/script.js
 └── webhook/routes.py

run.py
requirements.txt
README.md
.gitignore
```

---

## **Notes**

* MongoDB Atlas is used to simulate a production-style cloud database.
* All secrets are stored securely using environment variables.
* ngrok is used only for local webhook testing.
* The project follows best practices for webhook handling and time management.

---

## **Author**

Tanveer Ahmad
