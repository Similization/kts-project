class TestHandleUpdates:
    async def test_no_messages(self, store):
        """
        :param store:
        :return:
        """
        await store.bots_manager.handle_updates(updates=[])
        assert store.vk_api.send_message.called is False
