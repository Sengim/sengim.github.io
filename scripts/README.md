# Publication Management Scripts

## add_publication.py

Interactive script to add a new publication to your site from a BibTeX entry.

### Usage

1. Get the BibTeX citation from Google Scholar:
   - Go to your publication on Google Scholar
   - Click the "Cite" button (quotation mark icon)
   - Click "BibTeX" at the bottom
   - Copy the entire BibTeX entry

2. Run the script:
   ```bash
   python3 scripts/add_publication.py
   ```

3. Paste your BibTeX entry when prompted

4. Press `CTRL+D` (Linux/Mac) or `CTRL+Z` then `Enter` (Windows) to finish input

5. Review the extracted information and confirm

The script will:
- Parse your BibTeX entry
- Extract title, authors, year, venue, DOI, and URL
- Create a properly formatted markdown file in `_publications/`
- Include the full BibTeX citation
- Add links to Google Scholar, DOI, and paper URL

### Example

```
$ python3 scripts/add_publication.py
======================================================================
Add New Publication
======================================================================

Paste your BibTeX entry below.
Press CTRL+D (Linux/Mac) or CTRL+Z then Enter (Windows) when done:

@article{karayalcin2023resolving,
  title={Resolving the doubts: On the construction and use of resnets for side-channel analysis},
  author={Karayalcin, Sengim and Perin, Guilherme and Picek, Stjepan},
  journal={Mathematics},
  volume={11},
  number={19},
  pages={4101},
  year={2023},
  publisher={MDPI}
}
^D

======================================================================
Parsing BibTeX...
======================================================================

Extracted information:
  Title:   Resolving the doubts: On the construction and use of resnets for side-channel analysis
  Authors: Karayalcin, Sengim, Perin, Guilherme, Picek, Stjepan
  Year:    2023
  Venue:   Mathematics

======================================================================
Create publication file? (y/n): y

======================================================================
✓ Publication created: 2023-01-01-resolving-the-doubts-on-the-construction-and-use-of-resnets-for-side-channel-analysis.md
  Location: _publications/2023-01-01-resolving-the-doubts-on-the-construction-and-use-of-resnets-for-side-channel-analysis.md
======================================================================
```

### Notes

- The script automatically formats author names and cleans up the citation
- Files are named using the pattern: `YEAR-01-01-title-slug.md`
- If a file with the same name exists, you'll be asked to confirm overwrite
- The BibTeX entry is stored in the markdown file for future reference
