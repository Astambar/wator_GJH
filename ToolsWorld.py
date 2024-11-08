from world import World
from fish import Fish
from shark import Shark
from pool import Grid
import copy
class ToolsWorld:
    def __init__(self):
        self.name = "ToolsWorld"
        # Valeurs par défaut pour les paramètres facultatifs
        self.default_params = {
            "row": 3,
            "columns": 3
        }

    def create_world(self, number_fish:int, number_sharks:int, **kwargs) -> World:
        """Crée une instance de World en s'assurant que les paramètres obligatoires sont fournis.
        
        Args:
            number_fish (int): Nombre de poissons initial.
            number_sharks (int): Nombre de requins initial.
            kwargs: Autres arguments facultatifs, avec des valeurs par défaut pour ceux non fournis.
        
        Returns:
            World: Une instance de la classe World initialisée.
        
        Raises:
            ValueError: Si les paramètres obligatoires ne sont pas fournis.
        """
        # Vérification des paramètres obligatoires
        if number_fish is None or number_sharks is None:
            raise ValueError("Les paramètres 'number_fish' et 'number_sharks' sont obligatoires.")

        # Mise à jour des paramètres facultatifs avec les valeurs passées dans kwargs
        params = {**self.default_params, **kwargs}
        
        # Création de l'instance de World avec les paramètres requis et facultatifs
        return World(
            initial_fish_number=number_fish,
            initial_shark_number=number_sharks,
            row=params["row"],
            columns=params["columns"],
        )
    
    def place_animals(self,world:World) -> World:
        world.initial_animal_placing()
        world_copy = copy.deepcopy(world)
        return world_copy
    def area(self,world:World) -> int:
        return world.row * world.columns
    def sum_shark_and_fish(self,world:World) -> int:
        return world.initial_fish_number + world.initial_shark_number
    
    def number_less_than_or_equal_to_the_size_of_the_grid(self,world:World) -> bool:
        return self.sum_shark_and_fish(world) <= self.area(world)
    def get_grid(self,world:World) -> Grid:
        return world.grid
    def get_grid_pool(self, world:World) -> list:
        if world.grid is None:
            raise ValueError("Le monde n'a pas été correctement initialisé : l'attribut 'grid' est None.")
        return self.get_grid(world).pool
    def get_grid_get_value(self,world:World,position:tuple) -> int|object|None:
        return self.get_grid(world).get_value(position)
    def search_grid(self,world:World,focus:int|object)-> list[int|object]:
        list_focus = []
        if not isinstance(focus,object):
            for row in self.get_grid_pool(world):
                for col in row:
                    if col == 0:
                        list_focus.append(0)
                    else:
                        ValueError("Valeur étrangére non prévu")
        else:
            for row in self.get_grid_pool(world):
                for col in row:
                    if type(col) == focus:  # noqa: E721
                        list_focus.append(col)
        return list_focus
    def number_sharks_in_grid(self,world:World) -> int:
        return len(self.search_grid(world, Shark))
    def number_fishes_in_grid(self,world: World) -> int:
        return len(self.search_grid(world, Fish))
    
    def get_list_sharks(self, world:World) -> list[Shark]:
        return world.list_sharks
    def get_list_fishes(self, world: World) -> list[Fish]:
        return world.list_fishes
    
    def len_list_sharks(self,world: World) -> int:
        return len(self.get_list_sharks(world))
    def len_list_fishes(self,world: World) -> int:
        return len(self.get_list_fishes(world))
    
    def get_first_shark(self,world:World) -> Shark:
        return self.get_list_sharks(world)[0]
    
    def get_first_fish(self,world:World) -> Fish:
        return self.get_list_fishes(world)[0]
    def get_chronon_animal(self,animal:object) -> int:
        return animal.get_chronon()

    def is_len_zero_fishes(self,world: World) -> bool:
        return (self.len_list_fishes(world) == 0)
    def is_len_zero_sharks(self, world: World) -> bool:
        return (self.len_list_sharks(world) == 0)
    
    def is_eq_list_sharks_and_list_grid_sharks(self,world: World) -> bool:
        return (self.number_sharks_in_grid(world) == self.len_list_sharks(world))
    def is_eq_list_fishes_and_list_grid_fishes(self,world: World) -> bool:
        return self.number_fishes_in_grid(world) == self.len_list_fishes(world)
    def is_conform_grid_and_list_animals(self,world: World) -> bool:
        return self.is_eq_list_fishes_and_list_grid_fishes(world) and self.is_eq_list_sharks_and_list_grid_sharks(world)

    def get_pos_animal(self,animal:object) -> tuple:
        return animal.get_position()
    def get_box_around(self,world:World, position:tuple):
        print(f"{world.surrounding_scan(position)=}")
        return world.surrounding_scan(position)
    def scan_box_around_animal(self,world: World,animal:object):
        return self.get_box_around(world,self.get_pos_animal(animal))
    def move_animal(self, world: World, animal:object) -> World:
        world_copy = copy.deepcopy(world)  # Crée une copie indépendante
        world_copy.move_and_reproduction(animal)
        return world_copy

    def move_multiple_animals(self,world: World,list_animals:list[object]):
        for animal in list_animals:
            world_copy = self.move_animal(world,animal)
        return world_copy
    def move_first_shark(self,world: World) -> World:
        world_copy = self.move_animal(world,self.get_first_shark(world))
        return world_copy
    def move_first_fish(self,world: World) -> World:
        world_copy = self.move_animal(world,self.get_first_fish(world))
        return world_copy
    def is_mature_animal(self,animal:object) -> bool:
        return (self.get_chronon_animal(animal) > 0)
    def is_not_mature_animal(self,animal:object)  -> bool:
        return (not self.is_mature_animal(animal))
    
    def convert_mature_animal(self, animal:object) -> object:
        if not self.is_mature_animal(animal):
            animal.chronon_increment() # Augmente le chronon si l'animal n'est pas mature
        return animal  # Retourne l'animal sans faire de copie
    def verifier_deplacement_animal(self, world: World, animal: object, attendu_deplacement=True) -> dict:
        """
        Vérifie le déplacement de l'animal et l'intégrité de sa position dans la grille.

        Args:
            world (World): Le monde dans lequel l'animal se déplace.
            animal (object): L'animal à déplacer.
            attendu_deplacement (bool): Si True, on s'attend à ce que l'animal bouge.

        Returns:
            dict: Contient les informations suivantes :
                - positions (tuple): Position de départ et d'arrivée.
                - fidele_debut (bool): Si l'animal était bien à sa position de départ dans la grille.
                - fidele_fin (bool): Si l'animal est bien à sa position de fin dans la grille.
                - deplacement_reussi (bool): Si le déplacement correspond à ce qui était attendu.
        """
        # Enregistre la position initiale de l'animal
        pos_debut = self.get_pos_animal(animal)
        fidele_debut = (self.get_grid_get_value(world,pos_debut) == animal)

        # Effectue le mouvement de l'animal
        self.move_animal(world, animal)

        # Enregistre la position finale de l'animal
        pos_fin = self.get_pos_animal(animal)
        fidele_fin = (self.get_grid_get_value(world,pos_fin) == animal)

        # Vérifie si le déplacement a eu lieu
        deplacement_effectue = (pos_debut != pos_fin)

        # Détermine si le résultat du déplacement correspond à l'attente
        deplacement_reussi = (deplacement_effectue == attendu_deplacement)

        # Retourne les informations sous forme de dictionnaire
        return {
            "positions": (pos_debut, pos_fin),
            "fidele_debut": fidele_debut,
            "fidele_fin": fidele_fin,
            "deplacement_reussi": deplacement_reussi
        }

    def check_animal_move(self, world: World,animal:object,attendue_deplacement=True) -> bool:
        # Compare si la position a changé
        move_animal_result = self.verifier_deplacement_animal(world,animal,attendue_deplacement)
        if move_animal_result["fidele_debut"] == False:
            ValueError("probléme de synchronisation entre la grille et l'animal avant le move")
        if move_animal_result["fidele_fin"] == False:
            ValueError("probléme de synchronisation entre la grille et l'animal après le move")
        
        return move_animal_result["deplacement_reussi"]
    def check_animal_not_move(self, world: World,animal) -> bool:
        return self.check_animal_move(world,animal,attendue_deplacement=False)
    def check_animal_mature_move(self, world: World,animal:object) -> bool:
        animal_copy = self.convert_mature_animal(animal)
        return self.check_animal_move(world,animal_copy)
    def check_animal_not_mature_not_move(self, world: World,animal) -> bool:
        return self.check_animal_not_move(world,animal)

    def check_shark_mature_move(self, world: World) -> bool:
        return self.check_animal_mature_move(world,self.get_first_shark(world))

    def check_fish_mature_move(self, world: World) -> bool:
        return self.check_animal_mature_move(world,self.get_first_fish(world))
    

    def check_shark_not_mature_not_move(self, world: World) -> bool:
        return self.check_animal_not_mature_not_move(world,self.get_first_shark(world))

    def check_fish_not_mature_not_move(self, world: World) -> bool:
        return self.check_animal_not_mature_not_move(world,self.get_first_fish(world))

if __name__ == "__main__":
    tools = ToolsWorld()
    new_world = tools.create_world(3,3)
    new_world.grid.print_grid()
    new_world = tools.place_animals(new_world)
    print("")
    new_world.grid.print_grid()