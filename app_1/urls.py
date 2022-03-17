from app_1.views import index
from django.urls import path


app_name='app_1'
urlpatterns = [
	path('', index)

]