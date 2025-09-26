# LingoTrack Backend API Documentation

This document provides an overview of the API endpoints for the LingoTrack backend application.

## Getting Started

### Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   A virtual environment (recommended)

### Installation

1.  Navigate to the `Backend` directory:
    ```bash
    cd Backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv env
    # On Windows:
    .\env\Scripts\activate
    # On macOS/Linux:
    source env/bin/activate
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt # Assuming a requirements.txt exists or you'll create one
    ```
    *(Note: If `requirements.txt` does not exist, you will need to create it by running `pip freeze > requirements.txt` after installing Django, Django REST Framework, PyJWT, and Django CORS Headers.)*

4.  Apply database migrations:
    ```bash
    python backend/manage.py makemigrations
    python backend/manage.py migrate
    ```

5.  Import initial word data (if `english_words_2000.json` is available in the project root):
    ```bash
    python backend/manage.py import_words
    ```

### Running the Server

```bash
python backend/manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/` (or `http://localhost:8000/`).

---

## API Endpoints

All endpoints require an `Authorization` header with a Bearer JWT token for user authentication.

### User Management

#### 1. Create or Update User Profile

Creates a new user profile or updates an existing one based on the `auth0_id` extracted from the JWT token.

*   **URL:** `/users/`
*   **Method:** `POST`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
    *   `Content-Type: application/json`
*   **Request Body:**
    ```json
    {
        "username": "newuser",
        "profile_picture_url": "http://example.com/pic.jpg",
        "current_level": "Beginner",
        "words_know_count": 0,
        "words_learned_count": 0,
        "sentences_correct_count": 0
    }
    ```
    *(Note: `auth0_id` is automatically extracted from the token and should not be sent in the body.)*
*   **Success Response (200 OK):** Returns the created/updated user object.
    ```json
    {
        "id": 1,
        "auth0_id": "auth0|some_id",
        "username": "newuser",
        "profile_picture_url": "http://example.com/pic.jpg",
        "current_level": "Beginner",
        "words_know_count": 0,
        "words_learned_count": 0,
        "sentences_correct_count": 0,
        "created_at": "2025-09-25T10:00:00Z",
        "updated_at": "2025-09-25T10:00:00Z"
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: Invalid token, missing `sub` in token, or invalid data in request body.
    *   `401 Unauthorized`: Invalid or missing token.

#### 2. Get User Profile

Retrieves the profile of the authenticated user.

*   **URL:** `/users/profile/`
*   **Method:** `GET`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
*   **Request Body:** None
*   **Success Response (200 OK):** Returns the user object.
    ```json
    {
        "id": 1,
        "auth0_id": "auth0|some_id",
        "username": "user1",
        "profile_picture_url": "http://example.com/pic1.jpg",
        "current_level": "Beginner",
        "words_know_count": 10,
        "words_learned_count": 5,
        "sentences_correct_count": 20,
        "created_at": "2025-09-20T09:00:00Z",
        "updated_at": "2025-09-25T11:00:00Z"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: Invalid or missing token.
    *   `404 Not Found`: User not found.

#### 3. Get All Users

Retrieves a list of all registered user profiles.

*   **URL:** `/users/all/`
*   **Method:** `GET`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
*   **Request Body:** None
*   **Success Response (200 OK):** Returns a list of user objects.
    ```json
    [
        {
            "id": 1,
            "auth0_id": "auth0|some_id",
            "username": "user1",
            "profile_picture_url": "http://example.com/pic1.jpg",
            "current_level": "Beginner",
            "words_know_count": 10,
            "words_learned_count": 5,
            "sentences_correct_count": 20,
            "created_at": "2025-09-20T09:00:00Z",
            "updated_at": "2025-09-25T11:00:00Z"
        },
        // ... more users
    ]
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: Invalid or missing token.

#### 4. Delete All Users

Deletes all registered user profiles from the database. **Use with caution.**

*   **URL:** `/users/all/delete`
*   **Method:** `DELETE`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
*   **Request Body:** None
*   **Success Response (200 OK):**
    ```json
    {"message": "Todos los usuarios han sido eliminados."}
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: Invalid or missing token.

### Word Management

#### 4. Get Random Unknown Word for User

Retrieves a random word that the authenticated user has not yet marked as 'known' or 'used'.

*   **URL:** `/words/random/`
*   **Method:** `GET`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
*   **Request Body:** None
*   **Success Response (200 OK):**
    ```json
    {
        "id": 123,
        "base": "example",
        "s_form": "examples",
        "past": "exampled",
        "past_participle": "exampled",
        "ing": "exampling",
        "meaning": "ejemplo",
        "example": "This is an example sentence.",
        "translation": "Esta es una oración de ejemplo."
    }
    ```
*   **Success Response (200 OK - All words known):**
    ```json
    {"message": "Congrats, u know all the words"}
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: Invalid or missing token.
    *   `404 Not Found`: User not found.

#### 5. Mark User Word (Known/Used)

Marks a specific word with a given status ('known' or 'used') for the authenticated user. If the word is already marked, its status will be updated.

*   **URL:** `/words/mark/`
*   **Method:** `POST`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
    *   `Content-Type: application/json`
*   **Request Body:**
    ```json
    {
        "word_id": 123,
        "status": "known"  // or "used"
    }
    ```
*   **Success Response (201 Created - New entry):**
    ```json
    {"message": "Palabra 'example' marcada como 'known' para el usuario 'username'"}
    ```
*   **Success Response (200 OK - Status updated):**
    ```json
    {"message": "Estado de la palabra 'example' actualizado a 'used' para el usuario 'username'"}
    ```
*   **Error Responses:**
    *   `400 Bad Request`: Missing `word_id` or `status`, or invalid `status` value.
    *   `401 Unauthorized`: Invalid or missing token.
    *   `404 Not Found`: User or Word not found.

#### 6. Get User's Words by Status

Retrieves a list of words marked by the authenticated user, optionally filtered by status ('known' or 'used'). For each word, it also includes the date it was marked and a list of other users at the same level who also have that word with the same status.

*   **URL:** `/words/my-words/`
*   **Method:** `GET`
*   **Authentication:** Required (Bearer Token)
*   **Headers:**
    *   `Authorization: Bearer <YOUR_AUTH0_JWT_TOKEN>`
*   **Query Parameters (Optional):**
    *   `status`: `known` or `used`. If omitted, returns both 'known' and 'used' words.
*   **Request Body:** None
*   **Success Response (200 OK):**
    ```json
    [
        {
            "word": {
                "id": 123,
                "base": "example",
                "s_form": "examples",
                "past": "exampled",
                "past_participle": "exampled",
                "ing": "exampling",
                "meaning": "ejemplo",
                "example": "This is an example sentence.",
                "translation": "Esta es una oración de ejemplo."
            },
            "status": "known",
            "date_marked": "2025-09-25T10:30:00.123456Z",
            "other_users_same_level_word": [
                {
                    "id": 2,
                    "auth0_id": "auth0|user123",
                    "username": "AnotherUser",
                    "profile_picture_url": "http://example.com/pic.jpg",
                    "current_level": "Beginner",
                    "words_know_count": 50,
                    "words_learned_count": 20,
                    "sentences_correct_count": 100,
                    "created_at": "2025-09-20T09:00:00Z",
                    "updated_at": "2025-09-25T11:00:00Z"
                },
                // ... more users
            ]
        },
        // ... more word entries
    ]
    ```
*   **Error Responses:**
    *   `400 Bad Request`: Invalid `status` query parameter value.
    *   `401 Unauthorized`: Invalid or missing token.
    *   `404 Not Found`: User not found.
