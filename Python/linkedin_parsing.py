# pip install bs4
from typing import Dict, List
from bs4 import BeautifulSoup
import requests, time, re

tag_hier = ["applied", "not-applied", "rejected"]
# To Explore:
# Monday
# Rapyd
# Google
# Databricks
# Istra


def parse_doc(document: str) -> Dict[str, Dict]:
    sections = re.split(r"# ", document)
    if sections[0] == "":
        sections = sections[1:]

    jobs = {}
    for section in sections:
        header, *content = section.split("\n")
        company_name, status = re.match(r"(.+?) #(\S+)", header).groups()

        # Initialize positions list
        positions = []
        info_lines = []
        for line in content:
            # Check if the line is a position link line
            if re.match(r"\[.*?\]\(.*?\)", line):
                position_name = re.search(r"\[(.*?)\]", line).group(1)
                link = re.search(r"\((.*?)\)", line).group(1)
                positions.append({"position_name": position_name, "link": link})
            else:
                info_lines.append(line)

        info = "\n".join(info_lines).strip()
        add_job(jobs, company_name.strip(), status, positions, info)
    return jobs


def read_doc(fp: str) -> Dict[str, Dict]:
    with open(fp, "r") as f:
        return parse_doc(f.read())


def info_from_html(s: str):
    soup = BeautifulSoup(s, "html.parser")
    company_name = soup.find("a", class_="topcard__org-name-link").text.strip()
    position_name = soup.find("h1", class_="topcard__title").text.strip()
    location = soup.find("span", class_="topcard__flavor--bullet").text.strip()
    return company_name, position_name, location


def add_job(
    jobs: Dict[str, Dict],
    company_name: str,
    status: str,
    positions: List[Dict],
    info: str,
):
    if company_name not in jobs:
        jobs[company_name] = {"status": status, "positions": positions, "info": info}
    else:
        existing = jobs[company_name]
        if tag_hier.index(status) < tag_hier.index(existing["status"]):
            existing["status"] = status
        for p in positions:
            for existing_p in existing["positions"]:
                if existing_p["link"] == p["link"]:
                    break
            else:
                existing["positions"].append(p)


def resolve_links(jobs: Dict[str, Dict], links: List[str]):
    for l in links:
        res = requests.get(l)
        company_name, position_name, location = info_from_html(res.content)
        add_job(
            jobs,
            company_name,
            "not-applied",
            [{"position_name": position_name, "link": l}],
            location,
        )
        time.sleep(1)


def canonize_links(links: List[str]) -> List[str]:
    prefix = "https://www.linkedin.com/jobs/view/"
    prefix_length = len(prefix)
    return [prefix + l[prefix_length:].split("/", maxsplit=1)[0] for l in links]


def company_to_row(company_name: str, job: Dict) -> str:
    lines = [f"# {company_name} #{job['status']}"]
    lines.extend([f"[{p['position_name']}]({p['link']})" for p in job["positions"]])
    lines.append(job["info"])
    return "\n".join(lines)


def write_doc(fp: str, jobs: Dict[str, Dict]):
    res = sorted(
        ((name, job) for name, job in jobs.items()),
        key=lambda x: (tag_hier.index(x[1]["status"]), x[0]),
    )
    s = "\n\n".join(company_to_row(name, job) for name, job in res)
    with open(fp, "w") as f:
        f.write(s)


if __name__ == "__main__":
    fp = "/home/user/Desktop/obsidian/Personal/Job Search/Positions.md"
    links = []
    canonized_links = canonize_links(links)
    existing_jobs = read_doc(fp)
    resolve_links(existing_jobs, canonized_links)
    write_doc("text.md", existing_jobs)
