from django.contrib import admin

from app.models import Account, AccountUser, PlantedTree, Tree, User

# Adding 'search_fields' to help search in the admin panel


class AccountUserInline(admin.TabularInline):
    model = AccountUser
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name')

    inlines = [
        AccountUserInline
    ]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'created_at', 'active')
    list_editable = ('active',)

    inlines = [
        AccountUserInline
    ]

@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):

    
    def tree_name(self, obj):
        return obj.tree.name
    list_display = ('tree_name',)
