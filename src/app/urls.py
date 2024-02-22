from django.urls import path

from app.api.viewsets import PlantedTreesViewSet
from app.views import (
    account_planted_trees,
    login,
    logout,
    new_planted_tree,
    new_planted_tree_page,
    planted_tree_detail,
    planted_trees,
)

urlpatterns = [
    path(
        'api/my-planted-trees/',
        PlantedTreesViewSet.as_view(),
        name='my-planted-trees',
    ),
    path('login/', login, name='login'),
    path('planted-trees', planted_trees, name='planted_trees'),
    path(
        'account-planted-trees',
        account_planted_trees,
        name='account_planted_trees',
    ),
    path('logout/', logout, name='logout'),
    path(
        'planted-tree/<int:tree_id>/', planted_tree_detail, name='planted_tree'
    ),
    path('new-planted-tree/', new_planted_tree_page, name='new_planted_tree'),
    path(
        'new-planted-tree/create/',
        new_planted_tree,
        name='new_planted_tree_create',
    ),
]
