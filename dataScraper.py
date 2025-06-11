import requests
from bs4 import BeautifulSoup
import pandas as pd

def list_to_sentence(lst):
    if not lst:
        return 'None'
    elif len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return f"{lst[0]} and {lst[1]}"
    else:
        return f"{', '.join(lst[:-1])}, and {lst[-1]}"

def Scrape():
    faculty_impacts = []
    faculty_interests = []

    response = requests.get('https://www.cockrell.utexas.edu/faculty-directory/')
    soup = BeautifulSoup(response.text, 'html.parser')

    contact_elements = soup.select('.contact')
    email_elements = soup.select('.email')
    impact_elements = soup.select('.impact')
    name_elements = soup.find_all('h4')
    research_elements = soup.select('.facareas')

    # ----- Extract Impact Areas -----
    for impact_element in impact_elements:
        if 'class="test"' in str(impact_element):  # Optional: refine if needed
            paragraphs = impact_element.find_all('p')
            cleaned_texts = [p.get_text().strip() for p in paragraphs]
            faculty_impacts.append(list_to_sentence(cleaned_texts))
        else:
            faculty_impacts.append('None')

    # ----- Extract and Convert Research Interests -----
    for research_block in research_elements:
        paragraphs = research_block.find_all('p')
        if len(paragraphs) >= 2:
            # Get second <p> and split into list on semicolon
            interest_raw = paragraphs[1].get_text(strip=True)
            interest_list = [item.strip() for item in interest_raw.split(';') if item.strip()]
        else:
            interest_list = []

        faculty_interests.append(interest_list)

    # ----- Build Final Faculty Data -----
    faculty_data = []
    email_offset = 0

    for i in range(len(name_elements)):
        name = name_elements[i].getText().strip()
        impact = faculty_impacts[i] if i < len(faculty_impacts) else 'None'
        interest = faculty_interests[i] if i < len(faculty_interests) else []

        if 'email' in str(contact_elements[i]):
            email = email_elements[i - email_offset].getText().strip()
        else:
            email = None
            email_offset += 1
            print("Missing email for:", name)

        faculty_data.append([name, email, impact, interest])

    # ----- Create DataFrame -----
    df = pd.DataFrame(faculty_data, columns=['Name', 'Email', 'Impact', 'Research Interests'])
    df.to_csv('output.csv', index=False)
    return df
