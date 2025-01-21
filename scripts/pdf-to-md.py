import pymupdf4llm

data = pymupdf4llm.to_markdown("./data/MERGED_cosmetic_guidances.pdf", page_chunks=True)

with open('./data/cosmetic_guidances.md', 'w', encoding='utf-8') as f:
    for i, page_content in enumerate(data, 1):
        f.write(f'## Page {i}\n\n')
        f.write(page_content['text'])
