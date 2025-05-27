import requests
from bs4 import BeautifulSoup

def extract_job_text(url):
    #ateempts to extract text from the website
    headers = {
        "User-Agent": "Mozilla/5.0" #used to bypass the bot or script flag
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Combine all paragraph text
        paragraphs = soup.find_all("p")
        job_text = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text()) > 30)

        # Check for Cloudflare or JavaScript protections
        if "enable javascript" in job_text.lower() or "cloudflare" in job_text.lower():
            return "⚠️ This job link is protected. In such cases, please copy and paste the job description manually."

        return job_text.strip() if job_text else "⚠️ No readable job description found. Please paste it manually."

    except Exception as e:
        return f"⚠️ Error while extracting: {e}"
