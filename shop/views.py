from django.db.models import Q

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from config.settings import PAGE_NAMES
from .models import Category, Book, Image
from main.mixins import ListViewBreadCrumbMixin, DetailViewBreadcrumbsMixin

from comments.models import CommentBook
from comments.forms import CommentBookForm
from blog.models import Article
# Create your views here.

class CatalogIndexView(ListViewBreadCrumbMixin):
    template_name = 'shop/index.html'
    model = Category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return Category.objects.filter(parent=None)
    
    def get_breadcrumbs(self):
        self.breadcrumbs = {
            'current' : PAGE_NAMES['catalog'],
        }
        return self.breadcrumbs
    
class AllBooksView(ListViewBreadCrumbMixin):
    template_name ='shop/all_books.html'
    
    def get_queryset(self):
        return Book.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context
    
class AllCategoriesView(ListViewBreadCrumbMixin):
    template_name ='shop/all_categories.html'
    
    def get_queryset(self):
        return Category.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
class BookByCategory(ListViewBreadCrumbMixin):
    template_name = 'shop/book_list.html'
    category = None
    categories = Category.objects.all()
    paginate_by = 6    
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Book.objects.filter(category=self.category)
        # print(Book.objects.filter(category=self.category))
        # print(Book.objects.all().first().category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["categories"] = self.categories
        print(Category.objects.get(slug=self.kwargs['slug']))
        
        context['books'] = Book.objects.filter(category=Category.objects.get(slug=self.kwargs['slug']))
        return context    
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        if self.category.parent:
            linkss = []
            parent = self.category.parent
            while parent is not None:
                linkss.append(
                    (
                        reverse('category', kwargs={'slug': parent.slug}),
                        parent.name
                    )
                )
                parent = parent.parent
            for url, name in linkss[::-1]:
                breadcrumbs[url] = name
                #breadcrumbs.update({url: name}) # або так
        breadcrumbs.update({'current': self.category.name})
        return breadcrumbs

class BookDetailView(DetailViewBreadcrumbsMixin):    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        category = self.object.main_category()
        if category:
            if category.parent:
                linkss = []
                parent = category.parent
                while parent is not None:
                    linkss.append(
                        (
                            reverse('category', kwargs={'slug': parent.slug}),
                            parent.name
                        )
                    )
                    parent = parent.parent
                for url, name in linkss[::-1]:
                    breadcrumbs.update({url: name})
            breadcrumbs.update({reverse('category', kwargs={'slug': category.slug}): category.name})
        breadcrumbs.update({'current': self.object.name})
        return breadcrumbs
    
    def get(self, request, slug):
        form = CommentBookForm()
        book = Book.objects.filter(slug=slug).first()
        related_articles = Article.objects.filter(related_book=book)
        comments = CommentBook.objects.filter(book=book)
        return render(request, 'shop/book_detail.html', {'form': form, 'book': book, 'comments': comments, 'related_articles': related_articles})
    
    def post(self, request, slug):
        book = Book.objects.filter(slug=slug).first()
        related_articles = Article.objects.filter(related_book=book)
        print(related_articles)
        form = CommentBookForm(request.POST, request.FILES)
        comments = CommentBook.objects.filter(book=book)
        if form.is_valid():
            comment = form.save(user=request.user, book=book)
            return redirect('book', slug=slug)
        render(request, 'shop/book_detail.html', {'form': form, 'book': book, 'comments': comments, 'related_articles': related_articles})

def user_book_list(request, pk):
    books = Book.objects.filter(owner=pk)
    return render(request, 'shop/custom_list.html', {'books': books})

def delete_image(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, book__owner=request.user)
    image.delete()
    return redirect('book', slug=slug)

def set_main_image(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, book__owner=request.user)
    image.set_main()
    return redirect('book', slug=slug)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('all_categories')

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('catalog')