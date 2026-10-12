import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('saarthi_all_pages.json', 'r', encoding='utf-8') as f:
    raw_pages = json.load(f)

def clean_str(s):
    if not s:
        return ""
    s = re.sub(r'[ \t]+', ' ', s)
    s = s.replace('ﬀ', 'ff').replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬃ', 'ffi')
    return s.strip()

KNOWN_HEADINGS = {
    # Ch 1
    "Political Ideologies", "Marxist Perspective on Ideology", "Core Marxist Concepts", 
    "Expanded Marxist Views", "Conservative Critique of Ideology: Michael Oakeshott",
    "Ideology and Totalitarianism: Arendt and Popper’s Perspectives",
    "Hannah Arendt: Ideology as the Engine of Totalitarianism",
    "Karl Popper: Defending the Open Society", "Synthesis and Contemporary Relevance",
    "The End of Ideology Debate: Origins and Core Thesis", "Daniel Bell and the “End of Ideology” Thesis",
    "Critics and Counterarguments", "Resurgence of Ideology in the 21st Century",
    
    # Ch 2
    "Liberalism", "Origin and Evolution of Liberalism", "Core Values of Liberalism",
    "Classical Liberalism", "Modern Liberalism", "Neo-Liberalism", 
    "Isaiah Berlin: Value Pluralism and Its Multicultural Implications",
    "Isaiah Berlin: Two Concepts of Liberty", "Classical Liberal Perspectives on the State",
    "Neo-Liberal Perspectives on the State", "Critiques of Neo-Liberalism",
    
    # Ch 3
    "Marxism", "Definition", "Core Tenets of Marxism", "Dialectical and Historical Materialism",
    "Labor Theory of Value and Surplus Value", "Marx’s Theory of Alienation", "Class Struggle and Revolution",
    "Marxist Theories of the State", "Instrumentalist View of the State", "Structuralist View of the State",
    "The Miliband-Poulantzas Debate", "Marxist Internationalism", "Variants and Adaptations",
    "Leninism", "Development of Marxism Post-Marx: Leninism", "Maoism", "Development of Marxism Post-Marx: Maoism",
    "Gramsci’s Contribution to Marxism", "Antonio Gramsci: Cultural Hegemony",
    "Frankfurt School and Critical Theory", "Frankfurt School and the Critical Turn in Neo-Marxism",
    "Neo-Marxism: Expanding Classical Marxism", "Continued Relevance of Neo-Marxism",
    "Global and Postcolonial Perspectives", "Incorporation of Other Critical Theories",
    "Herbert Marcuse - \"One-Dimensional Man\"", "Jürgen Habermas - \"The Theory of Communicative Action\"",
    "Structuralist School within Neo-Marxism", "Contemporary Relevance of Marxism", "Various Streams of Marxism",
    
    # Ch 4
    "Socialism and Fascism", "Origin and Evolution of Socialism", "Utopian Socialism", 
    "Evolutionary Socialism", "Revolutionary Socialism", "Fabian Socialism", "Revisionism", 
    "Syndicalism", "Guild Socialism", "Equality under Socialism", "Democratic Socialism", 
    "Socialism in the 21st Century", "Fascism", "What is fascism?", "Evolution of Fascism", 
    "Characteristics of Fascism", "Authority under Fascism", "Fascism on Collectivism", 
    "Fascism as Totalitarianism", "Nazism under Adolf Hitler", "Italian Fascism under Benito Mussolini", 
    "Fascism Today: Contemporary Manifestations of Far-Right Extremism",
    
    # Ch 5
    "Gandhism", "Introduction", "Mahatma Gandhi (1869–1948): Life and Influences", 
    "Gandhi’s Concept of Truth (Satya)", "Gandhi’s Philosophy of Non-Violence (Ahimsa)", 
    "Gandhi’s Views on Socialism", "Gandhian Concept of Sarvodaya: “Welfare of All”", 
    "Gandhian Trusteeship Theory: Wealth with Responsibility", 
    "Gandhi’s Views on the State: Decentralized, Ethical, and Nonviolent", 
    "Gandhian Concept of Ramrajya: The Ideal State", "Gandhi on Caste and Untouchability: A Moral Revolution", 
    "Gandhi’s Views on Democracy: A Moral, Decentralized, Inclusive Ideal", 
    "Gandhi on Fascism", "Gandhi on Decentralization", "Gandhi on Power", 
    "Gandhi on Rights and Duties", "Gandhian Theory of Satyagraha", 
    "Gandhi on Western Civilization (Hind Swaraj)", "Gandhian Concept of Swaraj", 
    "Gandhi on Means and Ends in Politics", "Gandhi on Modernism", 
    "Relevance of Gandhi in the Contemporary World",
    
    # Ch 6
    "Feminism", "Evolution of Feminism", "Meaning of Feminism", 
    "Liberal Feminism: Overview", "Key Tenets of Liberal Feminism", "Critiques of Liberal Feminism", 
    "Radical Feminism: Overview", "Key Tenets of Radical Feminism", "Critiques of Radical Feminism", 
    "Socialist Feminism: Integrating Gender and Class", "Critiques of Socialist Feminism", 
    "Marxist Feminism: Feminism through a Class Lens", 
    "Postcolonial Feminism: Reclaiming Voice, History, and Identity", 
    "Other Streams of Feminism: Diverse Voices, Shared Struggles", "Relevance of Feminism Today"
}

def is_heading_line(line):
    line_clean = line.strip().rstrip(':')
    if line_clean in KNOWN_HEADINGS:
        return True
    for kh in KNOWN_HEADINGS:
        if line_clean.lower() == kh.lower() or line_clean.lower().startswith(kh.lower() + ":"):
            return True
    if line.endswith(':') and len(line) < 60 and '.' not in line[:-1] and not line.startswith('●') and not line.startswith('○'):
        return True
    return False

def get_page_lines(pnum):
    if pnum < 1 or pnum > len(raw_pages):
        return []
    p = raw_pages[pnum - 1]
    raw_lines = p['text'].splitlines()
    clean_lines = []
    for l in raw_lines:
        s = clean_str(l)
        if not s:
            continue
        if s in ["PSIR", "(Political Ideologies)"] or s == "PSIR | (Political Ideologies)":
            continue
        if s.startswith("© Sarrthi IAS") or s == "9569093856" or s.startswith("Telegram:-"):
            continue
        if s.isdigit() and len(s) <= 3:
            continue
        if "All material appearing on the" in s or "protected by" in s or "exploit any such content" in s:
            continue
        clean_lines.append(s)
    return clean_lines

def parse_page_clean(pnum):
    lines = get_page_lines(pnum)
    items = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('●'):
            b_text = line[1:].strip()
            idx += 1
            while idx < len(lines):
                nxt = lines[idx]
                if nxt.startswith('●') or nxt.startswith('○') or is_heading_line(nxt):
                    break
                b_text += ' ' + nxt
                idx += 1
            items.append({'type': 'bullet', 'text': clean_str(b_text), 'page': pnum})
        elif line.startswith('○'):
            sb_text = line[1:].strip()
            idx += 1
            while idx < len(lines):
                nxt = lines[idx]
                if nxt.startswith('●') or nxt.startswith('○') or is_heading_line(nxt):
                    break
                sb_text += ' ' + nxt
                idx += 1
            items.append({'type': 'subbullet', 'text': clean_str(sb_text), 'page': pnum})
        elif is_heading_line(line):
            items.append({'type': 'heading', 'text': clean_str(line), 'page': pnum})
            idx += 1
        else:
            p_text = line
            idx += 1
            while idx < len(lines):
                nxt = lines[idx]
                if nxt.startswith('●') or nxt.startswith('○') or is_heading_line(nxt):
                    break
                p_text += ' ' + nxt
                idx += 1
            items.append({'type': 'paragraph', 'text': clean_str(p_text), 'page': pnum})
    return items

def split_bullet_label(b_text):
    colon_idx = b_text.find(':')
    if colon_idx != -1 and colon_idx < 60:
        label = b_text[:colon_idx].strip()
        desc = b_text[colon_idx+1:].strip()
        return label, desc
    
    dash_match = re.search(r'^([A-Za-z0-9\s,\'’&]+)\s+[-–—]\s+(.+)$', b_text)
    if dash_match and len(dash_match.group(1)) < 50:
        return dash_match.group(1).strip(), dash_match.group(2).strip()

    return "", b_text

CHAPTERS = [
    {
        "id": "ch1_ideologies",
        "num": 1,
        "title": "Chapter 1: Political Ideologies",
        "short_title": "1. Political Ideologies",
        "subtitle": "Origins, Functions & Perspectives (Marxist, Oakeshott, Arendt, Popper, End of Ideology)",
        "start_page": 3,
        "end_page": 8,
        "pdf_pages": "pp. 3–8"
    },
    {
        "id": "ch2_liberalism",
        "num": 2,
        "title": "Chapter 2: Liberalism & Theories of the State",
        "short_title": "2. Liberalism & State",
        "subtitle": "Classical Liberalism (Night-Watchman), Welfare Liberalism & Neo-Liberalism (Roll-Back)",
        "start_page": 9,
        "end_page": 18,
        "pdf_pages": "pp. 9–18"
    },
    {
        "id": "ch3_marxism",
        "num": 3,
        "title": "Chapter 3: Marxism, Neo-Marxism & State Theories",
        "short_title": "3. Marxism & State",
        "subtitle": "Dialectical Materialism, Alienation, Instrumentalist vs Structuralist State, Lenin, Mao, Gramsci & Frankfurt",
        "start_page": 19,
        "end_page": 40,
        "pdf_pages": "pp. 19–40"
    },
    {
        "id": "ch4_socialism_fascism",
        "num": 4,
        "title": "Chapter 4: Socialism and Fascism",
        "short_title": "4. Socialism & Fascism",
        "subtitle": "Utopian & Scientific Socialism, Fabianism, Guild Socialism & Totalitarian Fascism",
        "start_page": 40,
        "end_page": 55,
        "pdf_pages": "pp. 40–55"
    },
    {
        "id": "ch5_gandhism",
        "num": 5,
        "title": "Chapter 5: Gandhism",
        "short_title": "5. Gandhism",
        "subtitle": "Satya, Ahimsa, Satyagraha, Swaraj, Sarvodaya, Trusteeship & Oceanic Circles (Stateless Village Swaraj)",
        "start_page": 56,
        "end_page": 69,
        "pdf_pages": "pp. 56–69"
    },
    {
        "id": "ch6_feminism",
        "num": 6,
        "title": "Chapter 6: Feminism",
        "short_title": "6. Feminism",
        "subtitle": "Waves of Feminism, Liberal, Radical, Marxist/Socialist, Intersectional & Contemporary Perspectives",
        "start_page": 69,
        "end_page": 76,
        "pdf_pages": "pp. 69–76"
    }
]

# Track bullet id counters
bullet_counters = {}

def get_bullet_id(ch_id, label, text, pnum):
    # Special check for Core Marxist Concepts (user screenshot from Page 3)
    if ch_id == "ch1_ideologies" and pnum == 3:
        if "Class Domination" in label:
            return "marx_1"
        if "False Consciousness" in label:
            return "marx_2"
        if "Class Consciousness" in label:
            return "marx_3"
        if "End of Ideology" in label:
            return "marx_4"
    
    if ch_id not in bullet_counters:
        bullet_counters[ch_id] = 1
    else:
        bullet_counters[ch_id] += 1
    return f"{ch_id}_b{bullet_counters[ch_id]}"

full_dataset = {
    "metadata": {
        "title": "PSIR Class Notes Master Suite",
        "faculty": "Vivek Waghmare",
        "telegram": "PSIR Study Suite",
        "totalChapters": 6,
        "totalPages": 77
    },
    "chapters": []
}

total_bullets_generated = 0

for ch_info in CHAPTERS:
    ch_id = ch_info['id']
    start_p = ch_info['start_page']
    end_p = ch_info['end_page']
    
    # Process all pages in this chapter
    sections = []
    current_sec = {
        "id": f"{ch_id}_sec_intro",
        "title": ch_info['title'].split(': ')[-1],
        "start_page": start_p,
        "paragraphs": [],
        "bullets": [],
        "subbullets": []
    }
    
    sec_counter = 1
    
    for pnum in range(start_p, end_p + 1):
        page_items = parse_page_clean(pnum)
        for it in page_items:
            itype = it['type']
            itext = it['text']
            
            if itype == 'heading':
                # Check if current section has content; if so save and start new section
                if current_sec['paragraphs'] or current_sec['bullets'] or current_sec['subbullets']:
                    sections.append(current_sec)
                    sec_counter += 1
                    current_sec = {
                        "id": f"{ch_id}_sec_{sec_counter}",
                        "title": itext.rstrip(':'),
                        "start_page": pnum,
                        "paragraphs": [],
                        "bullets": [],
                        "subbullets": []
                    }
                else:
                    current_sec['title'] = itext.rstrip(':')
                    current_sec['start_page'] = pnum
            elif itype == 'paragraph':
                current_sec['paragraphs'].append({
                    "page": pnum,
                    "text": itext
                })
            elif itype == 'bullet':
                lbl, desc = split_bullet_label(itext)
                b_id = get_bullet_id(ch_id, lbl, desc, pnum)
                current_sec['bullets'].append({
                    "id": b_id,
                    "page": pnum,
                    "label": lbl,
                    "text": desc,
                    "full_text": itext
                })
                total_bullets_generated += 1
            elif itype == 'subbullet':
                lbl, desc = split_bullet_label(itext)
                current_sec['subbullets'].append({
                    "page": pnum,
                    "label": lbl,
                    "text": desc,
                    "full_text": itext
                })
    
    if current_sec['paragraphs'] or current_sec['bullets'] or current_sec['subbullets']:
        sections.append(current_sec)
        
    ch_obj = {
        "id": ch_id,
        "num": ch_info['num'],
        "title": ch_info['title'],
        "short_title": ch_info['short_title'],
        "subtitle": ch_info['subtitle'],
        "page_range": ch_info['pdf_pages'],
        "start_page": start_p,
        "end_page": end_p,
        "sections": sections,
        "total_bullets": sum(len(s['bullets']) for s in sections)
    }
    full_dataset['chapters'].append(ch_obj)

print(f"Generated {len(full_dataset['chapters'])} chapters.")
print(f"Total bullets generated: {total_bullets_generated}")
for c in full_dataset['chapters']:
    print(f" -> {c['title']}: {len(c['sections'])} sections, {c['total_bullets']} bullets")

# Write to sarrthi_full_data.js
js_content = f"/* Auto-generated Sarrthi IAS PSIR Class Notes Complete Study Suite */\nwindow.SARRTHI_DATA = {json.dumps(full_dataset, indent=2, ensure_ascii=False)};\n"

with open('sarrthi_full_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ sarrthi_full_data.js successfully written! Size: {len(js_content)} bytes")
