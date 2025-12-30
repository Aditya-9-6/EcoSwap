import os
import json
import google.generativeai as genai

def get_eco_alternatives(product_name):
    # Mock Data Fallback
    mock_data = [
        {
            "name": "Bamboo Toothbrush",
            "impact_score": 9,
            "link": "https://www.google.com/search?q=bamboo+toothbrush"
        },
        {
            "name": "Metal Straw",
            "impact_score": 8,
            "link": "https://www.google.com/search?q=metal+straw"
        },
        {
            "name": "Reusable Bottle",
            "impact_score": 10,
            "link": "https://www.google.com/search?q=reusable+water+bottle"
        }
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("NOTICE: No GEMINI_API_KEY found. Using Mock Data.")
        return mock_data
    
    try:
        genai.configure(api_key=api_key)
        
        # Robust Model Selection: Try Flash (New), Fallback to Pro (Stable)
        model_name = 'gemini-1.5-flash'
        try:
            # Check availability (lightweight check) or just fail on first generate
            model = genai.GenerativeModel(model_name)
        except:
            model_name = 'gemini-pro'
            model = genai.GenerativeModel(model_name)

        # --- RAG: Retrieval Step ---
        # 1. Load CSV (Simple linear search for demo, Vector DB better for large scale)
        import csv
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sustainable_products.csv')
        
        rag_context = ""
        found_matches = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Simple keyword matching
                    if product_name.lower() in row['Product'].lower() or product_name.lower() in row['Alternative'].lower():
                        found_matches.append(row)
                        if len(found_matches) >= 3: break # Limit context
            
            if found_matches:
                rag_context = "Knowledge Base Recommendations:\n"
                for match in found_matches:
                    rag_context += f"- Alternative to {match['Product']}: {match['Alternative']} (Score: {match['ImpactScore']})\n"
        except Exception as e:
            print(f"RAG Error: {e}")

        # --- Generation Step ---
        prompt = f"""
        User is looking for sustainable alternatives to: '{product_name}'.
        
        {rag_context}
        
        If the Knowledge Base recommendations above are relevant, INCLUDE them. 
        If not, use your general knowledge to find better ones.
        
        Return exactly 3 alternatives as valid JSON:
        [
            {{
                "name": "Product Name",
                "impact_score": 9,
                "link": "https://www.google.com/search?q=buy+sustainable+product+name"
            }},
            ...
        ]
        Do not add any markdown formatting (like ```json). Ensure strictly valid JSON.
        """
        
        try:
            response = model.generate_content(prompt)
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                print(f"Gemini 1.5 Flash failed ({e}). Retrying with Gemini Pro...")
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
            else:
                raise e # Re-raise if it's not a model not found error
        
        content = response.text
        
        # Cleanup markdown if present
        content = content.replace('```json', '').replace('```', '').strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error fetching alternatives from Gemini: {e}. Returning Mock Data.")
        # DEBUG: Show error in UI
        return [
            {
                "name": f"Error: {str(e)[:50]}...",
                "impact_score": 0,
                "link": "#",
                "description": f"Full error: {str(e)}. Check Render Logs."
            }
        ] + mock_data

def analyze_image(image):
    return "Detected: Plastic Bottle"

def get_chart_data(user):
    from .models import SearchHistory
    from django.db.models import Count
    from django.db.models.functions import TruncDay
    from datetime import timedelta

    # Get search history aggregated by day
    searches_by_day = SearchHistory.objects.filter(user=user) \
        .annotate(day=TruncDay('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')

    labels = []
    data = []
    cumulative_plastic_saved = 0

    if searches_by_day:
        # Create a dictionary to hold data for each day
        search_dict = {item['day'].date(): item['count'] for item in searches_by_day}
        
        start_date = searches_by_day.first()['day'].date()
        end_date = searches_by_day.last()['day'].date()
        
        # Iterate from the first search day to the last
        current_date = start_date
        while current_date <= end_date:
            daily_searches = search_dict.get(current_date, 0)
            daily_plastic_saved = daily_searches * 50 # 50g per search
            cumulative_plastic_saved += daily_plastic_saved
            
            labels.append(current_date.strftime("%b %d"))
            data.append(cumulative_plastic_saved)
            
            current_date += timedelta(days=1)
    
    # If no data, provide a baseline for the chart to render something
    if not labels:
        labels = ["Start", "Today"]
        data = [0, 0]

    return {
        'labels': labels,
        'data': data
    }
