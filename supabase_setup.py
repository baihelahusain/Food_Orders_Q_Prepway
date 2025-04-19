#!/usr/bin/env python

"""
Supabase Schema Creation Script for Food Orders App

This script generates SQL statements to create tables in Supabase based on
the Django models. Run this script to get the SQL you'll need to execute
in the Supabase SQL Editor.

Usage:
    python supabase_setup.py
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodsite.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from food.models import Item, Cart, Order, OrderItem

def generate_create_table_sql():
    """Generate SQL to create tables in Supabase"""
    print("-- SQL to create tables in Supabase SQL Editor")
    print("\n-- Users Table")
    print("""
CREATE TABLE auth.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Enable Row Level Security
ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

-- User Profiles
CREATE TABLE public.user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth.users(id) ON DELETE CASCADE,
    location TEXT,
    image VARCHAR(1000)
);

-- Enable Row Level Security
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
    """)

    print("\n-- Items Table")
    print("""
CREATE TABLE public.items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(200) NOT NULL,
    item_desc TEXT,
    item_price INTEGER NOT NULL,
    item_img VARCHAR(1100) DEFAULT 'https://cdn-icons-png.flaticon.com/512/1377/1377194.png',
    item_image TEXT,
    category VARCHAR(20) DEFAULT 'fast_food',
    prep_time VARCHAR(50)
);

-- Enable Row Level Security
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;
    """)

    print("\n-- Cart Table")
    print("""
CREATE TABLE public.cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth.users(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES public.items(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE public.cart ENABLE ROW LEVEL SECURITY;
    """)

    print("\n-- Orders Table")
    print("""
CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth.users(id) ON DELETE CASCADE,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    contact_number VARCHAR(15),
    delivery_location TEXT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    estimated_delivery_time INTEGER,
    timer_start TIMESTAMP WITH TIME ZONE
);

-- Enable Row Level Security
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
    """)

    print("\n-- Order Items Table")
    print("""
CREATE TABLE public.order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES public.orders(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES public.items(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    price DECIMAL(10,2) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE public.order_items ENABLE ROW LEVEL SECURITY;
    """)

    print("\n-- Row Level Security Policies")
    print("""
-- Users can read their own data
CREATE POLICY "Users can view own data" 
ON auth.users FOR SELECT 
USING (auth.uid() = id);

-- Only authenticated users can insert into cart
CREATE POLICY "Authenticated users can add to cart" 
ON public.cart FOR INSERT 
TO authenticated 
USING (auth.uid() = user_id);

-- Users can only view their own cart
CREATE POLICY "Users can view own cart" 
ON public.cart FOR SELECT 
USING (auth.uid() = user_id);

-- Users can only update their own cart
CREATE POLICY "Users can update own cart" 
ON public.cart FOR UPDATE 
USING (auth.uid() = user_id);

-- Users can only delete their own cart items
CREATE POLICY "Users can delete own cart items" 
ON public.cart FOR DELETE 
USING (auth.uid() = user_id);

-- Anyone can view items
CREATE POLICY "Anyone can view items" 
ON public.items FOR SELECT 
TO anon, authenticated 
USING (true);

-- Only admins can insert, update, delete items
CREATE POLICY "Admins can manage items" 
ON public.items FOR ALL 
TO authenticated 
USING (EXISTS (SELECT 1 FROM auth.users WHERE auth.uid() = id AND is_superuser = true));

-- Users can view own orders
CREATE POLICY "Users can view own orders" 
ON public.orders FOR SELECT 
USING (auth.uid() = user_id);

-- Authenticated users can create orders
CREATE POLICY "Authenticated users can create orders" 
ON public.orders FOR INSERT 
TO authenticated 
USING (auth.uid() = user_id);

-- Admins can view all orders
CREATE POLICY "Admins can view all orders" 
ON public.orders FOR SELECT 
TO authenticated 
USING (EXISTS (SELECT 1 FROM auth.users WHERE auth.uid() = id AND is_superuser = true));

-- Admins can update orders
CREATE POLICY "Admins can update orders" 
ON public.orders FOR UPDATE 
TO authenticated 
USING (EXISTS (SELECT 1 FROM auth.users WHERE auth.uid() = id AND is_superuser = true));
    """)

    print("\n-- Sample Category Data")
    print("""
-- Insert sample categories
INSERT INTO public.items (item_name, item_desc, item_price, category, prep_time) 
VALUES 
('French Fries', 'Crispy golden fries served with ketchup and mayo.', 99, 'fast_food', '15 minutes'),
('Chicken Nuggets', 'Crispy chicken nuggets served with dipping sauce.', 149, 'fast_food', '10 minutes'),
('Chicken Biryani', 'Fragrant basmati rice cooked with tender chicken pieces and aromatic spices.', 249, 'main_course', '40 minutes'),
('Mango Lassi', 'Refreshing yogurt-based drink with sweet mango pulp.', 89, 'drinks', '5 minutes'),
('Gulab Jamun', 'Soft, spongy milk-solid-based sweet soaked in sugar syrup.', 99, 'sweet', '25 minutes');
    """)

if __name__ == "__main__":
    generate_create_table_sql() 