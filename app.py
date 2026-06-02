from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    location = ""
    error = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        location = request.form.get("location", "").strip()

        if not query:
            error = "Please enter a job title or keyword to search."
        else:
            try:
                # Indeed public job search via their RSS feed
                params = {
                    "q": query,
                    "l": location,
                    "sort": "date",
                    "limit": 25,
                }
                response = requests.get(
                    "https://www.indeed.com/rss",
                    params=params,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10,
                )
                response.raise_for_status()

                # Parse the RSS XML for job listings
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                channel = root.find("channel")
                if channel is not None:
                    for item in channel.findall("item"):
                        title = item.findtext("title", default="N/A")
                        company = item.findtext(
                            "{http://www.indeed.com/}company", default="N/A"
                        )
                        loc = item.findtext(
                            "{http://www.indeed.com/}city", default=""
                        )
                        link = item.findtext("link", default="#")
                        pub_date = item.findtext("pubDate", default="")
                        results.append(
                            {
                                "title": title,
                                "company": company,
                                "location": loc,
                                "link": link,
                                "date": pub_date,
                            }
                        )
            except requests.exceptions.Timeout:
                error = "The search request timed out. Please try again."
            except requests.exceptions.RequestException as e:
                error = f"Could not reach the job search service: {e}"
            except Exception as e:
                error = f"An unexpected error occurred: {e}"

    return render_template(
        "index.html",
        results=results,
        query=query,
        location=location,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=False)
