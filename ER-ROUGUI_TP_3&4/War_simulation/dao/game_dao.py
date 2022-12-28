from sqlalchemy import create_engine , Column, Integer , String ,ForeignKey ,select

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , relationship


engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class GameEntity(Base):
 __tablename__ = 'game'
 id = Column(Integer, primary_key=True)
 players = relationship("PlayerEntity", back_populates="game",
 cascade="all, delete-orphan")

class PlayerEntity(Base):
 __tablename__ = 'player'
 id = Column(Integer, primary_key=True)
 name = Column(String, nullable=False)
 game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
 game = relationship("GameEntity", back_populates="players")
 battle_field = relationship("BattlefieldEntity",
 back_populates="player",
 uselist=False, cascade="all, delete-orphan")

 class BattlefieldEntity(Base):
    __tablename__ = 'Battelfeild'
    id = Column(Integer,primary_key = True)
    min_x = Column(Integer )
    min_y = Column(Integer)
    min_z = Column(Integer )
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    max_power = Column(Integer , nullinteger = False)

class VesselEntity(Base):
    __tablename__ = 'VesselEntity'
    coord_x = Column(Integer , primary_key = True)
    coord_y =Column(Integer)
    coord_z = Column (Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(String)
    battle_field_id = Column(Integer , ForeignKey('Weapon.id'),nullInt = False)
    def map_to_game(game_entity: GameEntity) -> Game:
    game = Game(
        id=game_entity.id,
        name=game_entity.name,
        release_date=game_entity.release_date,
        publisher=game_entity.publisher,
        platform=game_entity.platform
    )
    return game


def map_to_game_entity(game: Game) -> GameEntity:
    game_entity = GameEntity(
        id=game.id,
        name=game.name,
        release_date=game.release_date,
        publisher=game.publisher,
        platform=game.platform
    )
    return game_entity

def map_to_player_entity(player: Player) -> PlayerEntity:
    player_entity = PlayerEntity(
        id=player.id,
        name=player.name,
        game_id=player.game.id
    )
    return player_entity

def map_to_vessel_entity(vessel: Vessel) -> VesselEntity:
    vessel_entity = VesselEntity(
        id=vessel.id,
        type=vessel.type,
        battlefield_id=vessel.battlefield.id
    )
    return vessel_entity

class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()
    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id
    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)


#cree et mettre PlayerEntity et VesselEntity-----------------------

def create_player(self, player: Player) -> int:
    player_entity = map_to_player_entity(player)
    self.db_session.add(player_entity)
    self.db_session.commit()
    return player_entity.id

def update_player(self, player: Player) -> None:
    player_entity = map_to_player_entity(player)
    self.db_session.merge(player_entity)
    self.db_session.commit()

def create_vessel(self, vessel: Vessel) -> int:
    vessel_entity = map_to_vessel_entity(vessel)
    self.db_session.add(vessel_entity)
    self.db_session.commit()
    return vessel_entity.id

def update_vessel(self, vessel: Vessel) -> None:
    vessel_entity = map_to_vessel_entity(vessel)
    self.db_session.merge(vessel_entity)
    self.db_session.commit()
#----------------------------------------------------------------
