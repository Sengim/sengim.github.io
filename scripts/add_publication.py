#!/usr/bin/env python3
"""
Interactive script to add a new publication from BibTeX
"""

import re
import os
from datetime import datetime

def parse_bibtex(bibtex):
    """Parse BibTeX entry and extract key information"""
    data = {}

    # Extract title
    title_match = re.search(r'title\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE | re.DOTALL)
    if title_match:
        data['title'] = title_match.group(1).strip().replace('\n', ' ')

    # Extract authors
    author_match = re.search(r'author\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE | re.DOTALL)
    if author_match:
        authors = author_match.group(1).strip().replace('\n', ' ')
        # Clean up author format
        authors = re.sub(r'\s+and\s+', ', ', authors)
        data['authors'] = authors

    # Extract year
    year_match = re.search(r'year\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE)
    if year_match:
        data['year'] = year_match.group(1).strip()

    # Extract venue (journal, booktitle, or venue)
    venue_match = re.search(r'(?:journal|booktitle|venue)\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE | re.DOTALL)
    if venue_match:
        data['venue'] = venue_match.group(1).strip().replace('\n', ' ')
    else:
        data['venue'] = ''

    # Extract DOI
    doi_match = re.search(r'doi\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE)
    if doi_match:
        data['doi'] = doi_match.group(1).strip()

    # Extract URL
    url_match = re.search(r'url\s*=\s*[{"](.*?)[}"]', bibtex, re.IGNORECASE)
    if url_match:
        data['url'] = url_match.group(1).strip()

    return data

def create_markdown_filename(title, year):
    """Create a filename from title and year"""
    # Remove special characters and convert to lowercase
    clean_title = re.sub(r'[^\w\s-]', '', title.lower())
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    clean_title = clean_title[:80]  # Limit length
    return f"{year}-01-01-{clean_title}.md"

def create_permalink(title, year):
    """Create permalink from title and year"""
    clean_title = re.sub(r'[^\w\s-]', '', title)
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    return f"/publication/{year}-01-01-{clean_title}"

def create_publication_markdown(data, bibtex, category):
    """Create markdown content for a publication"""

    # Format the citation
    citation = f'{data["authors"]}, "{data["title"]}" {data["venue"]}, {data["year"]}.'

    # Build markdown content
    content = f"""---
title: "{data['title']}"
collection: publications
category: {category}
permalink: {create_permalink(data['title'], data['year'])}
date: {data['year']}-01-01
venue: '{data['venue']}'
citation: '{citation}'
"""

    # Add paper URL if available
    if 'url' in data:
        content += f"paperurl: '{data['url']}'\n"

    # Add BibTeX
    content += "bibtex: |\n"
    for line in bibtex.strip().split('\n'):
        content += f"  {line}\n"

    content += "---\n\n"

    # Add links
    scholar_search = data['title'].replace(' ', '+')
    content += f"[Google Scholar](https://scholar.google.com/scholar?q={scholar_search}){{:target=\"_blank\"}}\n"

    if 'doi' in data:
        content += f"\n[DOI: {data['doi']}](https://doi.org/{data['doi']}){{:target=\"_blank\"}}\n"

    if 'url' in data:
        content += f"\n[Paper]({data['url']}){{:target=\"_blank\"}}\n"

    return content

def main():
    print("=" * 70)
    print("Add New Publication")
    print("=" * 70)
    print("\nPaste your BibTeX entry below.")
    print("Press CTRL+D (Linux/Mac) or CTRL+Z then Enter (Windows) when done:\n")

    # Read multiline BibTeX input
    bibtex_lines = []
    try:
        while True:
            line = input()
            bibtex_lines.append(line)
    except EOFError:
        pass

    bibtex = '\n'.join(bibtex_lines)

    if not bibtex.strip():
        print("\nNo BibTeX entry provided. Exiting.")
        return

    print("\n" + "=" * 70)
    print("Parsing BibTeX...")
    print("=" * 70)

    # Parse BibTeX
    data = parse_bibtex(bibtex)

    # Display extracted information
    print("\nExtracted information:")
    print(f"  Title:   {data.get('title', 'NOT FOUND')}")
    print(f"  Authors: {data.get('authors', 'NOT FOUND')}")
    print(f"  Year:    {data.get('year', 'NOT FOUND')}")
    print(f"  Venue:   {data.get('venue', 'NOT FOUND')}")

    # Validate required fields
    if not all(key in data for key in ['title', 'authors', 'year']):
        print("\nERROR: Missing required fields (title, authors, year)")
        return

    # Ask for category
    print("\n" + "=" * 70)
    print("Publication type:")
    print("  1. Conference paper")
    print("  2. Journal article")
    category_choice = input("Select type (1 or 2): ").strip()

    if category_choice == '1':
        category = 'conferences'
    elif category_choice == '2':
        category = 'manuscripts'
    else:
        print("Invalid choice. Defaulting to conference paper.")
        category = 'conferences'

    # Ask for confirmation
    print("\n" + "=" * 70)
    response = input("Create publication file? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return

    # Create publications directory if it doesn't exist
    pub_dir = "_publications"
    os.makedirs(pub_dir, exist_ok=True)

    # Create filename and filepath
    filename = create_markdown_filename(data['title'], data['year'])
    filepath = os.path.join(pub_dir, filename)

    # Check if file already exists
    if os.path.exists(filepath):
        print(f"\nWARNING: File already exists: {filename}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    # Create markdown content
    markdown_content = create_publication_markdown(data, bibtex, category)

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print("\n" + "=" * 70)
    print(f"✓ Publication created: {filename}")
    print(f"  Location: {filepath}")
    print("=" * 70)

if __name__ == "__main__":
    main()
