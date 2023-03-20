from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, insert, func

from kts_backend.base.base_accessor import BaseAccessor
from kts_backend.game.model import (
    PlayerDC,
    PlayerModel,
    PlayerGameScoreModel,
    GameModel,
    GameDC,
)


class GameAccessor(BaseAccessor):
    @staticmethod
    def convert_player_model_list_to_dc_list(
        player_model_list: List[PlayerModel],
    ):
        return [
            GameAccessor.convert_player_model_to_dc(player_model=player_model)
            for player_model in player_model_list
        ]

    @staticmethod
    def convert_player_model_to_dc(player_model: PlayerModel) -> PlayerDC:
        return PlayerDC(
            vk_id=player_model.vk_id,
            name=player_model.name,
            last_name=player_model.last_name,
        )

    @staticmethod
    def convert_game_model_to_dc(
        game_model: GameModel, players: List[PlayerDC] | List[PlayerModel]
    ) -> GameDC:
        if len(players) != 0 and type(players[0]) is PlayerModel:
            players = GameAccessor.convert_player_model_list_to_dc_list(
                player_model_list=players
            )
        return GameDC(
            game_id=game_model.game_id,
            created_at=game_model.created_at,
            chat_id=game_model.chat_id,
            players=players,
        )

    async def get_players_by_chat_id(
        self, chat_id: int
    ) -> List[PlayerDC] | None:
        query = (
            select(PlayerModel)
            .join(PlayerGameScoreModel)
            .join(GameModel)
            .where(GameModel.chat_id == chat_id)
        )

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            players: Optional[List[PlayerModel]] = res.scalars()

            if players:
                return self.convert_player_model_list_to_dc_list(
                    player_model_list=players
                )
            return None

    async def create_new_game(
        self, players: List[PlayerDC], chat_id: int
    ) -> GameDC:
        query = insert(GameModel).values(chat_id=chat_id).returning(GameModel)
        players_id = [{"vk_id": player.vk_id} for player in players]

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game: Optional[GameModel] = res.scalar()
            # await session.commit()

            query = insert(PlayerGameScoreModel).values(
                game_id=game.game_id
            )  # .returning(PlayerGameScoreModel)
            _ = await session.execute(query, players_id)
            # _: Optional[List[PlayerGameScoreModel]] = res.scalars()
            await session.commit()
        return self.convert_game_model_to_dc(game_model=game, players=players)

    async def get_game_by_date(self, created_at: datetime) -> GameDC | None:
        query = select(GameModel).where(GameModel.created_at == created_at)
        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game: Optional[GameModel] = res.scalar()

        players = await self.get_players_by_game_id(game_id=game.game_id)
        return self.convert_game_model_to_dc(game_model=game, players=players)

    async def get_players_by_game_id(
        self, game_id: int
    ) -> List[PlayerDC] | List:
        query = (
            select(PlayerModel)
            .join(PlayerGameScoreModel)
            .where(PlayerGameScoreModel.game_id == game_id)
        )
        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            players: Optional[List[PlayerModel]] = res.scalars()

        return self.convert_player_model_list_to_dc_list(
            player_model_list=players
        )

    async def get_last_game(self) -> GameDC | None:
        subquery = select(func.max(GameModel.created_at))
        query = select(GameModel).where(GameModel.created_at.in_(subquery))

        async with self.app.database.session.begin() as session:
            res = await session.execute(query)
            game: Optional[GameModel] = res.scalar()

            return await self.get_game_by_date(created_at=game.created_at)
