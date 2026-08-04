skills = ["Python", "FastAPI", "Python", "RAG", "Git", "  SQL  "]
cleaned = []
seen = set()
counts = {}
for raw_skill in skills:
    clean_skill = raw_skill.strip()
    if clean_skill not in seen:
        seen.add(clean_skill)
        cleaned.append(clean_skill)
        counts[clean_skill] = 0
    counts[clean_skill] += 1

top_skill = ''
top_count = 0
for skill in cleaned:
    if counts[skill] > top_count:
        top_skill = skill
        top_count = counts[skill]

print("cleaned:", cleaned)
print("counts:", counts)
print("top:", top_skill)
