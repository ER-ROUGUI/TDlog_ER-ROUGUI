from dao.game_dao import GameDao
from model.player import Player
from model.battlefield import Battlefield
from model.game import Game
from model.vessel import Vessel
class GameService:
    def __init__(self):
       self.game_dao = GameDao()
    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int,
        max_y: int, min_z: int, max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)
    def join_game(self, game_id: int, player_name: str) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        if len(game.players) >= 2:
            return False
        min_x, max_x, min_y, max_y, min_z, max_z = game.players[0].battlefield.get_boundaries()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        self.game_dao.update_game(game)
        return True
    def get_game(self, game_id: int) -> Game:
        return self.game_dao.find_game(game_id)
    def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        player = None
        for p in game.players:
            if p.name == player_name:
                player = p
                break
        if player is None:
            return False
        if not player.battlefield.add_vessel(Vessel(vessel_type, x, y, z)):
            return False
        self.game_dao.update_game(game)
        return True
    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        shooter = None
        target = None
        for player in game.players:
            if player.name == shooter_name:
                shooter = player
            for vessel in player.battlefield.vessels:
                if vessel.id == vessel_id:
                    target = vessel
            if shooter is not None and target is not None:
                break
        if shooter is None or target is None:
            return False
        if shooter.battlefield.shoot_at(target, x, y, z):
            self.game_dao.update_game(game)
            return True
        return False
    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return "Game not found"
        shooter = None
        for p in game.players:
            if p.name == shooter_name:
                shooter = p
                break
        if shooter is None:
            return "Player not found"
        if len(game.players[0].battlefield.vessels) == 0:
            return "GAGNE" if shooter == game.players[0] else "PERDU"
        if len(game.players[1].battlefield.vessels) == 0:
            return "GAGNE" if shooter == game.players[1] else "PERDU"
        return "ENCOURS"
