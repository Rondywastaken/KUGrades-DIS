import requests
from bs4 import BeautifulSoup

def get_entry(soup: BeautifulSoup, label: str) -> str:
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if label in tds[0].text:
            return tds[1].text.strip()
    raise ValueError(f"Label {label} can't be found")

def get_grades(soup: BeautifulSoup) -> dict[str, int]:
    grades = {}
    for tr in soup.find_all("table")[2].find_all("tr")[1::]:
        tds = tr.find_all("td")
        grades[tds[0].text.strip()] = int(tds[1].text.strip())
    return grades

def get_entry_reexam(soup: BeautifulSoup, label: str) -> str:
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) == 5 and label in tds[3].text:
            return tds[4].text.strip()
        elif len(tds) == 4 and label in tds[2].text:
            return tds[3].text.strip()
    raise ValueError(f"Label {label} can't be found")

def get_grades_reexam(soup: BeautifulSoup) -> dict[str, int]:
    grades = {}
    for tr in soup.find_all("table")[4].find_all("tr")[1::]:
        tds = tr.find_all("td")
        grades[tds[0].text.strip()] = int(tds[1].text.strip())
    return grades

"""

Not sure if we need this function anyways

def get_other_terms(soup):
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if "Andre versioner" in tds[0].text:
            return [{"term": a.text.strip(), "url": a["href"]} for a in tds[1].find_all("a")]
"""
def parse_link(link: str) -> tuple[str, dict]:
    try:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, "html.parser")

        link_split = link.split("/")
        key = f"{link_split[-3]}-{link_split[-2]}-{link_split[-1]}"

        data = {}

        data["title"] = soup.find("h2").text.strip()
        data["term"] = get_entry(soup, "Termin")
        data["ects"] = get_entry(soup, "ECTS")
        
        """
        # not all terms have other terms section. leaving empty if not
        try:
            # remove other terms (for some reason url with just B1 other terms shows itself but not for urls with B1-1,
            # removing the term itself from other terms
            data["other_terms"] = []
            for tr in soup.find_all("tr"):
                tds = tr.find_all("td")
                if "Andre versioner" in tds[0].text:
                    data["other_terms"] = [a.text.strip() for a in tds[1].find_all("a") if a.text.strip() != data["term"]]
                    break
        except BaseException:
            data["other_terms"] = []
        """

        no_data_str = "Fordelingen vises ikke da tre eller færre har været til denne eksamen."
        if soup.find_all("table")[1].find("td").text.strip() == no_data_str :
            data["exam"] = False
            return key, data

        data["exam"] = True
        data["registered"] = get_entry(soup, "Antal tilmeldte") 
        data["attended"] = get_entry(soup, "Fremmødte") 
        data["passed"] = get_entry(soup, "Antal bestået").split()[0] # Only get the amount of passed
        data["grades"] = get_grades(soup)


        # Check if reexam scraping is needed
        if soup.find_all("table")[3].find("td").text.strip() == no_data_str :
            data["reexam"] = False
            return key, data

        data["reexam"] = True
        data["registered_reexam"] = get_entry_reexam(soup, "Antal tilmeldte") 
        data["attended_reexam"] = get_entry_reexam(soup, "Fremmødte") 
        data["passed_reexam"] = get_entry_reexam(soup, "Antal bestået").split()[0] # Only get the amount of passed
        data["grades_reexam"] = get_grades_reexam(soup)

        return key, data
    except Exception as e:
        print(f"Failed on {link}: {e}")
        return link, {"error": str(e)}
