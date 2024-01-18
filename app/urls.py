from django.urls import path
from app import views

# app_name = 'app'
urlpatterns = [
    path("", views.IndexView.as_view(), name="Index"),
    # path("product/<slug>", views.ItemDetailView.as_view(), name="product"),
    # path("additem/<slug>", views.addItem, name="additem"),
    # path("order/", views.OrderView.as_view(), name="order"),
    # path("removeitem<slug>", views.removeItem, name="removeitem"),
    # path("removesingleitem<slug>", views.removeSingleItem, name="removesingleitem"),
    # path("payment/", views.PaymentView.as_view(), name="payment"),
    
    # path("cart", views.CartView.as_view(), name="cart"),
    # path("shop", views.ShopView.as_view(), name="shop"),
    # path("favorite", views.FavoriteView.as_view(), name="favorite"),
    # path("contact", views.ContactView.as_view(), name="contact"),
    # path("login", views.LoginView.as_view(), name="app_login"),
    # path("download", views.DownloadView.as_view(), name="download"),

    path("editor/", views.EditorView.as_view(), name="editor"),
    path("editors", views.EditorsView.as_view(), name="editors"),
    path("editor/mylist", views.EditorMyListView.as_view(), name="editor_mylist"),
    path("editor/mylist/delete/<slug>", views.EditorMyListDeleteView.as_view(), name="editor_mylist_delete"),
    
    path("editor/list", views.EditorListView.as_view(), name="editor_list"),
    path("editor/template/<slug>", views.EditorTemplateView.as_view(), name="editor_template"),
    path("editor/template/delete/<slug>", views.EditorTemplateDeleteView.as_view(), name="editor_template_delete"),
    path("editor/view/<slug>", views.EditorDetailView.as_view(), name="editor_detail"),
    path("editor/progress/<slug>", views.EditorProgressView.as_view(), name="editor_progress"),
    
    path("test", views.test, name="test"),
    path('ajax-number/', views.ajax_number, name='ajax_number'),
    path('reload/', views.reload, name='reload'),
    path('editor/template/publish/', views.templatePublish, name='templatePublish'),
    path('editor/publish/', views.publish, name='publish'),

    path('register_task', views.register_task, name='register_task'),
    path('check_task', views.check_task, name='check_task'),

    # path('task_1', views.task_1, name='task_1'),
]