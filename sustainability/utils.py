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
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Find 3 sustainable alternatives to '{product_name}'.
        Return ONLY valid JSON in this format:
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
        
        response = model.generate_content(prompt)
        content = response.text
        
        # Cleanup markdown if present
        content = content.replace('```json', '').replace('```', '').strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error fetching alternatives from Gemini: {e}. Returning Mock Data.")
        return mock_data

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
