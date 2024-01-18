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

    def post(self, request, *args, **kwargs):
        
        # search_data = ''
        item_data = Item.objects.all()
        search_data = request.POST['search']
        search_id_data = request.POST['search_id']
        sex_data = request.POST['sex']
        
        # if sex_data == 'man':
        #     sex_result = Item.objects.filter(Q(sex=sex_data)).all()
        # elif sex_data == 'woman':
        #     sex_result = Item.objects.filter(Q(sex=sex_data)).all()
        # else:
        #     sex_result = Item.objects.filter(Q(sex__contains="man")).all()
        print(Item.objects.filter(Q(sex=sex_data)).all())

        if search_id_data == 'title':
            result = Item.objects.filter(Q(title__contains=search_data)).all() # | Q(title=search_data) | Q(title__contains=search_data) | Q(brand__contains=search_data)
        elif search_id_data == 'category':
            result = Item.objects.filter(Q(category=search_data)).all()
            
        elif search_id_data == 'brand':
            result = Item.objects.filter(Q(brand__contains=search_data)).all()
        else:
            result = Item.objects.filter(Q(title__contains=search_data) | Q(category=search_data) | Q(brand__contains=search_data)).all()

        return render(request, 'app/store/index.html', {
            'item_data': item_data,
            'search_data': result
        })

class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        item_data = Item.objects.get(slug=slug)
        review_data = Review.objects.filter(content_id=slug)
        Favorite_Item_List = FavoriteItemList.objects.filter(Q(user_id=request.user.id) & Q(favorite_item=slug)).all()
        Favorite_data = False
        if Favorite_Item_List.count() == 0:
            Favorite_data = True
            

        paginator = Paginator(review_data, 3)
        p = request.GET.get('p')
        review_data = paginator.get_page(p)
        request.session['TempPage'] = request.build_absolute_uri()

        return render(request, "app/store/product.html", {
            'item_data': item_data,
            "review_data": review_data,
            'slug': slug,
            'favorite': Favorite_data
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_for_item_count = self.object.like_for_item_set.count()
        # ポストに対するイイね数
        context['like_for_item_count'] = like_for_item_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.like_for_item_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_item'] = True
        else:
            context['is_user_liked_for_item'] = False

        return context


class ItemReviewView(View):
    
    
    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        item_data = Item.objects.get(slug=slug)
        review_data = Item.objects.filter(content_id=slug)
        return render(request, "app/store/product.html", {
            'item_data': item_data,
            'slug': slug
        })
    


class ReviewPost(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        form = PostReview(request.POST or None)
        print (item_data)
        # review_data = Review.objects.filter(content_id=self.kwargs['slug'])
        context={
            'form': form,
            'item_data': item_data
        }
        return render(request, "app/review/review_post.html", context)
    
    def post(self, request, *args, **kwargs):
        content_id=self.kwargs['slug']
        order = OrderItem.objects.filter(user_id=request.user.id, item__slug=content_id)
        rate = request.POST['rate']
        
        bought = False
        if order:
            bought = True

        #orderedがされたらという機能を入れるつもりだったけど、HEWなのと、Orderedされる処理は……って考えると今は不明。入れてもいいけど……時間があれば。

        if not(1 <= int(rate) <=5):
            raise ValueError('評価基準がおかしい。')
        form = PostReview(request.POST or None)
        if form.is_valid():
            obj = Review(
                title=form.cleaned_data['title'], 
                content=form.cleaned_data['content'],
                like=rate, bought=bought, content_id=content_id,
                author=request.user
                )

            obj.save()
            return redirect('review_success')
        else:
            print('error')
            if form.is_valid() == False:
                for ele in form :
                    print(ele)

        context={
            'form': form
            # 'Item': item_data
        }
        # return render(request, "app/review_check.html", context)
        return render(request, "app/review/review_post.html", context)

class ReviewSuccess(View):
    def get(self, request, *args, **kwargs):
        UserName = CustomUser.objects.get(id=request.user.id)
        context = {
            'User': UserName.first_name
        }
        return render(request, "app/review/review_success.html", context)

class ReviewList(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            item_data = Item.objects.all()
            Review_Data = Review.objects.filter(Q(author_id=request.user.id))
            paginator = Paginator(Review_Data, 10)
            p = request.GET.get('p')
            Review_Data = paginator.get_page(p)
            request.session['TempPage'] = request.build_absolute_uri()

            context={
                'item_data': item_data,
                'Review_Data': Review_Data
            }
            return render(request, 'app/review/review_list.html', context)
        else:
                response = redirect('Index')
                return response



class ReviewEdit(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            context = {}
            user_id = request.user.id
            Review_ID = self.kwargs['int']
            slug = self.kwargs['slug']
            
            request.session['TempPage'] = request.build_absolute_uri()

            Review_Data = Review.objects.filter(Q(author_id=user_id) & Q(content_id=slug) & Q(id=Review_ID))

            if Review_Data.count() > 0:
                form = PostReview(
                request.GET or None,
                initial = {
                    'title': Review_Data.last().title,
                    'content': Review_Data.last().content,
                }
            )
        
                context={
                    'form': form
                }
                return render(request, 'app/review/review_edit.html', context)
            else:
                return redirect(request.session['TempPage'])
        else:
                response = redirect('Index')
                return response
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            user_id = request.user.id
            Review_ID = self.kwargs['int']
            slug = self.kwargs['slug']
            Review_Data = Review.objects.filter(Q(author_id=user_id) & Q(content_id=slug) & Q(id=Review_ID)).last()
            
            request.session['TempPage'] = request.build_absolute_uri()
            
            rate = request.POST['rate']
            
            form = PostReview(request.POST or None)

            if form.is_valid():
                Review_Data.title = form.cleaned_data['title']
                Review_Data.content = form.cleaned_data['content']
                Review_Data.like = rate
                Review_Data.save()

            return redirect('review_list')
        else:
                response = redirect('Index')
                return response

class ReviewDelete(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            user_id = request.user.id
            Review_ID = self.kwargs['int']
            slug = self.kwargs['slug']
            Review_Data = Review.objects.filter(Q(author_id=user_id) & Q(content_id=slug) & Q(id=Review_ID))

            if Review_Data.count() > 0:
                Review_Data.last().delete()
            else:
                return redirect(request.session['TempPage'])
            return redirect(request.session['TempPage'])
        else:
                return redirect(request.session['TempPage'])


@login_required
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect('order')


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            form = Coupon(request.POST or None)
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order,
                'form': form
            }
            return render(request, 'app/store/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/store/order.html')
        
    def post(self, request, *args, **kwargs):
        try:
            form = Coupon(request.POST or None)
            order = Order.objects.get(user=request.user, ordered=False)
            
            # code = form.cleaned_data['couponcode']
            # result = 0
            # if form.valid():
            #     if Coupon.objects.filter(Q(coupon_code=code)).exists():
            #         result = Coupon.objects.filter(Q(coupon_code=code))
            # else:
            #     raise form.ValueError('正しいクーポンコードを入力してください。')
            context = {
                'order': order,
                'form': form,
                # 'couponresult': result
            }
            return render(request, 'app/store/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/store/order.html')

@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('order')

    return redirect('product', slug=slug)


@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect('order')
    return redirect('product', slug=slug)


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {
            'order': order,
            'user_data': user_data
        }
        return render(request, 'app/store/payment.html', context)

    def post(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        # print(user_data)
        if not(user_data.first_name == '' or user_data.last_name == '' or user_data.zipcode == '' or user_data.address == '' or user_data.tel == ''):
        
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            amount = order.get_total()

            payment = Payment(user=request.user)
            payment.stripe_change_id = 'test_stripe_charge_id'
            payment.amount = amount
            payment.save()

            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()
            
            send_email(order_items, user_data)

            return redirect('thanks')
        else:
            Switch = True
            user_data = CustomUser.objects.get(id=request.user.id)
            return render(request, 'accounts/profile/profile.html', {
                'user_data': user_data,
                'Switch': Switch
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

class FavoriteMenuView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            request.session['TempPage'] = request.build_absolute_uri()
            return render(request, 'app/store/favoritemenu.html')
        else:
                response = redirect('Index')
                return response

class ReviewMenuView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            request.session['TempPage'] = request.build_absolute_uri()
            return render(request, 'app/review/review_menu.html')
        else:
                response = redirect('Index')
                return response


class FavoriteFashionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
# Using item:
        context = {}
        if request.method == 'GET':
            request.session['TempPage'] = request.build_absolute_uri()

            item_data = Item.objects.all()

            Favorite_Item_List = FavoriteFashionListItem.objects.filter(user_id=request.user.id).all()
            
            paginator = Paginator(Favorite_Item_List, 20)
            p = request.GET.get('p')
            Favorite_Item_List = paginator.get_page(p)
            

            fashion_item_data = FashionSaveList.objects.filter(publish=True).all()

            fashion_list_data = FashionItemList.objects.filter().all()
            #↑要素があるものだけを取り出すという機能にできるならばするべき。

            # paginator = Paginator(fashion_item_data, 20)
            # p = request.GET.get('p')
            # fashion_item_data = paginator.get_page(p)
            
            context={
                'item_data': item_data,
                'fashion_item_data': fashion_item_data,
                'fashion_list_data': fashion_list_data,
                'Favorite_Item_List': Favorite_Item_List
            }
            
            return render(request, 'app/store/favorite_fashion.html', context)
        else:
                response = redirect('Index')
                return response
        
        
# お気に入りファッションコーデ一覧 ADD
class FavoriteItemListAdd(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            slug = self.kwargs['slug']
            Favorite_Item_List = FavoriteFashionListItem.objects.filter(Q(user_id=request.user.id) & Q(favorite_item=slug)).all()
            if Favorite_Item_List.count() == 0:
                obj = FavoriteFashionListItem(
                    user_id=request.user.id,
                    favorite_item=slug
                )
                obj.save()
            
                return redirect(request.session['TempPage'])
            else:
                return redirect(request.session['TempPage'])
        else:
                response = redirect('Index')
                return response

class FavoriteItemListDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            slug = self.kwargs['slug']
            Favorite_Item_List = FavoriteFashionListItem.objects.filter(Q(user_id=request.user.id) & Q(favorite_item=slug)).all()

            if Favorite_Item_List.count() != 0:
                Favorite_Item_List.delete()
                # return redirect('product', slug)
                return redirect(request.session['TempPage'])
            else:
                return redirect(request.session['TempPage'])
        else:
                response = redirect(request.session['TempPage'])
                return response


# お気に入りアイテム一覧
class FavoriteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
# Using item:
        context = {}
        if request.method == 'GET':
            item_data = Item.objects.all()
            Favorite_Item_List = FavoriteItemList.objects.filter(user_id=request.user.id).all()
            
            paginator = Paginator(Favorite_Item_List, 20)
            p = request.GET.get('p')
            Favorite_Item_List = paginator.get_page(p)

            request.session['TempPage'] = request.build_absolute_uri()
            context={
                'item_data': item_data,
                'Favorite_Item_List': Favorite_Item_List
            }
            return render(request, 'app/store/favorite.html', context)
        else:
                response = redirect('Index')
                return response


class FavoriteItemView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.method == 'GET':
            slug = self.kwargs['slug']
            Favorite_Item_List = FavoriteItemList.objects.filter(Q(user_id=request.user.id) & Q(favorite_item=slug)).all()
            if Favorite_Item_List.count() == 0:
                obj = FavoriteItemList(
                    user_id=request.user.id,
                    favorite_item=slug
                )
                obj.save()
                return redirect('product', slug)
            else:
                return redirect('product', slug)
        else:
                response = redirect('Index')
                return response
        

class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/store/thanks.html')
    

class MemberView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/test/hew_group.html')

class LoadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/test/load.html')





def like(request):
    print ("aaa")
    article_pk = request.POST.get('article_pk')
    context = {
        'user_id': f'{ request.user }',
    }
    article = get_object_or_404(FashionSaveList, slug=article_pk)
    like = Like.objects.filter(target=article, user_id=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=article, user_id=request.user)
        context['method'] = 'create'

    context['like_count'] = article.like_set.count()

    return JsonResponse(context)

from django.http import JsonResponse  # 追加
def like_for_post(request):
    item_pk = request.POST.get('item_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    post = get_object_or_404(Item, slug=item_pk)
    like = LikeForPost.objects.filter(target=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        context['method'] = 'create'

    context['like_for_post_count'] = post.likeforpost_set.count()

    return JsonResponse(context)



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