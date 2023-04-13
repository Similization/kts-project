## Google docs
> Here is a [link](https://docs.google.com/document/d/1jAkiMhfxjpW21ChR5jEwwarMe_4wiXl7D3sfKwBMOmY/edit?usp=sharing) to google docs file
## API
> Here is a [link](https://app.swaggerhub.com/apis/Similization/vk-bot/0.0.1#/) to swagger
```json
{
  "swagger": "2.0",
  "info": {
    "version": "0.0.1",
    "title": "Vk Bot"
  },
  "paths": {
    "/user.get": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserId"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/User"
            }
          }
        }
      }
    },
    "/user.create": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserFullCreate"
            }
          }
        ],
        "responses": {
          "201": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/User"
            }
          }
        }
      }
    },
    "/user.update": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserFullUpdate"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/User"
            }
          }
        }
      }
    },
    "/user.delete": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserId"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/User"
            }
          }
        }
      }
    },
    "/user.get_many": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserIdList"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/UserMany"
            }
          }
        }
      }
    },
    "/user.create_many": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserFullListCreate"
            }
          }
        ],
        "responses": {
          "201": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/UserMany"
            }
          }
        }
      }
    },
    "/user.update_many": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserFullListUpdate"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/UserMany"
            }
          }
        }
      }
    },
    "/user.delete_many": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/UserIdList"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/UserMany"
            }
          }
        }
      }
    },
    "/game_data.post": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/GameData"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/GameData"
            }
          }
        }
      }
    },
    "/game_data.get": {
      "get": {
        "parameters": [],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/GameDataList"
            }
          }
        }
      }
    },
    "/admin.login": {
      "post": {
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "required": false,
            "schema": {
              "$ref": "#/definitions/Admin"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/Admin"
            }
          }
        }
      }
    },
    "/admin.current": {
      "get": {
        "parameters": [],
        "responses": {
          "200": {
            "description": "",
            "schema": {
              "$ref": "#/definitions/Admin"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "UserId": {
      "type": "object",
      "required": [
        "id"
      ],
      "properties": {
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "User ID"
        }
      }
    },
    "User": {
      "type": "object",
      "required": [
        "id"
      ],
      "properties": {
        "vk_id": {
          "type": "integer",
          "format": "int32",
          "description": "VK ID of user"
        },
        "name": {
          "type": "string",
          "description": "First name of user"
        },
        "last_name": {
          "type": "string",
          "description": "Last name of user"
        },
        "username": {
          "type": "string",
          "description": "Username of user"
        },
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "User ID"
        }
      }
    },
    "UserCreate": {
      "type": "object",
      "required": [
        "last_name",
        "name",
        "username",
        "vk_id"
      ],
      "properties": {
        "vk_id": {
          "type": "integer",
          "format": "int32",
          "description": "VK ID of user"
        },
        "username": {
          "type": "string",
          "description": "Username of user"
        },
        "name": {
          "type": "string",
          "description": "First name of user"
        },
        "last_name": {
          "type": "string",
          "description": "Last name of user"
        }
      }
    },
    "UserFullCreate": {
      "type": "object",
      "required": [
        "user"
      ],
      "properties": {
        "user": {
          "$ref": "#/definitions/UserFullCreate_user"
        }
      }
    },
    "UserUpdate": {
      "type": "object",
      "required": [
        "id",
        "last_name",
        "name",
        "username",
        "vk_id"
      ],
      "properties": {
        "vk_id": {
          "type": "integer",
          "format": "int32",
          "description": "New VK ID of user"
        },
        "name": {
          "type": "string",
          "description": "New first name of user"
        },
        "last_name": {
          "type": "string",
          "description": "New last name of user"
        },
        "username": {
          "type": "string",
          "description": "New username of user"
        },
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "ID of user to be updated"
        }
      }
    },
    "UserFullUpdate": {
      "type": "object",
      "required": [
        "user"
      ],
      "properties": {
        "user": {
          "$ref": "#/definitions/UserFullUpdate_user"
        }
      }
    },
    "UserIdList": {
      "type": "object",
      "required": [
        "user_id_list"
      ],
      "properties": {
        "user_id_list": {
          "type": "array",
          "description": "List of User IDs",
          "items": {
            "type": "integer",
            "format": "int32"
          }
        }
      }
    },
    "UserMany": {
      "type": "object",
      "required": [
        "id"
      ],
      "properties": {
        "user_list": {
          "type": "array",
          "description": "List of users' details",
          "items": {
            "$ref": "#/definitions/User"
          }
        },
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "User ID"
        }
      }
    },
    "UserFullListCreate": {
      "type": "object",
      "required": [
        "user_list"
      ],
      "properties": {
        "user_list": {
          "type": "array",
          "description": "List of details of users to be created",
          "items": {
            "$ref": "#/definitions/UserCreate"
          }
        }
      }
    },
    "UserFullListUpdate": {
      "type": "object",
      "required": [
        "user_list"
      ],
      "properties": {
        "user_list": {
          "type": "array",
          "description": "List of details of users to be updated",
          "items": {
            "$ref": "#/definitions/UserUpdate"
          }
        }
      }
    },
    "GameData": {
      "type": "object",
      "required": [
        "answer",
        "question"
      ],
      "properties": {
        "question": {
          "type": "string",
          "description": "The question associated with the game data."
        },
        "answer": {
          "type": "string",
          "description": "The answer associated with the game data."
        },
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "The ID of the game data."
        }
      }
    },
    "GameDataList": {
      "type": "object",
      "properties": {
        "game_data_list": {
          "type": "array",
          "description": "A list of game data objects.",
          "items": {
            "$ref": "#/definitions/GameData"
          }
        }
      }
    },
    "Admin": {
      "type": "object",
      "required": [
        "email",
        "password"
      ],
      "properties": {
        "email": {
          "type": "string",
          "format": "email",
          "description": "The email associated with the Admin (required, maximum length 60 characters).",
          "maxLength": 60
        },
        "password": {
          "type": "string",
          "description": "The password associated with the Admin (required, load only)."
        },
        "user_id": {
          "type": "integer",
          "format": "int32",
          "description": "The ID of the user associated with the Admin."
        },
        "id": {
          "type": "integer",
          "format": "int32",
          "description": "The ID of the Admin."
        }
      }
    },
    "UserFullCreate_user": {
      "type": "object",
      "description": "Details of user to be created"
    },
    "UserFullUpdate_user": {
      "type": "object",
      "description": "Details of user to be updated"
    }
  }
}
```
## Docker image
> Here is a [link](https://hub.docker.com/repository/docker/similization/vk-bot-pole-chudes/general) to docker image
## How to use Vk bot
Before start:
* All messages are ignored and bot sends information about how to start a game
* Min player count is 3
* Max player count is 5
* Message __Создай игру для: @vk_id1, @vk_id2, vk_id3__ - creates game for users, send table with score, question and hided answer like ******

In game:
* Check whose turn now, if this user is not in game, or it is not his turn - sends an appropriate message
* If user guess a letter - check if this letter wasn't guess before, and it contains in the answer word, if guess is correct - generate random points count from 10 to 50 and sends an appropriate message, otherwise turn goes to the next player
* If user guess a word - compares word with answer, if guess is correct - player wins and game finishes, and if not - player kicked from game, bot also sends an appropriate message
* If this is the last player - he has only 1 attempt to guess the answer (he has to write full answer word)
### Contacts
> **Email:** borbri228@gmail.com\
> **Full name:** Bakhlanov Daniil\
> **Telegram:** @Similization
