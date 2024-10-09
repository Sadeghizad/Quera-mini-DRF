# Video Streaming Platform with Real-Time Features

Welcome to the **Video Streaming Platform**! This project lets users stream videos, comment on them, and manage watch lists. We’ve added some cool features like real-time comment updates using WebSockets, and admins can manage everything from the videos to user subscriptions.

---

## Main Features:

- **User Accounts**: Custom user registration and login system.
- **Payments**: Users can subscribe to different plans and handle payments seamlessly.
- **Watch Lists**: Users can create and manage their own personalized watch lists.
- **Comments**: Leave comments on videos, and they’ll show up instantly thanks to real-time updates.
- **Admin Controls**: Admins can manage videos, genres, actors, and user interactions.
- **Real-Time Updates**: Comments appear live on the video page as soon as someone posts them!

---

## How to Get Started:

### 1. Clone the Project

Start by cloning the project to your local machine:

```bash
git clone https://github.com/your-username/video-streaming-platform.git
cd video-streaming-platform
```

### 2. Set Up a Virtual Environment

You’ll need a Python virtual environment for this project. Here’s how to set one up:

```bash
python3 -m venv env
source env/bin/activate  # If you're on Windows, use `env\Scripts\activate`
```

### 3. Install the Dependencies

Once the virtual environment is running, install all the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Redis for Real-Time Features

For real-time updates, you’ll need Redis running in the background. You can either run Redis via Docker or install it locally:

**Option 1: Run Redis with Docker**:
```bash
docker run -p 6379:6379 -d redis
```

**Option 2: Start Redis Locally**:
```bash
redis-server
```

### 5. Apply Migrations and Create an Admin Account

To get the database ready, apply the migrations, and create a superuser to manage the admin tasks:

```bash
python manage.py migrate
python manage.py createsuperuser  # Follow the prompts to create an admin user
```

### 6. Run the Django Server

Now that everything is set up, you can run the development server:

```bash
python manage.py runserver
```

### 7. Enjoy Real-Time Comments with WebSockets

The app already supports WebSockets, so when users post comments, they’ll instantly appear for everyone without refreshing the page. Just make sure Redis is running, and everything will work like magic.

---

## How the Real-Time Comments Work

We use **WebSockets** for live updates. So when a user posts a comment on a video, it’s instantly broadcast to everyone watching the video.

Here’s a sample WebSocket connection you can use in your frontend:

```javascript
const socket = new WebSocket('ws://127.0.0.1:8000/comments/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const comment = data.comment;
    console.log("New comment: ", comment);
};
```

---

## API Overview

You can use **Bruno**, **Postman**, or **Swagger** to test the API. Here are some of the important endpoints:

### 1. **Authentication**:
- **Register**: `POST /auth/registration/`
- **Login**: `POST /auth/login/`

### 2. **Payment**:
- **Initiate Payment**: `POST /payment/initiate/`
- **Payment Callback**: `POST /payment/callback/`
- **Payment History**: `GET /payment/history/`

### 3. **Watch Lists**:
- **Create a Watch List**: `POST /watchLists/`
- **View Watch List**: `GET /watchLists/`

### 4. **Comments**:
- **Add a Comment**: `POST /comments/?video_id={video_id}`
- **View Comments for a Video**: `GET /comments/?video_id={video_id}`

---

## Environment Variables

To keep your sensitive data safe, you can store them in a `.env` file. Here's an example:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

REDIS_URL=redis://127.0.0.1:6379/1
```

---

## Running the Project with Docker (Optional)

If you prefer using Docker, the project is already Docker-ready. Simply build and run the containers using:

```bash
docker-compose up --build
```

---

## Testing the API

Use **Bruno**, **Postman**, or any API testing tool to test the endpoints. Here's an example of how to log in:

**Login Example**:

- **Method**: `POST`
- **URL**: `/auth/login/`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

---

## License

This project is open-source and available under the MIT License.

---

## Contributing

We’d love your help! If you find any issues or want to contribute, feel free to create a pull request or open an issue. Let's make this platform even better together.

---

## Final Words

Thanks for checking out the project! We hope you find it useful. If you have any questions or run into any issues, feel free to reach out!

---
