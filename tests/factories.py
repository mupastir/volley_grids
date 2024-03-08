import factory

from volley_grids.models.players import MenPlayer, WomenPlayer
from volley_grids.models.teams import MenTeam, MixedTeam, WomenTeam


class MenPlayerFactory(factory.Factory):
    class Meta:
        model = MenPlayer

    age = factory.Faker('random_int', min=18, max=40)
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    points = factory.Faker('random_int', min=0, max=100)


class WomenPlayerFactory(factory.Factory):
    class Meta:
        model = WomenPlayer

    age = factory.Faker('random_int', min=18, max=40)
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    points = factory.Faker('random_int', min=0, max=100)


class MenTeamFactory(factory.Factory):
    class Meta:
        model = MenTeam

    player_one = factory.SubFactory(MenPlayerFactory)
    player_two = factory.SubFactory(MenPlayerFactory)


class WomenTeamFactory(factory.Factory):
    class Meta:
        model = WomenTeam

    player_one = factory.SubFactory(WomenPlayerFactory)
    player_two = factory.SubFactory(WomenPlayerFactory)


class MixedTeamFactory(factory.Factory):
    class Meta:
        model = MixedTeam

    player_one = factory.SubFactory(WomenPlayerFactory)
    player_two = factory.SubFactory(MenPlayerFactory)
