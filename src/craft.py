#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsapi.articles import Articles
import requests
import os

from urlparse import urlparse

import datetime

import jinja2

def craft_newsletter():
    '''
    Craft the newsletter. Returns JSON.
    :return: the newsletter json
    '''

    a = Articles(API_KEY=os.environ["NEWSAPI_KEY"])
    top_results = a.get_by_top(source="google-news")

    breaking = requests.get("https://librenews.io/api").json()["latest"]

    period = "AM"
    greeting = "It's 5:30 ZULU time."

    if datetime.datetime.now(tz=None).time() > datetime.time(12):
        period = "PM"
        greeting = "It's 17:30 ZULU time."

    name = period + " - " + datetime.date.today().strftime("%A, %d %B %Y")

    for story in top_results["articles"]:
        story["source"] = urlparse(story["url"]).netloc

    return {
        "top_stories": top_results["articles"][:3],
        "breaking": [story for story in breaking if story["channel"] == "Breaking News"][:5],
        "name": name,
        "greeting": greeting
    }

def craft_html(newsletter):
    base_template = '''
    <h1 style="font-family: sans-serif;">530ZULU<br><small style="font-family: sans-serif; color: gray; display: inline;">{{name}}</small></h1>
    <p style="font-family: sans-serif;">{{greeting}} Here's the latest:</p>
    <ul>
    {% for flash in breaking %}
        <li style="font-family: sans-serif;">{{flash.text}} <a href="{{flash.link}}">&rarr;</a></li>
    {% endfor %}
    </ul>
    <p style="font-family: sans-serif;">Here are the headlines:</p>
    <ul>
    {% for story in stories %}
        <li>
            <a style="font-family: sans-serif;" href="{{story.url}}">{{story.title}}</a>
            <p style="font-family: sans-serif;">{{story.description}} <small style="font-family: sans-serif; color: gray;">{{story.source}}</small></p>
        </li>
    {% endfor %}
    </ul>
    <br>
    <small style="font-family: monospace;">Powered by <a href="https://librenews.io">LibreNews</a>, <a href="https://newsapi.org">NewsAPI</a>, and <a href="https://news.google.com">Google News</a>. Created by <a href="https://rmrm.io">Miles McCain</a>.</small>
    '''
    template = jinja2.Template(base_template)
    html = template.render(name=newsletter["name"], stories=newsletter["top_stories"], breaking=newsletter["breaking"], greeting=newsletter["greeting"])
    return html

def craft_text(newsletter):
    base_template = '''{{name}} (TEXT ONLY VERSION)

Top Stories
------------------
        
{% for story in stories %}
{{story.title}}
{{story.description}}
{{story.url}}
{% endfor %}

Breaking
------------------
{% for flash in breaking %}
{{flash.text}} -- {{flash.link}}
{% endfor %}

-----
Powered by LibreNews, NewsAPI, and Google News. Created by Miles McCain.'''
    template = jinja2.Template(base_template)
    text = template.render(name=newsletter["name"], stories=newsletter["top_stories"], breaking=newsletter["breaking"], greeting=newsletter["greeting"])
    return text
