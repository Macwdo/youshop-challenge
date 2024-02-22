from django.contrib import admin

from app.models import Account, AccountUser, PlantedTree, Tree, User


class AccountUserInline(admin.TabularInline):
    model = AccountUser
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

    inlines = [AccountUserInline]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'active')
    list_editable = ('active',)

    inlines = [AccountUserInline]


@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):

    list_filter = ('tree__name', 'tree__scientific_name')

    def tree_name(self, obj):
        return obj.tree.name

    def tree_scientific_name(self, obj):
        return obj.tree.scientific_name

    def user_name(self, obj):
        return obj.user.username

    # I couldn't understand the task 1.3. I think it was asked to add some filter.
    list_display = ('tree_name', 'tree_scientific_name', 'user_name')


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    ...
