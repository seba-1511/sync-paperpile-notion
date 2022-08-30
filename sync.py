
import bibtexparser
import json
import os
import pickle
import pprint
import requests

"""
TODO:
- Default icon for papers.
"""

ARCHIVE_PATH = 'archive.pk'
BIB_PATH = 'references.bib'
NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_IDENTIFIER = os.environ['DATABASE_IDENTIFIER']


def notion_add_entry(
    title='',
    authors='',
    year='0',
    ref_id='',
    link='',
):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {
            'database_id': DATABASE_IDENTIFIER,
        },
        "properties": {
            'Title': {
                'title': [{
                    'text': {
                        'content': title,
                        }
                    }]
                },
            'Authors': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": authors,
                    }
                }],
            },
            'Year': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": year,
                    }
                }],
            },
            'Reference ID': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": ref_id,
                    }
                }],
            },
            'Link': {
                "url": link,
            },
                    
                    
        },
    }
    #  pprint.pprint(payload)
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)
    #  pprint.pprint(json.loads(response.text))


def notion_update_page(
    page_id,
    title='',
    authors='',
    year='0',
    ref_id='',
    link='',
):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "parent": {
            'database_id': DATABASE_IDENTIFIER,
        },
        "properties": {
            'Title': {
                'title': [{
                    'text': {
                        'content': title,
                        }
                    }]
                },
            'Authors': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": authors,
                    }
                }],
            },
            'Year': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": year,
                    }
                }],
            },
            'Reference ID': {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": ref_id,
                    }
                }],
            },
            'Link': {
                "url": link,
            },
                    
                    
        },
    }
    #  pprint.pprint(payload)
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_TOKEN}"
    }
    response = requests.patch(url, json=payload, headers=headers)


def notion_fetch_page(ref_id):
    url = f"https://api.notion.com/v1/databases/{DATABASE_IDENTIFIER}/query"

    # list database pages
    payload = {
        "page_size": 1,
        "filter": {
            'property': 'Reference ID',
            'rich_text': {"equals": ref_id},
        },
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_TOKEN}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    response = json.loads(response.text)
    #  pprint.pprint(response)
    try:
        if len(response['results']) > 0:
            return response['results'][0]['id']
    except:
        return -1
    return -1


def clean_str(string):
    string = string.strip()
    string = string.replace('\n', ' ')
    string = string.replace(r'\"a', 'ä')
    string = string.replace(r'\"e', 'ë')
    string = string.replace(r'\"i', 'ï')
    string = string.replace(r'\"o', 'ö')
    string = string.replace(r'\"u', 'ü')
    string = string.replace(r'\'a', 'á')
    string = string.replace(r'\'e', 'é')
    string = string.replace(r'\'i', 'í')
    string = string.replace(r'\'o', 'ó')
    string = string.replace(r'\'u', 'ú')
    string = string.replace(r'\^a', 'â')
    string = string.replace(r'\^e', 'ê')
    string = string.replace(r'\^i', 'î')
    string = string.replace(r'\^o', 'ô')
    string = string.replace(r'\^u', 'û')
    string = string.replace(r'\`a', 'à')
    string = string.replace(r'\`e', 'è')
    string = string.replace(r'\`i', 'ì')
    string = string.replace(r'\`o', 'ò')
    string = string.replace(r'\`u', 'ù')
    string = ' '.join([w.title() if w.islower() else w for w in string.split()])
    string = string.replace('{', '')
    string = string.replace('}', '')
    return string


def main():

    # instantiate the parser
    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = True
    parser.homogenize_fields = False
    parser.interpolate_strings = False

    with open(BIB_PATH) as bib_file:
        bibliography = bibtexparser.load(bib_file, parser=parser)

    if os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, 'rb') as archive_file:
            archive = pickle.load(archive_file)
    else:
        archive = []
    archive_ids = [e['ID'] for e in archive]

    # add each entry to notion database
    update_archive = False
    for entry in reversed(bibliography.entries):

        title = entry.get('title', '')
        title = clean_str(title)
        title = title

        authors = entry.get('author', '')
        authors = authors.replace(' and ', '; ')
        authors = clean_str(authors)

        year = entry.get('year', '')
        link = entry.get('url', '')
        ref_id = entry.get('ID')

        if ref_id not in archive_ids: # new page
            notion_add_entry(
                title=title,
                authors=authors,
                year=year,
                ref_id=ref_id,
                link=link,
            )
            update_archive = True
        elif entry not in archive: # update existing page
            page_id = notion_fetch_page(ref_id)
            if page_id != -1:
                notion_update_page(
                    page_id=page_id,
                    title=title,
                    authors=authors,
                    year=year,
                    ref_id=ref_id,
                    link=link,
                )
                update_archive = True

    # only update the archive if necessary
    if update_archive:
        with open(ARCHIVE_PATH, 'wb') as archive_file:
            archive = pickle.dump(bibliography.entries, archive_file)


if __name__ == "__main__":
    main()
