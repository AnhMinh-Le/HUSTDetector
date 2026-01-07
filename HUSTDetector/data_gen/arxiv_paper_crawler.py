import arxiv
import json
import requests
import re
import pymupdf
from datetime import datetime

def extract_introduction_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        
        pdf_document = pymupdf.open(stream=response.content, filetype="pdf")
        
        full_text = ""
        for page in pdf_document:
            full_text += page.get_text()
        
        pdf_document.close()
        
        intro_patterns = [
            r'\n\s*1\.?\s+Introduction\s*\n',
            r'\n\s*I\.?\s+INTRODUCTION\s*\n',
            r'\n\s*Introduction\s*\n\s*\n',
        ]
        
        intro_start = -1
        for pattern in intro_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                intro_start = match.end()
                break
        
        if intro_start == -1:
            return "Introduction section not found"

        end_patterns = [
            r'\n\s*2\.?\s+[A-Z][a-zA-Z\s]+\n',
            r'\n\s*II\.?\s+[A-Z]+',
            r'\n\s*[A-Z][a-zA-Z\s]+\s*\n\s*\n',
        ]
        
        intro_end = len(full_text)
        text_after_intro = full_text[intro_start:]
        
        for pattern in end_patterns:
            match = re.search(pattern, text_after_intro)
            if match and match.start() > 100:
                intro_end = intro_start + match.start()
                break
        
        introduction = full_text[intro_start:intro_end].strip()

        introduction = re.sub(r'\n+', '\n', introduction)
        introduction = re.sub(r'([a-z,])\n([a-z])', r'\1 \2', introduction)
        
        if len(introduction) > 2500:
            truncated = introduction[:2500]
            last_period = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
            if last_period > 100:
                introduction = introduction[:last_period + 1]
            else:
                last_space = truncated.rfind(' ')
                introduction = introduction[:last_space] if last_space > 100 else introduction[:2500]
        
        if len(introduction) < 50:
            return "Introduction section too short or not found"
        
        return introduction
        
    except Exception as e:
        return f"Error extracting introduction: {str(e)}"

def build_query_with_date_filter(topic, from_date=None, to_date=None):
    query = topic
    
    if from_date or to_date:
        from_str = from_date.strftime('%Y%m%d0000') if from_date else '20070101000'
        to_str = to_date.strftime('%Y%m%d2359') if to_date else datetime.now().strftime('%Y%m%d2359')
        
        query = f"({topic}) AND submittedDate:[{from_str} TO {to_str}]"
    
    return query

def crawl_papers(topic, num_papers=10, from_date=None, to_date=None):
    client = arxiv.Client()
    
    if from_date and isinstance(from_date, str):
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
    if to_date and isinstance(to_date, str):
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
    
    query = build_query_with_date_filter(topic, from_date, to_date)
    
    search = arxiv.Search(
        query=query,
        max_results=num_papers,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    date_info = ""
    if from_date and to_date:
        date_info = f" published from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}"
    elif from_date:
        date_info = f" published from {from_date.strftime('%Y-%m-%d')}"
    elif to_date:
        date_info = f" published until {to_date.strftime('%Y-%m-%d')}"
    
    print(f"Searching for {num_papers} papers on topic: '{topic}'{date_info}...")
    print(f"Query: {query}\n")
    
    papers_data = []
    count = 0
    
    for result in client.results(search):
        count += 1
        
        print(f"[{count}/{num_papers}] Processing: {result.title[:70]}...")
        print(f"   Published: {result.published.strftime('%Y-%m-%d')}")
        
        introduction = extract_introduction_from_pdf(result.pdf_url)
        
        paper_info = {
            "title": result.title,
            "abstract": result.summary,
            "introduction": introduction,
            "published": result.published.strftime('%Y-%m-%d')
        }
        
        papers_data.append(paper_info)
        print(f"   ✓ Successfully crawled\n")
        
        if count >= num_papers:
            break
    
    if count < num_papers:
        print(f"Warning: Only found {count} papers matching criteria.")
        print(f"Try expanding your date range or using a broader topic.\n")
    
    filename = f"{topic.replace(' ', '_').replace('/', '_')}.json"
    
    output_data = {
        "topic": topic,
        "num_papers": num_papers,
        "papers": papers_data
    }
    
    if from_date or to_date:
        output_data["date_filter"] = {}
        if from_date:
            output_data["date_filter"]["from_date"] = from_date.strftime('%Y-%m-%d')
        if to_date:
            output_data["date_filter"]["to_date"] = to_date.strftime('%Y-%m-%d')
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*80}")
    print(f"Successfully saved {len(papers_data)} papers to '{filename}'")
    print(f"{'='*80}")
    
    return filename

def main():
    print("=" * 80)
    print("ArXiv Paper Crawler")
    print("=" * 80)
    print()
    
    topic = input("Enter the topic: ")
    num_papers = int(input("Enter the number of papers: "))
    
    use_date_filter = input("Filter by date? (y/n, default=n): ").strip().lower()
    from_date = None
    to_date = None
    
    if use_date_filter == 'y':
        from_input = input("From date (YYYY-MM-DD, press Enter to skip): ").strip()
        to_input = input("To date (YYYY-MM-DD, press Enter to skip): ").strip()
        
        if from_input:
            from_date = datetime.strptime(from_input, '%Y-%m-%d')
        if to_input:
            to_date = datetime.strptime(to_input, '%Y-%m-%d')
    
    print()
    
    filename = crawl_papers(topic, num_papers, from_date=from_date, to_date=to_date)

if __name__ == "__main__":
    main()