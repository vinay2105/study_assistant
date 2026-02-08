from pypdf import PdfReader
from google import genai

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def generate_notes(text, p1, p2, key):
    client = genai.Client(api_key=key)
    
    prompt_text = (
        "DETAILED NOTES - GENERATE 2000+ WORDS. OUTPUT ONLY COMPLETE HTML DOCUMENT. NO MARKDOWN.\n\n"
        "Create COMPREHENSIVE structured notes (10+ sections, 4-6 bullets each, detailed paragraphs).\n"
        "Use ALL input text. Cover EVERY key point in depth.\n\n"
        "<html><head><style>"
        "body{{font-family:\'Orbitron\',monospace;background:linear-gradient(135deg,#0a0a0a,#1a0033);color:#e0f7ff;padding:80px 2rem 2rem;max-width:1200px;margin:auto;overflow:hidden;}}"
        ".notes-container{{background:rgba(10,15,35,0.97);min-height:100vh;padding:3rem 3rem 2rem;border-radius:0 0 30px 30px;box-shadow:0 30px 100px rgba(0,0,0,0.8),inset 0 1px 0 rgba(0,255,204,0.2);backdrop-filter:blur(25px);overflow-y:auto;max-height:calc(100vh - 80px);}}"
        "h1{{font-size:3.2rem;text-align:center;background:linear-gradient(45deg,#00ffcc,#ff1493,#00ffff);background-clip:text;-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:3.5rem;text-shadow:0 0 50px rgba(0,255,204,0.7);animation:glow 3s infinite alternate;}}"
        "@keyframes glow{{0%{{filter:drop-shadow(0 0 30px #00ffcc);}}100%{{filter:drop-shadow(0 0 60px #ff1493);}}}}"
        "h2{{font-size:2rem;color:#00ffff;margin:3rem 0 1.5rem;padding-bottom:1rem;border-bottom:3px solid transparent;background:linear-gradient(to right,#00ffff,#ff1493);background-clip:text;-webkit-background-clip:text;position:relative;}}"
        "h2::after{{content:\'\';position:absolute;bottom:-4px;left:0;width:80px;height:3px;background:linear-gradient(90deg,#00ffcc,#ff1493);border-radius:2px;animation:expand 1.5s ease-out;}}"
        "@keyframes expand{{from{{width:0;}}}}"
        "ul{{list-style:none;padding-left:1.5rem;max-width:1000px;}}li{{background:rgba(0,255,204,0.12);margin:1.2rem 0;padding:1.5rem 1.8rem;border-left:5px solid #ff1493;border-radius:0 12px 12px 0;transition:all 0.4s cubic-bezier(0.25,0.8,0.25,1);position:relative;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.3);}}"
        "li::before{{content:\'⚡\';color:#00ffcc;font-size:1.3rem;margin-right:1rem;opacity:0.9;font-weight:bold;}}"
        "li:hover{{transform:translateX(12px) scale(1.02);box-shadow:0 15px 40px rgba(255,20,147,0.4);border-left-color:#00ffcc;background:rgba(0,255,204,0.25);}}"
        "p{{line-height:1.75;font-size:1.1rem;margin:1.2rem 0;color:#d0e8ff;text-align:justify;}}"
        "strong{{color:#ff1493;font-weight:700;}}"
        ".conclusion{{text-align:center;font-size:1.4rem;color:#00ffcc !important;padding:3rem 2.5rem;background:linear-gradient(135deg,rgba(255,20,147,0.15),rgba(0,255,204,0.15));border-radius:20px;margin:4rem 1rem 2rem;border:2px solid rgba(0,255,204,0.4);box-shadow:0 20px 50px rgba(0,0,0,0.5);}}"
        ".notes-container::-webkit-scrollbar{{width:8px;}}.notes-container::-webkit-scrollbar-track{{background:rgba(0,0,0,0.4);border-radius:4px;}}.notes-container::-webkit-scrollbar-thumb{{background:linear-gradient(#00ffcc,#ff1493);border-radius:4px;}}"
        "</style></head><body><div class=notes-container>\n"
        "<h1>🚀 COMPREHENSIVE AI NOTES</h1>\n"
    )
    
    # Add detailed content instructions
    detailed_prompt = (
        f"<h2>📋 Main Summary</h2><p><strong>DETAILED ANALYSIS:</strong> {text[:800].replace('\\n',' ').replace('\\r',' ')} "
        f"Continue with full breakdown covering all concepts, examples, formulas.</p>\n"
        f"<h2>🎯 Key Point 1: {p1}</h2><ul><li>Comprehensive explanation with 6+ detailed bullets</li>"
        f"<li>Real-world applications and examples</li><li>Technical details and implementation</li>"
        f"<li>Common pitfalls and solutions</li><li>Advanced considerations</li><li>Best practices</li></ul>\n"
        f"<h2>🎯 Key Point 2: {p2}</h2><ul><li>Same detailed structure - 6+ bullets each</li></ul>\n"
        "<h2>🔬 Technical Deep Dive</h2><ul><li>Break down algorithms step-by-step</li>"
        "<li>Include code examples where relevant</li><li>Complexity analysis O(n)</li>"
        "<li>Optimization techniques</li></ul>\n"
        "<h2>💡 Practical Implementation</h2><ul><li>Step-by-step guide</li>"
        "<li>Tools and libraries needed</li><li>Troubleshooting common errors</li></ul>\n"
        "<h2>📊 Examples & Case Studies</h2><ul><li>3+ real-world examples</li>"
        "<li>Success stories and metrics</li><li>Industry applications</li></ul>\n"
        "<h2 class=conclusion>✅ COMPLETE COVERAGE - All key concepts analyzed in depth. Ready for implementation!</h2>"
        "</div></body></html>"
    )
    
    full_prompt = prompt_text + detailed_prompt
    
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=full_prompt
    )
    
    return response.text







