#!/usr/bin/env python3
"""
🔍 SHOPIFY RECON — One Command to Clone Any Shopify Store
Paste a link → Get a complete Shopify Liquid theme

Usage: python3 shopify-recon.py <url> [output-dir]
       python3 shopify-recon.py https://rothys.com ./my-clone

What it does:
  1. Extract all data (products, collections, theme metadata, HTML)
  2. Crawl all page types (homepage, product, collection, search, cart, 404)
  3. Run Theme DNA fingerprint
  4. Generate complete Shopify Liquid theme (18 files)
  5. Generate standalone HTML website clone
  6. Run SEO + Performance analysis
  7. Display beautiful TUI dashboard
"""

import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))


def run_tool(script, args, label):
    """Run a tool script and return success status"""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    
    cmd = ["python3", os.path.join(TOOL_DIR, script)] + args
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def run_bash(script, args, label):
    """Run a bash script"""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    
    cmd = [os.path.join(TOOL_DIR, script)] + args
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║  🔍 SHOPIFY RECON — One Command Store Cloner                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                                ║
║  Paste a link → Get a complete Shopify Liquid theme            ║
║                                                                ║
║  Usage:                                                        ║
║    python3 shopify-recon.py <url> [output-dir]                 ║
║                                                                ║
║  Example:                                                      ║
║    python3 shopify-recon.py https://rothys.com                 ║
║    python3 shopify-recon.py https://allbirds.com ./allbirds    ║
║                                                                ║
║  What it does:                                                 ║
║    1. Extract products, collections, theme metadata            ║
║    2. Crawl all page types (product, collection, search, cart) ║
║    3. Theme DNA fingerprint (detect theme framework)           ║
║    4. Generate complete Liquid theme (18 files)                ║
║    5. Generate HTML website clone                              ║
║    6. SEO + Performance analysis                               ║
║    7. Beautiful TUI dashboard                                  ║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
""")
        sys.exit(0)
    
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
    
    store_name = url.replace("https://", "").replace("http://", "").split("/")[0]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else f"./{store_name.replace('.', '-')}-clone"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  🔍 SHOPIFY RECON — Starting Full Clone                        ║
╠═══════════════════════════════════════════════════════════════╣
║  🏪 Store:  {store_name:<50}║
║  📁 Output: {output_dir:<50}║
║  🕐 Time:   {datetime.now().strftime('%Y-%m-%d %H:%M'):<50}║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    start_time = datetime.now()
    steps_completed = 0
    total_steps = 27
    
    # Step 1: Extract data (Liquid Inspector)
    print(f"\n📌 Step 1/{total_steps}: Extracting store data...")
    extract_dir = os.path.join(output_dir, "extracted")
    if run_bash("shopify-liquid-inspector.sh", [url, extract_dir], "📡 Liquid Inspector"):
        steps_completed += 1
    
    # Step 2: Crawl all page types
    print(f"\n📌 Step 2/{total_steps}: Crawling all page types...")
    pages_dir = os.path.join(output_dir, "pages")
    products_json = os.path.join(extract_dir, "api", "products.json")
    collections_json = os.path.join(extract_dir, "api", "collections.json")
    
    page_args = [url, output_dir]
    if os.path.exists(products_json):
        page_args.append(f"--products={products_json}")
    if os.path.exists(collections_json):
        page_args.append(f"--collections={collections_json}")
    
    if run_tool("page-extractor.py", page_args, "🌐 Page Extractor"):
        steps_completed += 1
    
    # Step 3: Theme DNA
    print(f"\n📌 Step 3/{total_steps}: Fingerprinting theme DNA...")
    if run_tool("theme-dna.py", [extract_dir, "--output", os.path.join(output_dir, "analysis")], "🧬 Theme DNA"):
        steps_completed += 1
    
    # Step 4: Generate complete Liquid theme
    print(f"\n📌 Step 4/{total_steps}: Generating Shopify Liquid theme...")
    page_analysis = os.path.join(output_dir, "page-analysis.json")
    theme_dir = os.path.join(output_dir, "theme")
    
    if os.path.exists(page_analysis):
        if run_tool("template-generator.py", [page_analysis, theme_dir], "🏗️ Template Generator"):
            steps_completed += 1
    else:
        # Fallback to basic theme converter
        if run_bash("shopify-theme-converter.sh", [extract_dir, theme_dir], "🏗️ Theme Converter (basic)"):
            steps_completed += 1
    
    # Step 5: Generate HTML website
    print(f"\n📌 Step 5/{total_steps}: Generating HTML website clone...")
    web_dir = os.path.join(output_dir, "website")
    if run_bash("web-clone-generator.sh", [extract_dir, web_dir], "🌐 Web Clone Generator"):
        steps_completed += 1
    
    # Step 6: SEO Analysis
    print(f"\n📌 Step 6/{total_steps}: Running SEO X-Ray...")
    if run_tool("seo-xray.py", [extract_dir, "-o", os.path.join(output_dir, "analysis")], "🔍 SEO X-Ray"):
        steps_completed += 1
    
    # Step 7: Performance Analysis
    print(f"\n📌 Step 7/{total_steps}: Running Performance Profiler...")
    if run_tool("perf-profiler.py", [extract_dir, "-o", os.path.join(output_dir, "analysis")], "⚡ Performance Profiler"):
        steps_completed += 1
    
    # Step 8: Section Reverse-Engineer (bonus)
    print(f"\n📌 Step 8/{total_steps}: Reconstructing sections...")
    sections_dir = os.path.join(output_dir, "analysis", "sections")
    if run_tool("section-reverse-engineer.py", [extract_dir, sections_dir], "🧠 Section Reverse-Engineer"):
        steps_completed += 1
    
    # Step 9: Animation/Hover Cloner
    print(f"\n📌 Step 9/{total_steps}: Extracting animations & hover effects...")
    anim_dir = os.path.join(output_dir, "analysis", "animations")
    if run_tool("animation-cloner.py", [extract_dir, anim_dir], "🎬 Animation Cloner"):
        steps_completed += 1
    
    # Step 10: CSS Injector
    print(f"\n📌 Step 10/{total_steps}: Injecting CSS into theme...")
    styles_dir = os.path.join(output_dir, "analysis", "styles")
    if os.path.exists(theme_dir) and os.path.exists(styles_dir):
        if run_tool("css-injector.py", [theme_dir, styles_dir, theme_dir + "-styled"], "💉 CSS Injector"):
            steps_completed += 1
            # Update theme_dir to styled version
            theme_dir = theme_dir + "-styled"
    else:
        print("  ⏭️  Skipping CSS injection (missing theme or styles)")
    
    # Step 11: Component Specs (from ai-website-cloner methodology)
    print(f"\n📌 Step 11/{total_steps}: Generating component specifications...")
    specs_dir = os.path.join(output_dir, "analysis", "component-specs")
    if run_tool("component-spec.py", [extract_dir, specs_dir], "📋 Component Spec Generator"):
        steps_completed += 1
    
    # Step 12: Deep Code Extraction (BeautifulSoup + webcrack + asset mirror)
    print(f"\n📌 Step 12/{total_steps}: Deep code extraction (deobfuscate + mirror assets)...")
    deep_dir = os.path.join(output_dir, "analysis", "deep-extract")
    if run_tool("deep-extractor-v2.py", [url, deep_dir], "🔬 Deep Code Extractor v2"):
        steps_completed += 1
    
    # Step 13: CSS Exact Values
    print(f"\n📌 Step 13/{total_steps}: Extracting exact CSS values...")
    css_exact_dir = os.path.join(output_dir, "analysis", "css-exact")
    if run_tool("css-exact-values.py", [extract_dir, css_exact_dir], "🎨 CSS Exact Values"):
        steps_completed += 1
    
    # Step 14: Form Cloner
    print(f"\n📌 Step 14/{total_steps}: Cloning forms...")
    forms_dir = os.path.join(output_dir, "analysis", "forms")
    if run_tool("form-cloner.py", [extract_dir, forms_dir], "📝 Form Cloner"):
        steps_completed += 1
    
    # Step 15: Schema Generator
    print(f"\n📌 Step 15/{total_steps}: Generating section schemas...")
    schemas_dir = os.path.join(output_dir, "analysis", "schemas")
    if run_tool("schema-generator.py", [extract_dir, schemas_dir], "⚙️ Schema Generator"):
        steps_completed += 1
    
    # Step 16: Responsive Cloner
    print(f"\n📌 Step 16/{total_steps}: Cloning responsive breakpoints...")
    resp_dir = os.path.join(output_dir, "analysis", "responsive")
    if run_tool("responsive-cloner.py", [extract_dir, resp_dir], "📱 Responsive Cloner"):
        steps_completed += 1
    
    # Step 17: DOM-to-Liquid Converter
    print(f"\n📌 Step 17/{total_steps}: Converting HTML to Liquid templates...")
    if run_tool("dom-to-liquid.py", [url, output_dir], "🔄 DOM-to-Liquid Converter"):
        steps_completed += 1
    
    # Step 18: Settings Data Generator
    print(f"\n📌 Step 18/{total_steps}: Generating settings_data.json + settings_schema.json...")
    if run_tool("settings-data-generator.py", [output_dir], "⚙️ Settings Generator"):
        steps_completed += 1
    
    # Step 19: Section-Group Builder
    print(f"\n📌 Step 19/{total_steps}: Building section-groups + layout/theme.liquid...")
    if run_tool("section-group-builder.py", [output_dir], "🏗️ Section-Group Builder"):
        steps_completed += 1
    
    # Step 20: Variant Selector + Filter Cloner
    print(f"\n📌 Step 20/{total_steps}: Cloning variant selector + collection filters...")
    if run_tool("variant-filter-cloner.py", [output_dir], "🎨 Variant + Filter Cloner"):
        steps_completed += 1
    
    # Step 21: Cart AJAX + Pagination Cloner
    print(f"\n📌 Step 21/{total_steps}: Cloning cart AJAX + pagination/infinite scroll...")
    if run_tool("cart-pagination-cloner.py", [output_dir], "🛒 Cart + Pagination Cloner"):
        steps_completed += 1
    
    # Step 22: CSS Style Cloner (extract design system)
    print(f"\n📌 Step 22/{total_steps}: Extracting CSS design system...")
    css_dir = os.path.join(output_dir, "analysis", "css")
    if run_tool("css-style-cloner.py", [url, css_dir], "🎨 CSS Style Cloner"):
        steps_completed += 1
    
    # Step 23: JS Logic Extractor
    print(f"\n📌 Step 23/{total_steps}: Extracting JavaScript logic...")
    js_dir = os.path.join(output_dir, "analysis", "js")
    if run_tool("js-logic-extractor.py", [url, js_dir], "⚡ JS Logic Extractor"):
        steps_completed += 1
    
    # Step 24: Section Detector (DATA-DRIVEN — discover REAL sections on each
    # page from shopify-section markers / structural patterns. Output drives
    # json-template-builder so the clone is 1:1 with the source — no invented
    # sections the page didn't have.)
    print(f"\n📌 Step 24/{total_steps}: Detecting real sections (1:1, no hallucination)...")
    if run_tool("section-detector.py", ["--clone", output_dir], "🔎 Section Detector"):
        steps_completed += 1

    # Step 25: JSON Template Builder (editor-native pages — consumes detected
    # sections; MUST run before block-ifier)
    print(f"\n📌 Step 25/{total_steps}: Building JSON templates (reorderable pages, data-driven)...")
    json_theme_path = os.path.join(output_dir, "theme")
    if run_tool("json-template-builder.py", [json_theme_path], "🧩 JSON Template Builder"):
        steps_completed += 1

    # Step 26: Block-ifier (make every section editor-customizable — runs AFTER
    # json-template-builder so detected + extracted sections get block-ified too)
    print(f"\n📌 Step 26/{total_steps}: Block-ifying sections (blocks + presets + shopify_attributes)...")
    sections_path = os.path.join(output_dir, "theme", "sections")
    if run_tool("block-ifier.py", ["--dir", sections_path], "🧱 Block-ifier"):
        steps_completed += 1

    # Step 27: Theme Validator (now reports Editor-Readiness Score)
    print(f"\n📌 Step 27/{total_steps}: Validating theme structure + editor-readiness...")
    theme_path = os.path.join(output_dir, "theme")
    if run_tool("theme-validator.py", [theme_path], "✅ Theme Validator"):
        steps_completed += 1
    
    # Calculate time
    elapsed = datetime.now() - start_time
    minutes = int(elapsed.total_seconds() // 60)
    seconds = int(elapsed.total_seconds() % 60)
    
    # Final summary
    print(f"""

╔═══════════════════════════════════════════════════════════════╗
║  ✅ CLONE COMPLETE — {store_name:<42}║
╠═══════════════════════════════════════════════════════════════╣
║                                                                ║
║  📊 Steps completed: {steps_completed}/{total_steps}{'':<{26}}║
║  ⏱️  Time elapsed: {minutes}m {seconds}s{'':<{30}}║
║                                                                ║
║  📁 Output directory: {output_dir:<40}║
║                                                                ║
║  📂 What you got:                                              ║
║     • extracted/     — Raw data (products, collections, HTML)  ║
║     • pages/         — All page HTML (product, cart, search)   ║
║     • theme/         — Complete Shopify Liquid theme (24+ files)║
║     • website/       — Standalone HTML website clone           ║
║     • analysis/      — Theme DNA, SEO, Performance reports     ║
║                                                                ║
║  🚀 Next steps:                                                ║
║     1. Preview website:                                        ║
║        cd {output_dir}/website && python3 -m http.server 8000{'':<{8}}║
║                                                                ║
║     2. Deploy theme to Shopify:                                ║
║        shopify theme dev --store=YOUR_STORE.myshopify.com --path={output_dir}/theme{'':<{0}}║
║                                                                ║
║     3. Push theme to store:                                    ║
║        shopify theme push --store=YOUR_STORE.myshopify.com --path={output_dir}/theme{'':<{0}}║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    # Count total files generated
    total_files = 0
    for root, dirs, files in os.walk(output_dir):
        total_files += len(files)
    
    print(f"  📄 Total files generated: {total_files}")
    print(f"  💾 Total size: ", end="")
    
    total_size = 0
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))
    
    if total_size > 1024 * 1024:
        print(f"{total_size / (1024*1024):.1f} MB")
    else:
        print(f"{total_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
