import pandas as pd
import random
from dataScraper import Scrape
from emailSender import send_email

df = Scrape()
Subject = 'Student Interested in Volunteering in Your Lab'

for index, row in df.iterrows():
    name = row['Name']
    email = row['Email']
    impact = row['Impact']
    interests = row['Research Interests']

    if pd.isna(email) or not interests or not isinstance(interests, list):
        continue

    interest_sample = random.choice(interests)
    # MODIFY THIS
    Body = f"""Dear {name},

My name is [Your Name], and I’m a [School Level] student with strong interests in {impact}. I came across your profile in the Cockrell School of Engineering directory and was fascinated by your work, particularly in {interest_sample}.

Your research is truly inspiring, and I would be incredibly grateful for an opportunity to get involved in any capacity—whether through volunteering, helping with lab tasks, or observing ongoing projects. I’m eager to learn and contribute, even in small ways, while gaining firsthand experience in an engineering research environment.

Please let me know if there's a way I could be helpful to your team or if there are any steps I should take to be considered. I’d be happy to share more about my background, interests, or availability.

Thank you for your time and consideration.

Best regards,  
[Your Full Name]"""

    send_email(Subject, Body, email)
