from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

urlpatterns = [
    path("api/", csrf_exempt(GraphQLView.as_view(graphiql=True))), 
]