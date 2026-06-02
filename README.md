cd /home/user/salesreps
git remote add origin https://github.com/YOUR_USERNAME/salesreps.git
git push -u origin main

salesreps/
├── app.py              ← Flask server + Indeed search
├── templates/
│   └── index.html      ← Full UI
├── requirements.txt    ← Flask + requests + gunicorn
├── Procfile            ← Railway start command
├── runtime.txt         ← Python 3.11
├── .gitignore
└── README.md
