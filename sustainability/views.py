from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import get_eco_alternatives, analyze_image, get_chart_data
from .models import UserScore, SearchHistory
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    context = {}
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        if product_name:
            # Get alternatives
            alternatives = get_eco_alternatives(product_name)
            context['alternatives'] = alternatives
            context['product_name'] = product_name
            
            # Save history and update score if user is authenticated
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, query=product_name)
                score, created = UserScore.objects.get_or_create(user=request.user)
                score.points += 10
                score.plastic_saved += 50 # Arbitrary 50g per search
                score.save()
            else:
                 SearchHistory.objects.create(user=None, query=product_name)

    return render(request, 'sustainability/index.html', context)

@login_required
def dashboard(request):
    score, created = UserScore.objects.get_or_create(user=request.user)
    recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
    chart_data = get_chart_data(request.user)
    
    context = {
        'points': score.points,
        'plastic_saved': score.plastic_saved,
        'recent_searches': recent_searches,
        'chart_data': chart_data
    }
    return render(request, 'sustainability/dashboard.html', context)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        result = analyze_image(image)
        return JsonResponse({'status': 'success', 'result': result})
    return JsonResponse({'status': 'error', 'message': 'No image uploaded'}, status=400)
