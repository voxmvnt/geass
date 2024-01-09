from typing import Any
from django.shortcuts import render
from .models import Post, Category, Tag, Comment, Like, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   
from django.utils.text import slugify   
from django.shortcuts import get_object_or_404  
from django.core.exceptions import PermissionDenied   
from django.db.models import Q  
from .forms import CommentForm, EditCommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.socialaccount.models import SocialAccount
from django.utils.functional import SimpleLazyObject

class PostList(ListView):
    model = Post
    ordering = "-pk"
    paginate_by = 4

    # get 메서드는 클래스가 요청을 받을 때 호출되는 메서드이며
    # 이를 통해 paginate_by를 동적으로 변경할 수 있습니다.
    def get(self, request, *args, **kwargs):
        pagenate_num = self.request.GET.get('pagenate_num')
        if pagenate_num:
            self.paginate_by = int(pagenate_num)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()  
        context['categories'] = Category.objects.all()
        context['all_post_count'] = Post.objects.count()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        if self.paginate_by is not None:
            page_obj = context['page_obj']
            paginator = context['paginator']
            context['pagenate_num'] = self.paginate_by
            context['is_paginated'] = page_obj.has_other_pages()
            context['prev_page_number'] = page_obj.previous_page_number() if page_obj.has_previous() else None
            context['next_page_number'] = page_obj.next_page_number() if page_obj.has_next() else None
            context['page_range'] = self.get_page_range(paginator, page_obj)
            context['show_right_end_button'] = page_obj.number < paginator.num_pages - 2 and paginator.num_pages > 5
            is_alert = self.request.GET.get('isAlert')
            if is_alert == 'Y':
                context['alert_message'] = "권한이 없습니다."
        return context
    
    def get_page_range(self, paginator, page_obj):
        # 페이지 번호를 그룹화하여 표시하는 로직
        current_page = page_obj.number
        total_pages = paginator.num_pages

        if total_pages <= 5:
            return range(1, total_pages + 1)
        elif current_page <= 3:
            return range(1, 6)
        elif current_page >= total_pages - 2:
            return range(total_pages - 4, total_pages + 1)
        else:
            return range(current_page - 2, current_page + 3)


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['all_post_count'] = Post.objects.count()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['likes_count'] = self.object.likes.count()
        if self.object.likes.count() > 0:
            current_user = self.request.user
            if current_user in self.object.likes.all():
                context['like_yn'] = "Y"
        context['comment_form'] = CommentForm
        context['edit_comment_form'] = EditCommentForm()
        context['ext_list'] = ['aac', 'ai', 'bmp', 'cs', 'css', 'csv', 'doc', 'docx', 'exe', 'gif', 'heic', 
                               'html', 'java', 'jpg', 'js', 'json', 'jsx', 'key', 'm4p', 'md', 'mdx', 'mov', 
                               'mp3', 'mp4', 'otf', 'pdf', 'php', 'png', 'ppt', 'pptx', 'psd', 'py', 'raw', 
                               'rb', 'sass', 'scss', 'sh', 'sql', 'svg', 'tiff', 'tsx', 'ttf', 'txt', 'wav', 
                               'woff', 'xls', 'xlsx', 'xml', 'yml']
        return context


def category_page(request, slug):  
    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,
            "categories": Category.objects.all(),
            "all_post_count": Post.objects.count(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,   
        },
    )


def tag_page(request, slug):  
    tag = Tag.objects.get(slug=slug)   
    post_list = tag.post_set.all()  

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,
            'tag': tag,
            "categories": Category.objects.all(),
            "all_post_count": Post.objects.count(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
        },
    )


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ["title", 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        current_user = self.request.user
        try:
            social_account = SocialAccount.objects.get(user=current_user)
            return True 
        except SocialAccount.DoesNotExist:
            return current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff)
        
    def handle_no_permission(self):
        return redirect("/blog/?isAlert=Y")   

    def form_valid(self, form): 
        current_user = self.request.user
        if self.test_func(): 
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form) 
            tags_str = self.request.POST.get("tags_str")
            if tags_str:
                tags_str = tags_str.strip()
                tags_list = tags_str.split("#")   
                for t in tags_list:
                    t = t.strip()
                    if t:  
                        tag, is_tag_created = Tag.objects.get_or_create(name=t)
                        if is_tag_created:
                            tag.slug = slugify(t, allow_unicode=True)
                            tag.save()
                        self.object.tags.add(tag)
            return response
        else:
            return redirect("/blog/?isAlert=Y")  
                    

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", 'content', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_update_form.html'   

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ' #'.join(tags_str_list)
        return context
    
    def dispatch(self, request, *args, **kwargs):  
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form) 
        self.object.tags.clear()
        tags_str = self.request.POST.get("tags_str")
        if tags_str:
            tags_str = tags_str.strip()
            tags_list = tags_str.split("#")  
            for t in tags_list:
                t = t.strip()
                if t:
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
        return response


def post_delete(request):
    try:
        post_pk = request.POST.get('post_pk')
        if post_pk:
            post = get_object_or_404(Post, pk=post_pk)
            if request.user == post.author:
                post.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid post_pk'})
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False, 'error': 'An error occurred during post deletion'})   


def post_like(request):
    try:
        post_pk = request.POST.get('post_pk')
        if post_pk:
            post = get_object_or_404(Post, pk=post_pk)
            current_user = request.user
            if not Like.objects.filter(name=current_user).exists():
                new_like = Like.objects.create(name=current_user)
            like_object, created = Like.objects.get_or_create(name=current_user)
            if like_object in post.likes.all():
                post.likes.remove(like_object)
                liked = False
                like_num = post.likes.count()
            else:
                post.likes.add(like_object)
                liked = True
                like_num = post.likes.count()
            return JsonResponse({'success': True, 'liked': liked, 'like_num': like_num})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid post_pk'})
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False, 'error': 'An error occurred during post like'})


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)  
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():  
                comment = comment_form.save(commit=False)
                comment.post = post   
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    

class CommentUpdate(LoginRequiredMixin, UpdateView): 
    model = Comment
    form_class = CommentForm 

    def dispatch(self, request, *args, **kwargs):  
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)  
        else:
            raise PermissionDenied
        

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    
    
class PostSearch(PostList): 
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        st = self.request.GET.get("searchType")
        query = Q(title__contains=q) | Q(tags__name__contains=q) | Q(author__username__contains=q)
        if st == "title":
            query = Q(title__contains=q)
        elif st == "tag":
            query = Q(tags__name__contains=q)
        elif st == "author":
            # 외래키 관계에서는 해당 모델의 필드를 직접 사용
            query = Q(author__username__contains=q)
        post_list = Post.objects.filter(query).order_by('-pk').distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        st = self.request.GET.get("searchType")
        st_text = "전체"
        if st == "title":
            st_text = '제목'
        elif st == "tag":
            st_text = '태그'
        elif st == "author":
            st_text = '작성자'
        context['search_info'] = f'{st_text} 검색결과: {q} ({self.get_queryset().count()})'
        return context
    
