from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(requests):
    """学习笔记的主页"""
    return render(requests, 'myapp1/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    result_topics = Topic.objects.order_by('date_added')
    context = {'topics': result_topics}
    return render(request, 'myapp1/topics.html', context)


def topic(request, topic_id):
    """显示所有的主题"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'myapp1/topic.html', context)


def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据: 创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myapp1:topics'))

    context = {'form': form}
    return render(request, 'myapp1/new_topic.html', context)


def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据, 对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('myapp1:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'myapp1/new_entry.html', context)


def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm(instance=entry)
    else:
        # POST 提交的数据, 对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myapp1:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'myapp1/edit_entry.html', context)
