from typing import Any, Dict
from django.db import models
from django.views import generic

class MetaTagMixin(models.Model):
    name = None
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    
    def get_meta_title(self):
        return self.meta_title or self.name
    
    class Meta:
        abstract = True

class ListViewBreadCrumbMixin(generic.ListView):
    breadcrumbs = {}
    
    def get_breadcrumbs(self):
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context

class DetailViewBreadcrumbsMixin(generic.DetailView):
    breadcrumbs = {}
    
    def get_breadcrumbs(self):
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context