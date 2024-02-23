from unittest import TestCase as UnitTestCase

from django.test import TestCase
from django.urls import reverse

from app.models import (
    Account,
    AccountUser,
    Coordinate,
    Plant,
    PlantedTree,
    Profile,
    Tree,
    User,
)


class FixturesMixin:
    def create_planted_tree(
        self,
        location: Coordinate = Coordinate(latitude=0, longitude=0),
        age: int = 0,
        tree: Tree = None,
        user: User = None,
        account: Account = None,
    ) -> PlantedTree:

        if not tree:
            tree = self.create_tree()

        if not user:
            user = self.create_user()

        if not account:
            account = self.create_account()

        planted_tree = PlantedTree.objects.create(
            latitude=location.latitude,
            longitude=location.longitude,
            age=age,
            tree=tree,
            user=user,
            account=account,
        )
        return planted_tree

    def create_user(
        self,
        username: str = 'username',
        email: str = 'test_user@email.co',
        password: str = 'Testpassword123#',
        first_name: str = 'Test',
        last_name: str = 'User',
    ) -> User:

        users = User.objects.all()

        if users.count() > 0:
            count = users.count()
            username = f'{username}{count + 1}'

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            profile=self.create_profile(),
        )
        user.set_password(password)
        user.save()
        return user

    def create_profile(self, about: str = 'Test About') -> Profile:
        profile = Profile.objects.create(about=about)
        return profile

    def create_tree(
        self,
        name: str = 'Test Tree name',
        scientific_name: str = 'Test Scientific Tree name',
    ) -> Tree:
        tree = Tree.objects.create(name=name, scientific_name=scientific_name)
        return tree

    def create_account(
        self, name: str = 'Test Account Name', active: bool = True
    ) -> Account:
        account = Account.objects.create(name=name, active=active)
        return account

    def create_account_user(self, account: Account, user: User) -> None:
        account_user = AccountUser.objects.create(account=account, user=user)
        return account_user


class PlantedTreeTests(TestCase, FixturesMixin):
    def setUp(self):
        self.__load_fixtures()
        return super().setUp()

    def __load_fixtures(self):
        self.__account_1 = self.create_account()
        self.__account_2 = self.create_account()
        self.__user_1 = self.create_user()
        self.__user_2 = self.create_user()
        self.__user_3 = self.create_user()

        self.__user_test_password = 'Testpassword123#'

        self.__account1_user_1 = self.create_account_user(
            account=self.__account_1, user=self.__user_1
        )
        self.__account1_user_2 = self.create_account_user(
            account=self.__account_1, user=self.__user_2
        )
        self.__account2_user_3 = self.create_account_user(
            account=self.__account_2, user=self.__user_3
        )

        self.__tree_1 = self.create_tree()

    def test_if_user_planted_trees_is_rendering(self):
        planted_tree_location_1 = Coordinate(latitude=1, longitude=2)
        planted_tree_location_2 = Coordinate(latitude=3, longitude=4)
        planted_tree_location_3 = Coordinate(latitude=5, longitude=6)
        planted_tree_1 = self.__user_1.plant_tree(
            self.__tree_1, planted_tree_location_1
        )
        planted_tree_2 = self.__user_1.plant_tree(
            self.__tree_1, planted_tree_location_2
        )
        planted_tree_3 = self.__user_1.plant_tree(
            self.__tree_1, planted_tree_location_3
        )

        self.client.login(
            username=self.__user_1.username, password=self.__user_test_password
        )
        response = self.client.get(reverse('planted_trees'))
        self.assertIn(
            f'<td>{planted_tree_1.id}</td>',
            response.content.decode('utf-8'),
        )
        self.assertIn(
            f'<td>{planted_tree_2.id}</td>',
            response.content.decode('utf-8'),
        )

        self.assertTemplateUsed(response, 'planted_trees.html')
        self.assertIn(
            f'<td>{planted_tree_3.id}</td>',
            response.content.decode('utf-8'),
        )
        self.assertIn(
            'Essas são as árvores plantadas do seu usuário',
            response.content.decode('utf-8'),
        )

    def test_user_cant_see_other_users_planted_trees(self):

        location = Coordinate(latitude=1, longitude=2)
        planted_tree = self.__user_1.plant_tree(self.__tree_1, location)

        self.client.login(
            username=self.__user_2.username, password=self.__user_test_password
        )

        response = self.client.get(
            reverse('planted_tree', args=[planted_tree.id])
        )
        self.assertTemplateUsed(response, 'forbidden.html')
        self.assertEqual(response.status_code, 403)

    def test_if_user_account_planted_trees_is_rendering(self):
        user_1 = self.__user_1
        user_2 = self.__user_2
        account_1 = self.__account_1
        tree_1 = self.__tree_1

        user_1_planted_tree = self.create_planted_tree(
            account=account_1, user=user_1, tree=tree_1
        )
        user_2_planted_tree = self.create_planted_tree(
            account=account_1, user=user_2, tree=tree_1
        )

        url = reverse('account_planted_trees')
        self.__loggin_user(user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planted_trees.html')

        self.assertIn(
            f'<td>{user_1_planted_tree.id}</td>',
            response.content.decode('utf-8'),
        )
        self.assertIn(
            f'<td>{user_2_planted_tree.id}</td>',
            response.content.decode('utf-8'),
        )
        self.assertIn(
            'Essas são as árvores plantadas da sua conta',
            response.content.decode('utf-8'),
        )

    def __loggin_user(self, user: User) -> None:
        self.client.login(
            username=user.username, password=self.__user_test_password
        )

    def tearDown(self) -> None:
        return super().tearDown()


class UserPlantTreeTests(UnitTestCase, FixturesMixin):
    def setUp(self):
        self.__load_fixtures()
        return super().setUp()

    def __load_fixtures(self):
        self.__user = self.create_user()
        ...

    def test_user_plant_tree_method(self):
        user = self.__user
        location = Coordinate(latitude=1, longitude=2)

        user.plant_tree(tree=self.create_tree(), location=location)

        query = PlantedTree.objects.filter(user=user)
        self.assertEqual(query.count(), 1)

    def test_user_plant_trees_method(self):
        user = self.__user
        tree = self.create_tree()

        planted_trees = user.plant_trees(
            plants=[
                Plant(tree=tree, location=Coordinate(latitude=1, longitude=2)),
                Plant(tree=tree, location=Coordinate(latitude=3, longitude=4)),
                Plant(tree=tree, location=Coordinate(latitude=5, longitude=6)),
            ]
        )

        planted_trees_ids = [planted_tree.id for planted_tree in planted_trees]

        query_planted_trees_ids = PlantedTree.objects.filter(
            id__in=planted_trees_ids
        ).values_list('id', flat=True)

        self.assertEqual(query_planted_trees_ids.count(), 3)
        self.assertSequenceEqual(planted_trees_ids, query_planted_trees_ids)

    def tearDown(self) -> None:
        return super().tearDown()
