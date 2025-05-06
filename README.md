# Food Orders App

A comprehensive food ordering platform built with Django, featuring real-time delivery tracking, order management, and a beautiful UI.

## Features

- **User Authentication**: Secure login/signup with profile management
- **Food Catalog**: Browse items by category with detailed descriptions and images
- **Shopping Cart**: Add items, adjust quantities, and checkout seamlessly
- **Order Management**: Track orders in real-time with status updates
- **Delivery Tracking**: Map integration with estimated delivery time
- **Admin Panel**: Manage items, orders, and user accounts
- **Mobile Responsive**: Works beautifully on all devices

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Bootstrap 5, JavaScript
- **Maps**: Google Maps JavaScript API
- **Deployment**: Render

## Deployment to Render and Supabase

### 1. Set up Supabase

1. Create a Supabase account at [supabase.com](https://supabase.com)
2. Create a new project and note your project URL and API key
3. Run the schema creation script to set up tables:

```bash
python supabase_setup.py > supabase_schema.sql
```

4. Copy the output SQL and execute it in the Supabase SQL Editor

### 2. Configure Environment Variables

Create a `.env` file using the example template:

```bash
cp .env.example .env
```

Update with your Supabase credentials:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-api-key
```

### 3. Deploy to Render

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Log in to [Render](https://render.com)
3. Create a new Web Service and connect to your Git repository
4. Configure the following settings:
   - **Name**: food-orders-app
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash bash.sh`
5. Add environment variables from your `.env` file
6. Deploy!

### 4. Using the Render Blueprint (Alternative)

Instead of manual configuration, you can use the provided `render.yaml` blueprint:

1. Fork this repository
2. Log in to Render and navigate to "Blueprints"
3. Create a new blueprint using your forked repository
4. Render will automatically set up your services as defined in `render.yaml`

## Local Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/food-orders-app.git
cd food-orders-app
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your environment variables:

```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

5. Visit `http://localhost:8000` in your browser

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Django secret key | Yes |
| DEBUG | Debug mode (True/False) | Yes |
| ALLOWED_HOSTS | Comma-separated list of hosts | Yes |
| DATABASE_URL | Database connection URL | Yes |
| SUPABASE_URL | Supabase project URL | Yes |
| SUPABASE_KEY | Supabase API key | Yes |
| AWS_ACCESS_KEY_ID | AWS S3 key (for media storage) | No |
| AWS_SECRET_ACCESS_KEY | AWS S3 secret | No |
| AWS_STORAGE_BUCKET_NAME | AWS S3 bucket name | No |

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

### Link:

https://food-orders-q-prepway.onrender.com/
