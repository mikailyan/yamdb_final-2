from django.urls import include, path

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       RegistrationView, ReviewViewSet, TitleViewSet,
                       TokenView)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
        RegistrationView.as_view(),
        name='signup',
    ),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='token',
    )
]
