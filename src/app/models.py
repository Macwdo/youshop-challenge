from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from pydantic import BaseModel


class Plant(BaseModel):
    tree: 'Tree'
    location: 'Coordinate'


class Coordinate(BaseModel):
    latitude: float
    longitude: float


# Create your models here.
class Tree(models.Model):

    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name} - {self.scientific_name}'


class Account(models.Model):

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}'


class AccountUser(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.account} - {self.user}'


class User(AbstractUser):
    def plant_tree(self, tree: Tree, location: 'Coordinate') -> PlantedTree:
        planted_tree = PlantedTree.objects.create(
            tree=tree,
            latitude=location.latitude,
            longitude=location.longitude,
            user=self,
        )
        planted_tree.save()
        return planted_tree

    def plant_trees(self, plants: list['Plant']) -> None:
        for plant in plants:
            self.plant_tree(plant.tree, plant.location)

    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f'{self.username}'


class Profile(models.Model):
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)


class PlantedTree(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()

    age = models.IntegerField(default=0, blank=True)
    planted_at = models.DateTimeField(auto_now_add=True)

    tree = models.ForeignKey('Tree', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f'{self.tree} at {self.latitude}, {self.longitude}'

    @property
    def location(self) -> Coordinate:
        return Coordinate(latitude=self.latitude, longitude=self.longitude)
