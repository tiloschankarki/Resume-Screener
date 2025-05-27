import requests
from bs4 import BeautifulSoup

def extract_job_text(url):
    #attempts to extract text from a job posting url, if not extracted provides error message
    headers = {
        "User-Agent": "Mozilla/5.0" #used so that the browser wont flag it as a bot or a script
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Very naive extraction
        paragraphs = soup.find_all("p")
        job_text = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text()) > 30)
        
        return job_text.strip() if job_text else "⚠️ Couldn't extract job description. Try pasting it manually."
    
    except Exception as e:
        return f"⚠️ Error while extracting: {e}"
