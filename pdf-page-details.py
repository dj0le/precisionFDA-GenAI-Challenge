import pymupdf4llm

data = pymupdf4llm.to_markdown("MERGED_cosmetic_guidances.pdf", page_chunks=True)


from pprint import pprint
pprint(data[4])
