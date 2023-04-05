from kts_backend.game.dataclasses import GameFull, Game
from kts_backend.store import Store
from kts_backend.store.game.game import PoleChuDesGame


class TestHandleUpdates:
    async def test_no_messages(self, store):
        await store.bots_manager.handle_updates(updates=[])
        assert store.vk_api.send_message.called is False

    async def test_unfinished_game_start(self, store: Store, game_2: Game):
        bot_manager = store.bots_manager
        assert len(bot_manager.game_list) == 1
        assert isinstance(bot_manager.game_list[0], GameFull)

    async def test_finished_game_start(self, store: Store, game_3: Game):
        bot_manager = store.bots_manager
        assert len(bot_manager.game_list) == 0

    async def test_get_game_by_chat_id(self, store: Store, game_3: Game):
        bot_manager = store.bots_manager
        full_game = store.game.get_full_game(game_id=game_3.id)
        pole_game = await PoleChuDesGame(app=store.bots_manager.app).init_from(game=full_game)
        assert await bot_manager.get_game_by_chat_id("2") == pole_game
