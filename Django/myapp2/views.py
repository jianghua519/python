from django.shortcuts import render
from .models import CaclValuesTbl


# Create your views here.

def share(request):
    """显示所有的主题"""
    topic = CaclValuesTbl.objects.get(share_code='9603')
    result_topics = CaclValuesTbl.objects.order_by('date_added')
    context = {'topics': result_topics}
    return render(request, 'myapp1/topics.html', context)
