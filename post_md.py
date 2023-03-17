import datetime
import re

date = datetime.datetime.now().strftime('%Y-%m-%d')
title = input("Title: ").strip()
categ = input("Category: ").strip()
tags = input("Tags (Space seperated): ").strip().split(' ')
tags_format = ''.join([" - "+s+"\n" for s in tags])

header = f"""--- 
layout: post
title:  "{title}"
date: {date}
tags:
{tags_format}
categories: {categ}
---
"""
print(header)

path = input('.md path: ').strip()
with open(path, 'r') as f:
    s = f.read()

s = header + s

name = input(f'Give a short name; Ex. "cute cats" will be saved as {date}-cute-cats.md\nName: ').strip()
with open(f"_posts/{date}-{re.sub(' ','-',name)}.md", 'w') as f:
    f.write(s)

