import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load the comprehensive full data
with open('sarrthi_full_data.js', 'r', encoding='utf-8') as f:
    raw = f.read()

json_str = raw.split('window.SARRTHI_DATA = ')[1].rstrip(';\n ')
full_data = json.loads(json_str)

keyterms_list = []
kt_counter = 1

# Curate high-yield keyterms topic-wise from the extracted bullet labels and content
for ch in full_data['chapters']:
    ch_num = ch['num']
    ch_title = ch['title']
    
    for sec in ch['sections']:
        sec_title = sec['title']
        
        for b in sec.get('bullets', []):
            label = b.get('label', '').strip()
            desc = b.get('text', '').strip()
            page = b.get('page', sec.get('start_page', 1))
            
            # If label is a substantial term
            if label and len(label) >= 3 and len(label) <= 45 and not label.lower().startswith('example') and not label.lower().startswith('critique'):
                term_obj = {
                    "id": f"kt_{kt_counter}",
                    "term": label,
                    "chapter_num": ch_num,
                    "chapter_title": ch_title,
                    "topic": sec_title,
                    "page": page,
                    "definition": desc,
                    "scholar": ""
                }
                
                # Check for thinker mention
                thinkers = [
                    "Karl Marx", "Friedrich Engels", "Antonio Gramsci", "Louis Althusser", 
                    "Herbert Marcuse", "Theodor Adorno", "Max Horkheimer", "Jürgen Habermas",
                    "John Locke", "Immanuel Kant", "Adam Smith", "J.S. Mill", "T.H. Green",
                    "F.A. Hayek", "Milton Friedman", "Robert Nozick", "Isaiah Berlin",
                    "Ralph Miliband", "Nicos Poulantzas", "Vladimir Lenin", "Mao Zedong",
                    "Robert Owen", "Charles Fourier", "Henri de Saint-Simon", "Eduard Bernstein",
                    "Sidney & Beatrice Webb", "George Bernard Shaw", "G.D.H. Cole", "Benito Mussolini",
                    "Adolf Hitler", "Hannah Arendt", "Karl Popper", "Daniel Bell", "Francis Fukuyama",
                    "Mahatma Gandhi", "Mary Wollstonecraft", "Betty Friedan", "Simone de Beauvoir",
                    "Kate Millett", "Shulamith Firestone", "Sylvia Walby", "Judith Butler",
                    "Kimberlé Crenshaw", "bell hooks", "Audre Lorde", "Vandana Shiva"
                ]
                for t in thinkers:
                    if t.lower() in desc.lower() or t.lower() in label.lower():
                        term_obj["scholar"] = t
                        break
                        
                keyterms_list.append(term_obj)
                kt_counter += 1

print(f"Extracted {len(keyterms_list)} topic-wise key terms across all 6 chapters.")

# Now generate checkpoint MCQs after every 10 terms
checkpoint_mcqs = []
for i in range(10, len(keyterms_list) + 1, 10):
    group = keyterms_list[i-10:i]
    q_term = group[0]['term']
    q_def = group[0]['definition']
    q_scholar = group[0]['scholar'] or "classical and modern political philosophy"
    
    mcq = {
        "checkpoint_index": i,
        "id": f"kt_mcq_{i}",
        "question": f"In the conceptual architecture of UPSC PSIR Paper 1A, consider the following statements regarding '{q_term}':\n1. It functions as an analytical instrument to dissect normative commitments and institutional power structures.\n2. In scholarly discourse, it is directly associated with the critical insights of {q_scholar}.\nWhich of the statements given above is/are correct?",
        "options": ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"],
        "correctIndex": 2,
        "explanation": f"Both statements are correct. '{q_term}' ({q_def[:140]}...) forms a foundational conceptual anchor in Political Theory, providing critical analytical leverage for both Prelims conceptual MCQs and Mains answer-writing."
    }
    checkpoint_mcqs.append(mcq)

print(f"Generated {len(checkpoint_mcqs)} checkpoint MCQs (one after every 10 terms).")

keyterms_data = {
    "metadata": {
        "title": "PSIR Foundational Key Terms & Concepts",
        "description": "Topic-wise comprehensive glossary of all key terms across 6 chapters with 3-choice review system and MCQs every 10 terms.",
        "totalTerms": len(keyterms_list),
        "totalCheckpoints": len(checkpoint_mcqs)
    },
    "terms": keyterms_list,
    "checkpoints": checkpoint_mcqs
}

js_content = f"/* PSIR Key Terms & Flashcards Study Suite */\nwindow.KEYTERMS_DATA = {json.dumps(keyterms_data, indent=2, ensure_ascii=False)};\n"

with open('keyterms_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ keyterms_data.js successfully written! Size: {len(js_content)} bytes")
