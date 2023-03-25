from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete, insert, func, and_

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.game.model import (
    Player, PlayerModel,
    Game, GameModel,
    GameData, GameDataModel,
    PlayerGame, PlayerGameModel
)


class GameAccessor(BaseAccessor):
    @staticmethod
    def player_model2player(player_model: PlayerModel) -> Player:
        """
        Convert PlayerModel object to Player object
        :param player_model: PlayerModel
        :return: Player
        """
        return Player(
            player_id=player_model.player_id,
            user_id=player_model.user_id,
            score=player_model.score,
            in_game=player_model.in_game,
            is_winner=player_model.is_winner
        )

    @staticmethod
    def player_model_list2player_list(player_model_list: List[PlayerModel]) -> List[Player]:
        """
        Convert list of PlayerModel objects to list of Player objects
        :param player_model_list: List[PlayerModel])
        :return: List[Player]
        """
        return [
            GameAccessor.player_model2player(player_model=player_model)
            for player_model in player_model_list
        ]

    @staticmethod
    def game_model2game(
            game_model: GameModel, players: List[Player] | List[PlayerModel]
    ) -> Game:
        """
        Convert GameModel object to Game
        :param game_model: GameModel
        :param players: List[Player] | List[PlayerModel]
        :return: Game
        """
        if len(players) != 0 and type(players[0]) is PlayerModel:
            players = GameAccessor.player_model_list2player_list(
                player_model_list=players
            )

        return Game(
            game_id=game_model.game_id,
            game_data_id=game_model.game_data_id,
            created_at=game_model.created_at,
            chat_id=game_model.chat_id,
            players=players
        )

    @staticmethod
    def game_data_model2game_data(game_data_model: GameDataModel) -> GameData:
        """
        Convert GameDataModel object to GameData
        :param game_data_model: GameDataModel
        :return: GameData
        """
        return GameData(
            game_data_id=game_data_model.game_data_id,
            question=game_data_model.question,
            answer=game_data_model.answer
        )

    @staticmethod
    def game_data_model_list2game_data_list(
            game_data_model_list: List[GameDataModel]
    ) -> List[GameData]:
        """
        Convert list of GameDataModel objects to list of GameData objects
        :param game_data_model_list: List[GameDataModel]
        :return: List[GameData]
        """
        return [
            GameAccessor.game_data_model2game_data(game_data_model=game_data_model)
            for game_data_model in game_data_model_list
        ]

    @staticmethod
    def player2dict(player: Player) -> dict:
        """
        Convert Player object to dictionary
        :param player:
        :return:
        """
        return player.__dict__

    @staticmethod
    def player_list2dict_list(player_list: List[Player]) -> List[dict]:
        """
        Convert list of Player objects to list of dictionaries
        :param player_list: List[Player]
        :return: List[dict]
        """
        return [player.__dict__ for player in player_list]

    async def get_player(self, player_id: List[int] | int) -> List[Player] | Player:
        """
        Get player objects from database
        :param player_id: List[int] | int
        :return: List[Player] | Player
        """
        if type(player_id) is int:
            return await self.get_one_player(player_id=player_id)
        if type(player_id) is list:
            return await self.get_player_list(player_id_list=player_id)

    async def get_one_player(self, player_id: int) -> Player:
        """
        Get Player object from database
        :param player_id: int
        :return: Player
        """
        async with self.app.database.session.begin() as session:
            player_model = await session.query(PlayerModel).get(player_id)

            return self.player_model2player(
                player_model=player_model
            )

    async def get_player_list(
            self, player_id_list: List[int]
    ) -> List[Player]:
        """
        Get list of players from database
        :param player_id_list: List[int]
        :return: List[Player]
        """
        # TODO: var 1
        # player_list: List[Player] = []
        # for player_id in player_id_list:
        #     player_list.append(await self.get_one_player(player_id=player_id))
        # return player_list
        # TODO: var 2
        statement = (
            select(PlayerModel)
            .where(PlayerModel.player_id.in_(player_id_list))
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

        return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def create_player(self, player: List[Player] | Player) -> List[Player] | Player:
        """
        Create player objects in database
        :param player: List[Player] | Player
        :return: List[Player] | Player
        """
        if type(player) is Player:
            return await self.create_one_player(player=player)
        if type(player) is list:
            return await self.create_player_list(player_list=player)

    async def create_one_player(self, player: Player) -> Player:
        """
        Create Player object in database
        :param player: Player
        :return: Player
        """
        async with self.app.database.session.begin() as session:
            res = await session.execute(
                insert(PlayerModel).returning(PlayerModel),
                self.player2dict(player=player)
            )
            player_model: Optional[PlayerModel] = res.scalar()
            await session.commit()

            return self.player_model2player(
                player_model=player_model
            )

    async def create_player_list(
            self, player_list: List[Player]
    ) -> List[Player]:
        """
        Create list of players in database
        :param player_list: List[Player]
        :return: List[Player]
        """
        # TODO: var 1
        # created_player_list: List[Player] = []
        # for player in player_list:
        #     created_player_list.append(await self.create_one_player(player=player))
        # return created_player_list
        # TODO: var 2
        async with self.app.database.session.begin() as session:
            res = await session.execute(
                insert(PlayerModel).returning(PlayerModel),
                self.player_list2dict_list(player_list=player_list)
            )
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

            return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def update_player(self, player: List[Player] | Player) -> List[Player] | Player:
        """
        Update player objects in database
        :param player: List[Player] | Player
        :return: List[Player] | Player
        """
        if type(player) is Player:
            return await self.update_one_player(player=player)
        if type(player) is list:
            return await self.update_player_list(player_list=player)

    async def update_one_player(self, player: Player) -> Player:
        """
        Update Player object in database
        :param player: Player
        :return: Player
        """
        async with self.app.database.session.begin() as session:
            res = await session.execute(
                update(PlayerModel).returning(PlayerModel),
                self.player2dict(player=player)
            )
            player_model: Optional[PlayerModel] = res.scalar()
            await session.commit()

            return self.player_model2player(
                player_model=player_model
            )

    async def update_player_list(self, player_list: List[Player]) -> List[Player]:
        """
        pdate list of players in database
        :param player_list: List[Player]
        :return: List[Player]
        """
        # TODO: var 1
        # updated_player_list: List[Player] = []
        # for player in player_list:
        #     updated_player_list.append(await self.update_one_player(player=player))
        # return updated_player_list
        # TODO: var 2
        async with self.app.database.session.begin() as session:
            res = await session.execute(
                update(PlayerModel).returning(PlayerModel),
                self.player_list2dict_list(player_list=player_list)
            )
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

            return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def delete_player(self, player_id: List[int] | int) -> List[Player] | Player:
        """
        Delete player objects from database
        :param player_id: List[int] | int
        :return: List[Player] | Player
        """
        if type(player_id) is int:
            return await self.delete_one_player(player_id=player_id)
        if type(player_id) is list:
            return await self.delete_player_list(player_id_list=player_id)

    async def delete_one_player(self, player_id: int) -> Player:
        """
        Create Player object in database
        :param player_id: int
        :return: Player
        """
        async with self.app.database.session.begin() as session:
            player_model: Optional[PlayerModel] = await session.query(PlayerModel).get(player_id)
            if player_model:
                await session.delete(player_model)

            return self.player_model2player(
                player_model=player_model
            )

    async def delete_player_list(
            self, player_id_list: List[int]
    ) -> List[Player]:
        """
        Create list of players in database
        :param player_id_list: List[int]
        :return: List[Player]
        """
        # TODO: var 1
        # deleted_player_list: List[Player] = []
        # for player_id in player_id_list:
        #     deleted_player_list.append(await self.delete_one_player(player_id=player_id))
        # return deleted_player_list
        # TODO: var 2
        statement = (
            delete(PlayerModel)
            .where(PlayerModel.player_id.in_(player_id_list))
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

        return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def get_game(self, game_id):
        async with self.app.database.session.begin() as session:
            game: Optional[GameModel] = await session.query(GameModel).get(game_id)

        players = await self.get_players_from_game(game_id=game.game_id)
        return self.game_model2game(game_model=game, players=players)

    async def create_game(
            self, players: List[Player], chat_id: int
    ) -> Game:
        statement = insert(GameModel).values(chat_id=chat_id).returning(GameModel)
        players_id = [{"vk_id": player.vk_id} for player in players]

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game: Optional[GameModel] = res.scalar()
            # await session.commit()

            query = insert(PlayerGameModel).values(
                game_id=game.game_id
            )  # .returning(PlayerGameScoreModel)
            _ = await session.execute(query, players_id)
            # _: Optional[List[PlayerGameScoreModel]] = res.scalars()
            await session.commit()
        return self.game_model2game(game_model=game, players=players)

    async def get_game_by_date(self, created_at: datetime) -> Game | None:
        query = select(GameModel).where(GameModel.created_at == created_at)
        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game: Optional[GameModel] = res.scalar()

        players = await self.get_players_by_game_id(game_id=game.game_id)
        return self.game_model2game(game_model=game, players=players)

    async def get_players_by_chat_id(
            self, chat_id: int
    ) -> List[Player] | None:
        query = (
            select(PlayerModel)
            .join(PlayerGameModel)
            .join(GameModel)
            .where(GameModel.chat_id == chat_id)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            players: Optional[List[PlayerModel]] = res.scalars()

            if players:
                return self.player_model_list2player_list(
                    player_model_list=players
                )
            return None

    async def get_players_from_game(
            self, game_id: int
    ) -> List[Player] | List:
        query = (
            select(PlayerModel)
            .join(PlayerGameModel)
            .where(PlayerGameModel.game_id == game_id)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            players: Optional[List[PlayerModel]] = res.scalars()

        return self.player_model_list2player_list(
            player_model_list=players
        )

    async def get_last_game(self) -> Game | None:
        subquery = select(func.max(GameModel.created_at))
        query = select(GameModel).where(GameModel.created_at.in_(subquery))

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game: Optional[GameModel] = res.scalar()

            return await self.get_game_by_date(created_at=game.created_at)

    async def get_game_data_list(self) -> List[GameData] | None:
        query = select(GameDataModel)

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game_data_list: Optional[List[GameDataModel]] = res.scalars()

            return self.game_data_model_list2game_data_list(game_data_model_list=game_data_list)

    async def set_game_winner(self, game_id, vk_id: int):
        async with self.app.database.session.begin() as session:
            _ = await (
                session.query(PlayerGameModel)
                .filter(
                    PlayerGameModel.game_id == game_id,
                    PlayerGameModel.vk_id == vk_id
                )
                .update({'is_winner': True})
            )
            _ = await (
                session.query(PlayerGameModel)
                .filter(
                    PlayerGameModel.game_id == game_id,
                    PlayerGameModel.vk_id != vk_id
                )
                .update({'is_winner': False})
            )
            await session.commit()
