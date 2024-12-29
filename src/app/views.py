from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import Coupon, MovieEdit
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Editor, Animations, Format, BGM, Filters, Template, Section, Plan, Language, Telop, Model, Publish, Voice

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustomUser

from django.db.models import Q

from django.core.paginator import Paginator



class IndexView(View):
    def get(self, request, *args, **kwargs):
        # search_data = ''
        # sex_data = ''
        main_data = Section.objects.get(id=1)
        news_data = News.objects.all()
        plan_data = Plan.objects.all()

        
        # paginator = Paginator(item_data, 10) # 1ページに10件表示
        # paginator = Paginator(item_data, 52) # 1ページに10件表示
        # p = request.GET.get('p') # URLのパラメータから現在のページ番号を取得
        # item_data = paginator.get_page(p) # 指定のページのArticleを取得


        return render(request, 'app/U22/index.html', {
            # 'item_data': item_data,
            # 'search_data': search_data,
            # 'articles': articles
            'main_data': main_data,
            'news_data': news_data,
            'plan_data': plan_data
        })


from django.core.mail import EmailMultiAlternatives

def send_email(order_items, user_data):
    items = ''
    for item in order_items:
        items += item.item.title
        
    mail_title="ご注文していただきありがとうございます。"
    text_content="""
    　　　　　　　　　　　　{user_data.first_name}様、この度は{items}をご注文していただき誠にありがとうございます。
            """
    html_content=f"""
            <p>{user_data.first_name}様、この度は{items}をご注文していただき誠にありがとうございます。</p>
            <p><strong>※このメールに返信はできません</strong></p>
            <p>お問い合わせしたい内容がございましたら<a href="{{ request.scheme }}://{{ request.get_host }}inquiry/">こちらから</a>お願い致します。</p>
            """

    msg=EmailMultiAlternatives(
            subject=mail_title, 
            body=text_content, 
            from_email='HALG07U22@gmail.com', 
            to=[user_data.email],
            # reply_to=[]
            )
    msg.attach_alternative(html_content,"text/html")
    msg.send()


#u22
class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/cart.html', {})


class ShopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/shop.html', {})

class FavoriteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/favorite.html', {})

class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/contact.html', {})
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/login.html', {})

class DownloadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/download.html', {})
    
    
class EditorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/editor/editor-select.html', {})
    
# class EditorNewView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'app/U22/editor/editor-base.html', {})

class EditorFilterView(View):
    def get(self, request, *args, **kwargs):
        filter_data = Filters.objects.all()
        context={
            'filter_data': filter_data
        }
        return render(request, 'app/U22/editor/editor-filter.html', context)
    
class EditorGenderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/U22/editor/editor-gender.html', {})
    
class EditorFormatView(View):
    def get(self, request, *args, **kwargs):
        format_data = Format.objects.all()
        context={
            'format_data': format_data
        }
        return render(request, 'app/U22/editor/editor-format.html', context)

class EditorBgmView(View):
    def get(self, request, *args, **kwargs):
        bgm_data = BGM.objects.all()
        context={
            'bgm_data': bgm_data
        }
        return render(request, 'app/U22/editor/editor-bgm.html', context)
    
class EditorAnimationView(View):
    def get(self, request, *args, **kwargs):
        anim_data = Animations.objects.all()
        context={
            'anim_data': anim_data
        }
        return render(request, 'app/U22/editor/editor-animation.html', context)




from mysite.tasks import Edit
from mysite.tasks import add
from celery.result import AsyncResult
from django_celery_results.models import TaskResult

class EditorUploadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = MovieEdit(request.GET or None)
        #user_data = Editor.objects.get(id=request.user.id)
        # form = Editor(
        #     request.POST or None,
        #     initial={
        #         'Editor': form.upload,
        #     }
        # )
        return render(request, 'app/U22/editor/editor-upload.html',{
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = MovieEdit(request.POST, request.FILES)
        if form.is_valid():
            template = Template(user=request.user)
            template.save()

            upload = form.cleaned_data['upload']
            number = Editor.objects.all().count() + 1
            obj = Editor(id=number, user_id=request.user.id, upload=upload, 
                        template=template, 
            )
            obj.save()
            # number = obj.id
            # dataBase = Editor.objects.filter(id=number)
            # task_id = add.delay(1, 1000)
            
            # Edit(number)
            # add.delay(1, 10000)
            task_id = Edit.delay(number)
            # task_id = Edit(number)
            # Edit(number)
            # task_id = add().delay(1, 10000)
            
            return render(request, 'app/U22/editor/editor-upload.html',{
                'form': form,
                # "task_id": result.task_id
                'task_id': task_id,
            })
        
        return render(request, 'app/U22/editor/editor-upload.html',{
            'form': form
        })

# from ave.prg import *


def register_task(request):
    task_id = add.delay(1, 1000)
    context = {'task_id': task_id}
    return render(request, 'app/U22/editor/register_task.html', context)

def check_task(request):
    task_id = request.GET.get("task_id")
    task = AsyncResult(task_id)

    # チェック中のIDを取得する。
    print(task.id)

    # タスクの状態を取得する。
    # PENDING: 保留中
    # FAILURE: 失敗
    # SUCCESS: 成功
    print(task.state)

    # 非同期処理が終了したかのステータスを取得する。
    # True: 終了
    # False: 終了していない
    print(task.ready())

    # タスクの結果を取得する。
    # None: 完了していない場合は None となる。
    print(task.result)

    context = {'task': task}
    return render(request, 'app/U22/editor/check_task.html', context)


class EditorMyListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        mylist_data = Editor.objects.filter(user_id=request.user.id)
        return render(request, 'app/U22/editor/editor-mylist.html',{
            'mylist_data': mylist_data
        })
    
class EditorMyListDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            slug = self.kwargs['slug']
            editor = Editor.objects.filter(Q(user_id=request.user.id) & Q(editorId=slug)).all()
            if editor.count() != 0:
                editor.delete()
                return redirect('editor_mylist')
                # return redirect(request.session['TempPage'])
            else:
                # return redirect(request.session['TempPage'])
                return redirect('editor_mylist')
        else:
                # response = redirect(request.session['TempPage'])
                # return response
            return redirect('editor_mylist')
        

class EditorTemplateDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            slug = self.kwargs['slug']
            template = Template.objects.filter(Q(user_id=request.user.id) & Q(templateId=slug)).all()
            if template.count() != 0:
                template.delete()
                return redirect('editor_list')
                # return redirect(request.session['TempPage'])
            else:
                # return redirect(request.session['TempPage'])
                return redirect('editor_list')
        else:
                # response = redirect(request.session['TempPage'])
                # return response
            return redirect('editor_list')
        

class EditorListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        list_data = Editor.objects.filter(user_id=request.user.id).all()
        return render(request, 'app/U22/editor/editor-list.html',{
            'list_data': list_data
        })

class EditorsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = MovieEdit(request.GET or None)
        anim_data = Animations.objects.all()
        filter_data = Filters.objects.all()
        format_data = Format.objects.all()
        bgm_data = BGM.objects.all()
        
        context={
            'form': form,
            'anim_data': anim_data,
            'filter_data': filter_data,
            'format_data': format_data,
            'bgm_data': bgm_data
        }
        return render(request, 'app/U22/editor/editors.html',context)


    def post(self, request, *args, **kwargs):
        form = MovieEdit(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            # movie_data = Template()

            # movie_data.user = request.user
            # movie_data.title = form.cleaned_data['title']
            # movie_data.animations = form.cleaned_data['animations']
            # movie_data.movie_format = form.cleaned_data['movie_format']
            # movie_data.filter_effect = form.cleaned_data['filter_effect']
            # movie_data.bgm = form.cleaned_data['bgm']
            # movie_data.voice = form.cleaned_data['voice']
            # movie_data.language = form.cleaned_data['language']
            # movie_data.telopPos = form.cleaned_data['telopPos']
            # movie_data.model = form.cleaned_data['model']
            # movie_data.translate = form.cleaned_data['translate']
            # movie_data.publish = form.cleaned_data['publish']
            # movie_data.save()
            # language = form.cleaned_data['language']
            # language = Language.objects.filter(code=form.cleaned_data['language'])
            movie_data = Template(
                user=request.user, title=form.cleaned_data['title'], 
                animations_id=form.cleaned_data['animations'],
                movie_format_id=form.cleaned_data['movie_format'],
                filter_effect_id=form.cleaned_data['filter_effect'],
                bgm_id=form.cleaned_data['bgm'],
                voice=Voice.objects.get(VoiceId=form.cleaned_data['voice']),
                language=Language.objects.get(code=form.cleaned_data['language']),
                telopPos=Telop.objects.get(telopName=form.cleaned_data['telopPos']),
                model=Model.objects.get(modelId=form.cleaned_data['model']),
                translate=form.cleaned_data['translate'], 
                publish=Publish.objects.get(publishName=form.cleaned_data['publish']),
            )
            movie_data.save()

            upload = form.cleaned_data['upload']
            obj = Editor(user_id=request.user.id, upload=upload, template=movie_data,
                publish=Publish.objects.get(publishName='close')
            )
            obj.save()
            task_id = Edit.delay(obj.editorId)
            # task_id = Edit(number)
            obj.task_id = task_id.id
            obj.save()
            # request.session['task_id'] = task_id.id
            # task_id = Edit(number)
            
            # return render(request, 'app/U22/editor/editor-mylist.html',context)
            return redirect('editor_progress', slug=obj.editorId)
        return render(request, 'app/U22/editor/editors.html',context)

class EditorTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        templateId=self.kwargs['slug']
        template = Template.objects.get(user=request.user, templateId=templateId)
        
        if template.user == request.user:
            # form = MovieEdit(request.GET or None)
            # form.title = template.title
            # form.voice = template.voice.VoiceId
            # form.language = template.language.code
            # form.telopPos = template.telopPos.telopName
            # form.model = template.model.modelId
            # form.translate = template.translate

            form = MovieEdit(
                        request.GET or None,
                        initial = {
                            'title': template.title,
                            'voice': template.voice.VoiceId,
                            'language': template.language.code,
                            'telopPos': template.telopPos.telopName,
                            'model': template.model.modelId,
                            'translate': template.translate,
                            'publish': template.publish.publishName,
                        }
                    )

            anim_data = Animations.objects.all()
            filter_data = Filters.objects.all()
            format_data = Format.objects.all()
            bgm_data = BGM.objects.all()
            
            context={
                'form': form,
                'anim_data': anim_data,
                'filter_data': filter_data,
                'format_data': format_data,
                'bgm_data': bgm_data
            }
            return render(request, 'app/U22/editor/editor-template.html',context)
        return redirect('Index')
    
    def post(self, request, *args, **kwargs):
        form = MovieEdit(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            movie_data = Template()

            movie_data = Template(
                user=request.user, title=form.cleaned_data['title'], 
                animations_id=form.cleaned_data['animations'],
                movie_format_id=form.cleaned_data['movie_format'],
                filter_effect_id=form.cleaned_data['filter_effect'],
                bgm_id=form.cleaned_data['bgm'],
                voice=Voice.objects.get(VoiceId=form.cleaned_data['voice']),
                language=Language.objects.get(code=form.cleaned_data['language']),
                telopPos=Telop.objects.get(telopName=form.cleaned_data['telopPos']),
                model=Model.objects.get(modelId=form.cleaned_data['model']),
                translate=form.cleaned_data['translate'], 
                publish=Publish.objects.get(publishName=form.cleaned_data['publish']),
            )
            movie_data.save()


            upload = form.cleaned_data['upload']
            obj = Editor(user_id=request.user.id, upload=upload, template=movie_data
            )
            obj.save()
            task_id = Edit.delay(obj.editorId)
            # task_id = Edit(number)
            obj.task_id = task_id.id
            obj.save()
            
            return redirect('editor_progress', slug=obj.editorId)
        return render(request, 'app/U22/editor/editors.html',context)


class EditorDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
            editorId=self.kwargs['slug']
            editor = Editor.objects.get(editorId=editorId)
            # pub = Publish.objects.filter(publishName=editor.publish)
            if editor.publish == "公開" or editor.publish == "限定公開" or editor.user == request.user:
                anim_data = Animations.objects.all()
                filter_data = Filters.objects.all()
                format_data = Format.objects.all()
                bgm_data = BGM.objects.all()

                # form = MovieEdit(
                #     request.GET or None,
                #     initial = {
                #         'publish': editor.publish.publushName,
                #     }
                # )
                
                context={
                    'editor': editor,
                    # 'publish': form,
                    'anim_data': anim_data,
                    'filter_data': filter_data,
                    'format_data': format_data,
                    'bgm_data': bgm_data
                }
                return render(request, 'app/U22/editor/editor-detail.html',context)
            return redirect('Index')
            


class EditorProgressView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
            editorId=self.kwargs['slug']
            editor = Editor.objects.get(editorId=editorId)
            task_id = editor.task_id
            anim_data = Animations.objects.all()
            filter_data = Filters.objects.all()
            format_data = Format.objects.all()
            bgm_data = BGM.objects.all()
            
            context={
                'editor': editor,
                'task_id': task_id,
                'anim_data': anim_data,
                'filter_data': filter_data,
                'format_data': format_data,
                'bgm_data': bgm_data
            }
            return render(request, 'app/U22/editor/editor-progress.html',context)

def test(request):
    return render(request, 'app/U22/editor/test.html', {})

def ajax_number(request):
    number1 = int(request.POST.get('number1'))
    number2 = int(request.POST.get('number2'))
    plus = number1 + number2
    minus = number1 - number2
    d = {
        'plus': plus,
        'minus': minus,
    }
    return JsonResponse(d)

from django.http import HttpResponse
import json
def reload(request):
    # task_id = request.GET.get('task_id', None)
    # print ('aaaaaaaaaaa')
    task_id = request.GET.get('task_id')
    # if task_id is not None:
    task = AsyncResult(task_id)
    data = {
        'state': task.state,
        'result': task.result,
    }
    # return JsonResponse(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

def templatePublish(request):
    # task_id = request.GET.get('task_id', None)
    # print ('aaaaaaaaaaa')
    slug = request.GET.get('slug')
    switch = request.GET.get('switch')
    template = Template.objects.get(templateId=slug)
    if  template:
    # return JsonResponse(data)
        template.publish = switch
        return JsonResponse()
    return redirect('Index')

def publish(request):
    # task_id = request.GET.get('task_id', None)
    # print ('aaaaaaaaaaa')
    slug = request.GET.get('slug')
    switch = request.GET.get('switch')
    editor = Editor.objects.get(editedId=slug)
    if editor:
        editor.publish = switch
        return JsonResponse()
        
    # return JsonResponse(data)
    return redirect('Index')
# from django.http import HttpResponse
# from celery import shared_task
# import time

# @shared_task
# def task_2(message):# 裏側で実行される処理
#     time.sleep(10)# 10秒待機する
#     print(message)

# def task_1(request):# 本処理
#     message = '非同期処理'
#     task_2.delay(message)# delayメソッドでタスクを呼び出す
#     return HttpResponse('裏側に処理を投げます！')
#     # return redirect('Index')



# import time
import zipfile
from io import BytesIO
from celery import shared_task
from celery_progress.backend import ProgressRecorder

def get_file_list(zip_file):
    # zipファイル内の全てのファイルを取得する
    buffer = BytesIO(zip_file.read())
    with zipfile.ZipFile(buffer, "r") as zip_ref:
        files = zip_ref.namelist()
    return files


# @shared_task(bind=True)
# def process_files(self, file_list):
#     print(type(self))
#     progress_recorder = ProgressRecorder(self)

#     # 進行状況の初期化
#     total_files = len(file_list)
#     progress_recorder.set_progress(0, total_files)
#     print("total files: ", total_files)

#     # ファイルを読み込んで、内容を取得する
#     result = 0
#     for idx, file in enumerate(file_list):
#         # 重い処理
#         print(f"Processing {file}")
#         time.sleep(0.4)
#         # 進行状況を更新
#         print(f"Done!")
#         result += 1

#         progress_recorder.set_progress(idx + 1, total_files, description=f"処理中...({idx+1}/{total_files})")
#     return "File upload success!"


# def upload_zip_file(request):
#     if request.method == "POST":
#         form = MovieEdit(request.POST, request.FILES)

#         if form.is_valid():
#             # クライアントから送信されたzipファイルを取得する
#             print("zip uploaded.")
#             zip_file = request.FILES["zip_file"]
#             file_list = get_file_list(zip_file)

#             # ファイルを処理する
#             result = process_files.delay(file_list)

#             print(type(result), result)
#             # 処理が完了したら、リダイレクトなど適切なレスポンスを返す
#             return render(request, "upload_file/upload.html", context={"form": form, "task_id": result.task_id})
#     else:
#         form = MovieEdit()
#     # GETリクエストの場合は、ファイルアップロードのフォームを表示する
#     return render(request, "upload_file/upload.html", {"form": form})