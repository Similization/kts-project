from dataclasses import asdict
from datetime import datetime
from typing import List, Optional, Sequence

from sqlalchemy import select, update, delete, insert, func
from sqlalchemy.orm import joinedload

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.game.model import (
    PlayerModel,
    GameModel,
    GameDataModel,
)
from kts_backend.game.dataclasses import (
    Player,
    Game,
    GameData,
    GameFull,
)
from kts_backend.user.dataclasses import User


class GameAccessor(BaseAccessor):
    @staticmethod
    def player_model2player(player_model: PlayerModel) -> Player:
        """
        Convert PlayerModel object to Player object
        :param player_model: PlayerModel
        :return: Player
        """
        return Player(
            id=player_model.id,
            user_id=player_model.user_id,
            game_id=player_model.game_id,
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
        player_list: List[Player] | List[PlayerModel] | None = None,
    ) -> Game:
        """
        Convert GameModel object to Game
        :param game_model: GameModel
        :param player_list: List[Player] | List[PlayerModel]
        :return: Game
        """
        if player_list is None:
            player_list = []

        if len(player_list) != 0 and isinstance(player_list[0], PlayerModel):
            player_list = GameAccessor.player_model_list2player_list(
                player_model_list=player_list
            )

        return Game(
            id=game_model.id,
            game_data_id=game_model.game_data_id,
            created_at=game_model.created_at,
            finished_at=game_model.finished_at,
            chat_id=game_model.chat_id,
            chat_message_id=game_model.chat_message_id,
            guessed_word=game_model.guessed_word,
            required_player_count=game_model.required_player_count,
            previous_player_id=game_model.previous_player_id,
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
            id=game_data_model.id,
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
    def game_model2game_full(game_model: GameModel) -> GameFull:
        """
        Convert GameModel object to Game
        :param game_model: GameModel
        :return: GameFull
        """
        return GameFull(
            id=game_model.id,
            game_data=game_model.game_data,
            created_at=game_model.created_at,
            finished_at=game_model.finished_at,
            chat_id=game_model.chat_id,
            chat_message_id=game_model.chat_message_id,
            guessed_word=game_model.guessed_word,
            required_player_count=game_model.required_player_count,
            previous_player=game_model.previous_player,
            player_list=game_model.player_list,
        )

    @staticmethod
    def player2dict(player: Player) -> dict:
        """
        Convert Player object to dictionary
        :param player:
        :return:
        """
        return asdict(player)

    @staticmethod
    def player_list2dict_list(player_list: List[Player]) -> List[dict]:
        """
        Convert list of Player objects to list of dictionaries
        :param player_list: List[Player]
        :return: List[dict]
        """
        return [asdict(player) for player in player_list]

    async def get_player(
        self, player_id: List[int] | int
    ) -> List[Player] | Player:
        """
        Get player objects from database
        :param player_id: List[int] | int
        :return: List[Player] | Player
        """
        if isinstance(player_id, int):
            return await self.get_one_player(player_id=player_id)
        if isinstance(player_id, list):
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
            .where(PlayerModel.id.in_(player_id_list))
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)
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
        if isinstance(player, Player):
            return await self.create_one_player(player=player)
        if isinstance(player, list):
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
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)
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
        if isinstance(player, Player):
            return await self.update_one_player(player=player)
        if isinstance(player, list):
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
        Update list of players in database
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
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)
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
        if isinstance(player_id, int):
            return await self.delete_one_player(player_id=player_id)
        if isinstance(player_id, list):
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
            .where(PlayerModel.id.in_(player_id_list))
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)
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
        player_list = await self.get_players_from_game(game_id=game_model.id)
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

        player_list = await self.get_players_from_game(game_id=game.id)
        return self.game_model2game(game_model=game, player_list=player_list)

    async def create_game(
        self,
        game_data_id: int,
        answer: str,
        chat_id: int,
        required_player_count: int = 3,
    ) -> Game:
        """
        Create Game object without players
        :param game_data_id: int
        :param answer: str
        :param chat_id: int
        :param required_player_count: int
        :return: Game
        """
        statement = (
            insert(GameModel)
            .values(
                game_data_id=game_data_id,
                chat_id=chat_id,
                guessed_word="*" * len(answer),
                required_player_count=required_player_count,
            )
            .returning(GameModel)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game: Optional[GameModel] = res.scalar()
        return self.game_model2game(game_model=game)

    async def create_game_with_players(
        self,
        game_data_id: int,
        answer: str,
        chat_id: int,
        player_list: List[Player],
    ) -> Game:
        """
        Create Game object with players (Player objects)
        :param game_data_id: int
        :param answer: str
        :param chat_id: int
        :param player_list: List[Player]
        :return: Game
        """
        created_player_list: List[Player] = await self.create_player_list(
            player_list=player_list
        )

        game: Game = await self.create_game(
            game_data_id=game_data_id,
            answer=answer,
            chat_id=chat_id,
            required_player_count=len(player_list),
        )

        game.player_list = created_player_list

        return game

    async def update_game(self, game: GameFull) -> None:
        """
        Update Game object in database
        :param game: GameFull
        :return: None
        """
        statement = (
            update(GameModel)
            .filter_by(id=game.id)
            .values(
                finished_at=game.finished_at,
                previous_player_id=game.previous_player.id,
            )
        )
        async with self.app.database.session.begin() as session:
            await session.execute(statement=statement)
            await session.commit()

    async def get_players_by_chat_id(self, chat_id: int) -> List[Player] | None:
        """
        Get list of Player objects from database by chat_id,
        otherwise return None
        :param chat_id: int
        :return: List[Player] | None
        """
        statement = (
            select(PlayerModel)
            .join(GameModel)
            .where(GameModel.chat_id == chat_id)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)

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
        statement = select(PlayerModel).filter_by(game_id=game_id)
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model_seq: Sequence[PlayerModel] | None = res.scalars().all()
            player_model_list: List[PlayerModel] = list(player_model_seq)

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

    async def get_game_data(self, game_data_id: int) -> GameData | None:
        """
        Get GameData object by game_data_id from database,
        otherwise return None
        :param game_data_id: int
        :return: GameData | None
        """
        async with self.app.database.session.begin() as session:
            game_data_model: Optional[GameDataModel] = await session.get(
                GameDataModel, game_data_id
            )

            if game_data_model is None:
                return None

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
            game_data_model_seq: Sequence[
                GameDataModel
            ] | None = res.scalars().all()
            game_data_model_list: List[GameDataModel] = list(
                game_data_model_seq
            )

            return self.game_data_model_list2game_data_list(
                game_data_model_list=game_data_model_list
            )

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

    async def get_unfinished_game_list(self) -> List[GameFull] | None:
        """
        Get all unfinished games from database,
        otherwise return None
        :return: List[Game] | None
        """
        statement = (
            select(GameModel)
            .filter_by(finished_at=None)
            .options(
                joinedload(GameModel.previous_player).subqueryload(
                    PlayerModel.user
                )
            )
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_model_list: Sequence[GameModel] | None = res.scalars().all()
            if game_model_list is None:
                return None

            return [
                self.game_model2game_full(game_model=game_model)
                for game_model in game_model_list
            ]

    async def update_player_points(
        self, player_id: int, new_score: int
    ) -> Player:
        """
        Increase player points
        :param player_id: int
        :param new_score: int
        :return: Player
        """
        statement = (
            update(PlayerModel)
            .filter_by(player_id=player_id)
            .values(score=new_score)
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model: PlayerModel | None = res.scalar()

            await session.commit()
        return self.player_model2player(player_model=player_model)

    async def set_game_winner(self, winner_id: int) -> Player:
        """
        Update player in database
        :param winner_id: int
        :return: Player
        """
        statement = (
            update(PlayerModel)
            .filter_by(player_id=winner_id)
            .values(is_winner=True)
            .returning(PlayerModel)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            player_model: PlayerModel | None = res.scalar()

            await session.commit()
        return self.player_model2player(player_model=player_model)

    async def create_player_list_by_user_info(
        self, game_id: int, users_info: List[dict]
    ) -> List[Player]:
        """
        :param game_id:
        :param users_info:
        :return:
        """
        # receive user dict info
        # get user vk_id
        user_vk_id_list = [user_info["vk_id"] for user_info in users_info]
        # get existed user list by vk_id list
        existed_user_list: List[
            User
        ] = await self.app.store.user.get_user_list_by_vk_id_list(
            vk_id_list=user_vk_id_list
        )
        # get existed user vk_id list by vk_id list
        existed_user_vk_id_list: List = [
            existed_user.vk_id for existed_user in existed_user_list
        ]
        # get not existed user dict info
        not_existed_user_info: List = [
            user_info
            for user_info in users_info
            if user_info["vk_id"] not in existed_user_vk_id_list
        ]
        # create such users
        if len(not_existed_user_info) != 0:
            created_user_list: List[
                User
            ] = await self.app.store.user.create_user_list(
                user_list=not_existed_user_info
            )
            # get all users together
            existed_user_list.extend(created_user_list)

        player_list: List[Player] = [
            Player(user_id=user.id, game_id=game_id)
            for user in existed_user_list
        ]
        return await self.create_player_list(player_list=player_list)

    async def get_full_game(self, game_id: int) -> GameFull:
        """
        :param game_id:
        :return:
        """
        statement = (
            select(GameModel)
            .filter_by(id=game_id)
            .options(
                joinedload(GameModel.previous_player).subqueryload(
                    PlayerModel.user
                )
            )
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(statement=statement)
            game_model: GameModel | None = res.scalar()

        return self.game_model2game_full(game_model=game_model)
