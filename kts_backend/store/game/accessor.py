from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete, insert, func

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.game.model import (
    Player,
    PlayerModel,
    Game,
    GameModel,
    GameData,
    GameDataModel,
    PlayerGameModel,
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
            is_winner=player_model.is_winner,
        )

    @staticmethod
    def player_model_list2player_list(
        player_model_list: List[PlayerModel],
    ) -> List[Player]:
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
        game_model: GameModel,
        player_list: Optional[List[Player] | List[PlayerModel]] = None,
    ) -> Game:
        """
        Convert GameModel object to Game
        :param game_model: GameModel
        :param player_list: List[Player] | List[PlayerModel]
        :return: Game
        """
        if player_list is None:
            player_list = []

        if len(player_list) != 0 and type(player_list[0]) is PlayerModel:
            player_list = GameAccessor.player_model_list2player_list(
                player_model_list=player_list
            )

        return Game(
            game_id=game_model.game_id,
            game_data_id=game_model.game_data_id,
            created_at=game_model.created_at,
            finished_at=game_model.finished_at,
            chat_id=game_model.chat_id,
            player_list=player_list,
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
            answer=game_data_model.answer,
        )

    @staticmethod
    def game_data_model_list2game_data_list(
        game_data_model_list: List[GameDataModel],
    ) -> List[GameData]:
        """
        Convert list of GameDataModel objects to list of GameData objects
        :param game_data_model_list: List[GameDataModel]
        :return: List[GameData]
        """
        return [
            GameAccessor.game_data_model2game_data(
                game_data_model=game_data_model
            )
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

    async def get_player(
        self, player_id: List[int] | int
    ) -> List[Player] | Player:
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
            player_model: Optional[PlayerModel] = await session.get(
                PlayerModel, player_id
            )

            return self.player_model2player(player_model=player_model)

    async def get_player_list(self, player_id_list: List[int]) -> List[Player]:
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

    async def create_player(
        self, player: List[Player] | Player
    ) -> List[Player] | Player:
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
                self.player2dict(player=player),
            )
            player_model: Optional[PlayerModel] = res.scalar()
            await session.commit()

            return self.player_model2player(player_model=player_model)

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
                self.player_list2dict_list(player_list=player_list),
            )
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

            return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def update_player(
        self, player: List[Player] | Player
    ) -> List[Player] | Player:
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
                self.player2dict(player=player),
            )
            player_model: Optional[PlayerModel] = res.scalar()
            await session.commit()

            return self.player_model2player(player_model=player_model)

    async def update_player_list(
        self, player_list: List[Player]
    ) -> List[Player]:
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
                self.player_list2dict_list(player_list=player_list),
            )
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            await session.commit()

            return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def delete_player(
        self, player_id: List[int] | int
    ) -> List[Player] | Player:
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
            player_model: Optional[PlayerModel] = await session.get(
                PlayerModel, player_id
            )
            if player_model:
                await session.delete(player_model)

            return self.player_model2player(player_model=player_model)

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

    async def get_game(self, game_id: int) -> Game | None:
        """
        Get game object from database,
        otherwise return None
        :param game_id: int
        :return: Game
        """
        async with self.app.database.session.begin() as session:
            game_model: Optional[GameModel] = await session.get(
                GameModel, game_id
            )
            if game_model is None:
                return None
        player_list = await self.get_players_from_game(
            game_id=game_model.game_id
        )
        return self.game_model2game(
            game_model=game_model, player_list=player_list
        )

    async def get_game_by_date(self, created_at: datetime) -> Game | None:
        """
        Get game object from database by date column,
        otherwise return None
        :param created_at: datetime
        :return: Game | None
        """
        statement = select(GameModel).filter_by(created_at=created_at)
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game: Optional[GameModel] = res.scalar()

        player_list = await self.get_players_from_game(game_id=game.game_id)
        return self.game_model2game(game_model=game, player_list=player_list)

    async def create_game(self, game_data_id: int, chat_id: int) -> Game:
        """
        Create Game object without players
        :param game_data_id: int
        :param chat_id: int
        :return: Game
        """
        statement = (
            insert(GameModel)
            .values(game_data_id=game_data_id, chat_id=chat_id)
            .returning(GameModel)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game: Optional[GameModel] = res.scalar()
        return self.game_model2game(game_model=game)

    async def create_game_with_players(
        self, game_data_id: int, chat_id: int, player_list: List[Player]
    ) -> Game:
        """
        Create Game object with players (Player objects)
        :param game_data_id: int
        :param chat_id: int
        :param player_list: List[Player]
        :return: Game
        """
        game: Game = await self.create_game(
            game_data_id=game_data_id, chat_id=chat_id
        )
        created_player_list: List[Player] = await self.create_player_list(
            player_list=player_list
        )
        game.player_list = created_player_list

        statement = insert(PlayerGameModel)

        params = [
            {"game_id": game.game_id, "player_id": player.player_id}
            for player in created_player_list
        ]
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement, params)
            game: Optional[GameModel] = res.scalar()

        return game

    async def get_players_by_chat_id(self, chat_id: int) -> List[Player] | None:
        """
        Get list of Player objects from database by chat_id,
        otherwise return None
        :param chat_id: int
        :return: List[Player] | None
        """
        statement = (
            select(PlayerModel)
            .join(PlayerGameModel)
            .join(GameModel)
            .where(GameModel.chat_id == chat_id)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_list: Optional[List[PlayerModel]] = res.scalars()

            if player_model_list is None:
                return None
            return self.player_model_list2player_list(
                player_model_list=player_model_list
            )

    async def get_players_from_game(self, game_id: int) -> List[Player] | None:
        """
        Get list of player objects from database by game_id
        :param game_id: int
        :return: List[Player] | None
        """
        statement = (
            select(PlayerModel).join(PlayerGameModel).filter_by(game_id=game_id)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_list: Optional[List[PlayerModel]] = res.scalars()
            if player_model_list is None:
                return None
        return self.player_model_list2player_list(
            player_model_list=player_model_list
        )

    async def get_last_game(self, chat_id: int) -> Game | None:
        """
        Get last Game object from database by chat_id
        :return:
        """
        subquery = select(func.max(GameModel.created_at)).filter_by(
            chat_id=chat_id
        )
        statement = select(GameModel).where(GameModel.created_at.in_(subquery))

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game: Optional[GameModel] = res.scalar()

            return await self.get_game_by_date(created_at=game.created_at)

    async def create_game_data(self, question: str, answer: str) -> GameData:
        """
        Create new GameData object in database,
        otherwise return the existed one
        :param question: str
        :param answer: str
        :return: GameData
        """
        statement = (
            insert(GameDataModel)
            .values(question=question, answer=answer)
            .returning(GameDataModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_data_model: GameDataModel = res.scalar()

            return self.game_data_model2game_data(
                game_data_model=game_data_model
            )

    async def get_game_data_by_question(
        self, question: str, answer: str
    ) -> GameData:
        """
        Create new GameData object in database,
        otherwise return the existed one
        :param question: str
        :param answer: str
        :return: GameData
        """
        statement = (
            insert(GameDataModel)
            .values(question=question, answer=answer)
            .returning(GameDataModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_data_model: GameDataModel = res.scalar()

            return self.game_data_model2game_data(
                game_data_model=game_data_model
            )

    async def get_game_data_list(self) -> List[GameData] | None:
        """
        Get list of all GameData objects from database,
        otherwise return None
        :return: List[GameData] | None
        """

        statement = select(GameDataModel)

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_data_model_list: Optional[List[GameDataModel]] = res.scalars()

            return self.game_data_model_list2game_data_list(
                game_data_model_list=game_data_model_list
            )

    async def get_unfinished_game_list(self) -> List[Game] | None:
        """
        Get all unfinished games from database,
        otherwise return None
        :return: List[Game] | None
        """
        statement = select(GameModel).filter_by(finished_at=None)

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_model_list: Optional[List[GameModel]] = res.scalars()
            if game_model_list is None:
                return None

            game_list = []
            for game_model in game_model_list:
                player_list = await self.get_players_from_game(
                    game_id=game_model.g
                )
                game_list.append(
                    self.game_model2game(
                        game_model=game_model, player_list=player_list
                    )
                )
            return game_list

    # async def set_game_winner(self, game_id, vk_id: int):
    #     async with self.app.database.session.begin() as session:
    #         _ = await (
    #             session.query(PlayerGameModel)
    #             .filter(
    #                 PlayerGameModel.game_id == game_id,
    #                 PlayerGameModel.vk_id == vk_id,
    #             )
    #             .update({"is_winner": True})
    #         )
    #         _ = await (
    #             session.query(PlayerGameModel)
    #             .filter(
    #                 PlayerGameModel.game_id == game_id,
    #                 PlayerGameModel.vk_id != vk_id,
    #             )
    #             .update({"is_winner": False})
    #         )
    #         await session.commit()
