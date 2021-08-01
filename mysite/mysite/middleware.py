# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

class Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'cv.realwebcreator.es' in request.META['HTTP_HOST'] and not request.path.startswith('/polls'):
            return redirect('/polls/')
        elif 'location.realwebcreator.es' in request.META['HTTP_HOST'] and not request.path.startswith('/holiday'):
            return redirect('/holiday/')
        
        return None
  
    def process_template_response(self, request, response):
        return response
