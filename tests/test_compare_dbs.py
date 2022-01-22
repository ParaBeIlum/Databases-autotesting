from models.db_model import *
import pytest

MODELS = [Ship, Hull, Weapon, Engine]


def idfn(val):
    res = f"Ship-{val}"
    return res


@pytest.mark.parametrize('comp', ['Weapon', 'Hull', 'Engine'])
@pytest.mark.parametrize('i', [i for i in range(1, 201)], ids=idfn)
class TestCompareDBs:
    def test_comp(self, i, comp, prepare_db_for_compare):
        with database.bind_ctx(MODELS):
            original_comp = get_comp(i, comp)
        with database_for_compare.bind_ctx(MODELS):
            randomized_comp = get_comp(i, comp)

        comp_differ_message = f"Ship-{i}, {randomized_comp}\n" \
                              f"expected {original_comp}," \
                              f" was {randomized_comp}"
        assert str(original_comp) == str(randomized_comp), comp_differ_message

        differed_fields = get_differed_fields(original_comp, randomized_comp)

        start_param_differ_message = f"Ship-{i}, {original_comp}\n"
        differ_params_enumeration = ""
        for param, values in differed_fields.items():
            differ_params_enumeration += f"{param}: expected {values[0]}, was {values[1]}\n"
        assert models_params_equality(original_comp, randomized_comp), \
            start_param_differ_message + differ_params_enumeration
