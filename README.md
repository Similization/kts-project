## Google docs
> Here is a [link](https://docs.google.com/document/d/1jAkiMhfxjpW21ChR5jEwwarMe_4wiXl7D3sfKwBMOmY/edit?usp=sharing) to google docs file
## API
> Here is a [link](https://app.swaggerhub.com/apis/Similization/vk-bot/0.0.1#/) to swagger
## Docker image
> Here is a [link](https://hub.docker.com/repository/docker/similization/vk-bot-pole-chudes/general) to docker image
## How to use Vk bot
__Before start:__
* All messages are ignored and bot sends information about how to start a game
* Min player count is 3
* Max player count is 5
* Message ___Создай игру для: @vk_id1, @vk_id2, vk_id3___ - creates game for users, send table with score, question and hided answer like ******

__In game:__
* Check whose turn now, if this user is not in game, or it is not his turn - sends an appropriate message
* If user guess a letter - check if this letter wasn't guess before, and it contains in the answer word, if guess is correct - generate random points count from 10 to 50 and sends an appropriate message, otherwise turn goes to the next player
* If user guess a word - compares word with answer, if guess is correct - player wins and game finishes, and if not - player kicked from game, bot also sends an appropriate message
* If this is the last player - he has only 1 attempt to guess the answer (he has to write full answer word)
## Presentation
> Here is a [link](https://docs.google.com/presentation/d/1Z4C8RqC34IJR_X_S4vHcrCYZtlRFfyqMrNrFXJnQBLk/edit?usp=sharing) to presentation
### Contacts
> **Email:** borbri228@gmail.com\
> **Full name:** Bakhlanov Daniil\
> **Telegram:** @Similization
