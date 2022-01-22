"""Database classes and functions for project."""
from peewee import *
from random import choice, randint
from definitions import SHIPS_DB_PATH, SHIPS_DB_COPY_PATH

database = SqliteDatabase(SHIPS_DB_PATH)
database_for_compare = SqliteDatabase(SHIPS_DB_COPY_PATH)


def make_table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + 's'


class BaseModel(Model):
    class Meta:
        database = database
        table_function = make_table_name


class BaseModelForCompare(Model):
    class Meta:
        database = database_for_compare


class Engine(BaseModel):
    engine = TextField(primary_key=True)
    power = IntegerField()
    type = IntegerField()


class Hull(BaseModel):
    hull = TextField(primary_key=True)
    armor = IntegerField()
    type = IntegerField()
    capacity = IntegerField()


class HullForCompare(BaseModelForCompare):
    hull = TextField(primary_key=True)
    armor = IntegerField()
    type = IntegerField()
    capacity = IntegerField()

    class Meta:
        table_name = 'hulls'


class Weapon(BaseModel):
    weapon = TextField(primary_key=True)
    reload_speed = IntegerField()
    rotation_speed = IntegerField()
    diameter = IntegerField()
    power_volley = IntegerField()
    count = IntegerField()


class Ship(BaseModel):
    ship = TextField(primary_key=True)
    weapon = ForeignKeyField(Weapon, column_name='weapon')
    hull = ForeignKeyField(Hull, column_name='hull')
    engine = ForeignKeyField(Engine, column_name='engine')


def create_tables():
    with database:
        database.create_tables([Engine, Hull, Weapon, Ship])


def get_rand_attr_value():
    return randint(1, 20)


def fill_the_tables(db):
    with db:
        for i in range(1, 6):
            hull_name = f"Hull-{i}"
            Hull.create(
                hull=hull_name,
                armor=get_rand_attr_value(),
                type=get_rand_attr_value(),
                capacity=get_rand_attr_value()
            )
        for i in range(1, 7):
            engine_name = f"Engine-{i}"
            Engine.create(
                engine=engine_name,
                power=get_rand_attr_value(),
                type=get_rand_attr_value()
            )
        for i in range(1, 21):
            weapon_name = f"Weapon-{i}"
            Weapon.create(
                weapon=weapon_name,
                reload_speed=get_rand_attr_value(),
                rotation_speed=get_rand_attr_value(),
                diameter=get_rand_attr_value(),
                power_volley=get_rand_attr_value(),
                count=get_rand_attr_value()
            )
        for i in range(1, 201):
            ship_name = f"Ship-{i}"
            ship_rand_weapon = f"Weapon-{randint(1, 20)}"
            ship_rand_hull = f"Hull-{randint(1, 5)}"
            ship_rand_engine = f"Engine-{randint(1, 6)}"
            Ship.create(
                ship=ship_name,
                weapon=ship_rand_weapon,
                hull=ship_rand_hull,
                engine=ship_rand_engine
            )


def randomize_db(db):
    with db:
        for ship in Ship.select():
            comp_dict = {
                "Weapon": randint(1, 20),
                "Hull": randint(1, 5),
                "Engine": randint(1, 6)
            }
            comp, comp_rand_int = choice(list(comp_dict.items()))
            new_comp = f"{comp}-{str(comp_rand_int)}"
            if comp == 'Hull':
                ship.update(hull=new_comp).where(Ship.ship == ship).execute()
            elif comp == 'Weapon':
                ship.update(weapon=new_comp).where(Ship.ship == ship).execute()
            elif comp == 'Engine':
                ship.update(engine=new_comp).where(Ship.ship == ship).execute()

        for weapon in Weapon.select():
            param_list = [
                "reload_speed",
                "rotation_speed",
                "diameter",
                "power_volley",
                "count"
            ]
            param = choice(param_list)
            param_value = get_rand_attr_value()
            if param == 'reload_speed':
                weapon.update(reload_speed=param_value).where(Weapon.weapon == weapon).execute()
            elif param == 'rotation_speed':
                weapon.update(rotation_speed=param_value).where(Weapon.weapon == weapon).execute()
            elif param == 'diameter':
                weapon.update(diameter=param_value).where(Weapon.weapon == weapon).execute()
            elif param == 'power_volley':
                weapon.update(power_volley=param_value).where(Weapon.weapon == weapon).execute()
            elif param == 'count':
                weapon.update(count=param_value).where(Weapon.weapon == weapon).execute()

        for hull in Hull.select():
            param_list = [
                "armor",
                "type",
                "capacity"
            ]
            param = choice(param_list)
            param_value = get_rand_attr_value()
            if param == 'armor':
                hull.update(armor=param_value).where(Hull.hull == hull).execute()
            elif param == 'type':
                hull.update(type=param_value).where(Hull.hull == hull).execute()
            elif param == 'capacity':
                hull.update(capacity=param_value).where(Hull.hull == hull).execute()

        for engine in Engine.select():
            param_list = [
                "power",
                "type"
            ]
            param = choice(param_list)
            param_value = f"{randint(1, 20)}"
            if param == 'power':
                engine.update(power=param_value).where(Engine.engine == engine).execute()
            elif param == 'type':
                engine.update(type=param_value).where(Engine.engine == engine).execute()


def get_comp(i, comp):
    if comp == 'Hull':
        return Ship.get(Ship.ship == 'Ship-' + str(i)).hull
    elif comp == 'Weapon':
        return Ship.get(Ship.ship == 'Ship-' + str(i)).weapon
    elif comp == 'Engine':
        return Ship.get(Ship.ship == 'Ship-' + str(i)).engine


def get_comp_params(comp):
    comp = str(comp)
    if 'Hull' in comp:
        return Hull.get(Hull.hull == comp)
    elif 'Weapon' in comp:
        return Weapon.get(Weapon.weapon == comp)
    elif 'Engine' in comp:
        return Engine.get(Engine.engine == comp)


def models_params_equality(a, b):
    for field in a._meta.sorted_fields:
        first_comp = getattr(a, field.name)
        second_comp = getattr(b, field.name)
        if first_comp != second_comp and field.name not in ['hull', 'weapon', 'engine']:
            return False
    return True


def get_differed_fields(first, second):
    result = {}
    for field in first._meta.sorted_fields:
        first_comp = getattr(first, field.name)
        second_comp = getattr(second, field.name)
        if first_comp != second_comp and field.name not in ['hull', 'weapon', 'engine']:
            result[field.name] = [first_comp, second_comp]
    return result


if __name__ == '__main__':
    database.create_tables([Ship, Hull, Weapon, Engine])
    fill_the_tables(database)
