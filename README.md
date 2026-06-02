SalesReps — Commission Sales Rep Finder

Find commission-based, 1099, and independent sales reps in any area. Built with Flask, deployed on Railway.

Table of Contents

Overview
Project Structure
Local Setup
Configuration
Deploy to Railway
Custom Domain
How It Works
Troubleshooting
Overview

SalesReps searches Indeed’s public RSS feed across three targeted queries:

commission sales representative
1099 independent sales rep
outside sales commission only
Results are filtered by location and radius, deduplicated, and displayed in a clean UI.

Project Structure

salesreps/
├── app.py                  # Flask server + search logic
├── templates/
│   └── index.html          # Frontend UI
├── requirements.txt        # Python dependencies
├── Procfile                # Railway/Heroku start command
├── runtime.txt             # Python version pin
├── .gitignore
└── README.md
 
Local Setup

Requirements: Python 3.11+

# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/salesreps.git
cd salesreps
 
# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Run the app
python app.py
 
Open your browser at http://localhost:5000

Configuration

The app works out of the box with no required environment variables. The following optional settings can be configured:

Variable	Default	Description
PORT	5000	Port the app listens on
FLASK_SECRET	salesreps-secret	Flask session secret key — change this in production
Setting environment variables

Locally — create a .env file in the root:

PORT=5000
FLASK_SECRET=your-secret-key-here
 
On Railway — go to your service → Variables tab → add key/value pairs there.

Changing search behavior

To adjust how many results are returned, edit app.py:

if len(results) >= 30:   # change 30 to any number
    break
 
To add or change the search queries, edit the queries list in app.py:

queries = [
    f"commission sales representative {industry}".strip(),
    f"1099 independent sales rep {industry}".strip(),
    f"outside sales commission only {industry}".strip(),
    # add more queries here
]
 
To change the default search radius, edit index.html:

<option value="25" selected>25 mi</option>   <!-- change "25" to your default -->
 
Deploy to Railway

Push this repo to GitHub
Go to railway.app → New Project → Deploy from GitHub repo
Select your salesreps repo
Railway auto-detects Python and deploys — takes about 1 minute
Go to Settings → Networking → click Generate Domain
Your app is live
Re-deploying after changes

git add .
git commit -m "your change description"
git push origin main
 
Railway automatically redeploys on every push to main.

Custom Domain

In Railway → your service → Settings → Networking → Custom Domain
Enter your domain (e.g. salesreps.com)
Railway shows you a CNAME value — copy it
Go to your domain registrar → DNS settings → add a CNAME record:
Type	Name	Value
CNAME	@	(value from Railway)
Wait 5–30 minutes for DNS to propagate — Railway shows a green checkmark when ready
How It Works

User enters a location, optional industry, and radius
Frontend sends a GET /search request with those params
Backend queries the Indeed RSS feed with three commission-focused search terms
Results are parsed from XML, HTML-stripped, deduplicated by URL
Up to 30 results returned as JSON and rendered as cards in the UI
Each card links directly to the full job listing on Indeed
Troubleshooting

No results showing

Try a larger radius (50 or 100 miles)
Try a major nearby city instead of a small town
Indeed RSS can occasionally be slow — try again in a few seconds
App won’t start locally

Make sure Python 3.11+ is installed: python --version
Make sure dependencies are installed: pip install -r requirements.txt
Railway deploy fails

Check the build logs in Railway for the specific error
Make sure Procfile and runtime.txt are committed to the repo
Dependencies

Package	Version	Purpose
Flask	3.1.3	Web framework
gunicorn	23.0.0	Production WSGI server
requests	2.32.5	HTTP requests to Indeed RSS
