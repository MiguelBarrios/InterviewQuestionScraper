from bs4 import BeautifulSoup
import requests
import re
import io
import sys

def app(initial_url, output_file_name):
    base_url = 'https://www.glassdoor.com';
    QUESTIONS = set()
    visited = set()
    links = [initial_url]
    while len(links) > 0:
        current_url = links.pop()
        response = requests.get(current_url)
        html = response.content
        soup =  BeautifulSoup(html, 'html.parser')
        questions = scrape_page_questions(soup);
        QUESTIONS.update(questions)
        urls = get_next_page_urls(soup)
        for url in urls:
            if url not in visited:
                visited.add(url)
                links.append(base_url + url)
    write_to_file(QUESTIONS, output_file_name)

def scrape_page_questions(soup):
    interview_question_containers = soup.find_all(attrs={"data-test": re.compile("Interview.*Questions")})
    questions = [container.find('span').text for container in interview_question_containers]
    return questions

def get_next_page_urls(soup):
    link_containers = soup.find_all(attrs={"data-test": re.compile("pagination-link-")})
    links = [a['href'] for a in link_containers]
    return links

def write_to_file(data, output_file_name):
    with open(output_file_name, 'w') as f:
        f.writelines(line + '\n\n' for line in data)

if __name__ == "__main__":
    initial_url = sys.argv[1]
    output_file_name = sys.argv[2]
    app(initial_url, output_file_name)
