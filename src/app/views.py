from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, PlantedTreesForm
from app.models import AccountUser, Coordinate, PlantedTree, User


def handler403(request, exception):
    return render(
        request, 'forbidden.html', status=403, context={'exception': exception}
    )


def handler404(request, exception):
    return render(
        request, 'not_found.html', status=404, context={'exception': exception}
    )


@require_http_methods(['GET'])
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect(reverse('planted_trees'))

    form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context=context)


@require_http_methods(['POST'])
def login_auth(request: HttpRequest) -> HttpResponseRedirect:
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login efetuado com sucesso')
        else:
            messages.error(request, 'Nome ou senha invalida')
    else:
        messages.error(request, 'Dados inválidos')

    return redirect(reverse('planted_trees'))


@login_required()
def logout(request: HttpRequest) -> HttpResponseRedirect:
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect(reverse('login'))


@login_required()
def planted_trees(request: HttpRequest) -> HttpResponse:
    planted_trees = PlantedTree.objects.filter(user=request.user)
    context = {'planted_trees': planted_trees}
    return render(request, 'planted_trees.html', context=context)


@require_http_methods(['GET'])
@login_required()
def account_planted_trees(request: HttpRequest) -> HttpResponse:
    user_accounts = AccountUser.objects.filter(user=request.user)
    accounts_ids = user_accounts.values_list('account_id', flat=True)
    planted_trees = PlantedTree.objects.filter(
        Q(account__in=accounts_ids) | Q(user=request.user)
    )

    context = {'planted_trees': planted_trees, 'account_planted_trees': True}
    return render(request, 'planted_trees.html', context=context)


@require_http_methods(['GET'])
@login_required()
def planted_tree_detail(
    request: HttpRequest, tree_id: int
) -> HttpResponse | HttpResponseForbidden:
    planted_tree = get_object_or_404(PlantedTree, pk=tree_id)
    if planted_tree.user != request.user:
        raise PermissionDenied(
            'Você não pode ver á árvore plantada por outro usuário'
        )

    context = {'planted_tree': planted_tree}
    return render(request, 'planted_tree_detail.html', context)


@require_http_methods(['GET'])
@login_required()
def new_planted_tree_page(request: HttpRequest) -> HttpResponse:
    form = PlantedTreesForm()
    context = {'form': form}
    return render(request, 'new_planted_tree.html', context)


@require_http_methods(['POST'])
@login_required()
def new_planted_tree(request: HttpRequest) -> HttpResponseRedirect:
    form = PlantedTreesForm(request.POST)
    request_user: User = request.user
    if form.is_valid():
        location = Coordinate(
            latitude=form.cleaned_data['latitude'],
            longitude=form.cleaned_data['longitude'],
        )
        planted_tree: PlantedTree = request_user.plant_tree(
            form.cleaned_data['tree'], location
        )
        planted_tree.age = form.cleaned_data['age']
        planted_tree.save()
        messages.success(request, 'A árvore plantada foi salva com sucesso')
    else:
        messages.error(request, 'Erro ao plantar árvore')

    return redirect(reverse('planted_trees'))
