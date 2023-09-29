from flask import Flask
import requests
from bs4 import BeautifulSoup
import json


from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "chrome-extension://gaebgamagkkllpjoahlldjafhiegmjji"}})

@app.route('/job_details/<job_id>', methods=['GET'])
def get_job_details(job_id):
    # LinkedIn job URL
    url = f"https://www.linkedin.com/jobs/view/{job_id}/"

    # Send a GET request to the LinkedIn job URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract job details
        title = soup.find("h1", class_="topcard__title")
        company = soup.find("a", class_="topcard__org-name-link")
        # location = soup.find("span", class_="topcard__flavor topcard__flavor--bullet")
        description = soup.find("div", class_="description__text description__text--rich")
        description_text = description.text.split("Show more")[0]

        # Create a dictionary with job details
        job_details = {
            "Role": title.text.strip(),
            "Company": company.text.strip(),
            # "Location": location.text.strip(),
            "Description": description_text.strip()
        }

        # Convert the dictionary to a JSON response
        return json.dumps(job_details), 200, {'Content-Type': 'application/json'}
    else:
        error_message = {"error": f"Unable to access the URL. Status code: {response.status_code}"}
        return json.dumps(error_message), 500, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run()
