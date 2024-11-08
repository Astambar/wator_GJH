
from Test_Standard import TestRunner
from ToolsWorld import ToolsWorld
from world import World
from shark import Shark
from fish import Fish
class ToolsTest:
    def __init__(self):
        self.result = None

    def is_eq(self, arg1, arg2):
        return arg1 == arg2

    def is_eqs(self, *args):
        if len(args) < 2:
            raise ValueError("Le nombre d'arguments doit être au moins 2")
        return all(self.is_eq(args[i], args[i + 1]) for i in range(len(args) - 1))


class TestWorld:
    def __init__(self):
        self.name = "TestWorld"
        self.world = None
        self.tools = ToolsWorld()
        self.tool_test = ToolsTest()

    def test_create_world_with_required_params(self):
        # Test avec paramètres obligatoires et facultatifs personnalisés
        self.world = self.tools.create_world(
            3, 3,
            row=5,
            column=5
        )
        return isinstance(self.world, World)

    def test_create_world_with_defaults(self):
        # Test avec seulement les paramètres obligatoires, vérification des valeurs par défaut
        self.world = self.tools.create_world(5, 10)
        return isinstance(self.world, World) and \
               self.tool_test.is_eqs(self.world.row, self.tools.default_params["row"]) and \
               self.tool_test.is_eqs(self.world.columns, self.tools.default_params["columns"])

    def test_create_world_missing_required(self):
        try:
            self.world = self.tools.create_world(number_sharks=5)  # Manque number_fish
        except TypeError:
            return True
        return False

    def test_place_animal(self):
        world = self.tools.create_world(4,4,row=5,columns=5)
        world = self.tools.place_animals(world)
        return (self.tools.len_list_fishes(world) > 0) and (self.tools.len_list_sharks(world) > 0)

    def test_fidelity_fishes_grid_and_list(self):
        world = self.tools.create_world(4,4,row=5,columns=5)
        world = self.tools.place_animals(world)
        return self.tools.is_eq_list_fishes_and_list_grid_fishes(world)

    def test_fidelity_sharks_grid_and_list(self):
        world = self.tools.create_world(4,4,row=5,columns=5)
        world = self.tools.place_animals(world)
        return self.tools.is_eq_list_sharks_and_list_grid_sharks(world)

    def test_conformity_grid_and_list(self):
        world = self.tools.create_world(4,4,row=5,columns=5)
        world = self.tools.place_animals(world)
        return self.tools.is_conform_grid_and_list_animals(world)

    def test_number_less_than_or_equal_to_the_size_of_the_grid(self):
        world = self.tools.create_world(10,10,row=5,columns=4)
        return self.tools.number_less_than_or_equal_to_the_size_of_the_grid(world)
    def test_move_fish_mature(self):
        world = self.tools.create_world(1,0,row=2,columns=2)
        world = self.tools.place_animals(world)
        return self.tools.check_fish_mature_move(world)
    def test_move_sharks_mature(self):
        world = self.tools.create_world(0,1,row=2,columns=2)
        world = self.tools.place_animals(world)
        return self.tools.check_shark_mature_move(world)
    def test_not_move_baby_fish(self):
        world = self.tools.create_world(1,0,row=2,columns=2)
        world = self.tools.place_animals(world)
        return self.tools.check_fish_not_mature_not_move(world)
    def test_not_move_baby_sharks(self):
        world = self.tools.create_world(0,1,row=2,columns=2)
        world = self.tools.place_animals(world)
        return self.tools.check_shark_not_mature_not_move(world)
    





    
if __name__ == '__main__':
    Test = TestRunner([TestWorld])
    Test.run()

