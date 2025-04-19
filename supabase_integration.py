"""
Supabase Integration for Django Food Orders App

This module provides helper functions to interact with Supabase 
from Django. It's designed to be imported and used in your views or models.
"""

import os
import requests
import json
from django.conf import settings

class SupabaseClient:
    """
    A simple Supabase client for Django integration.
    
    This is a lightweight wrapper around the Supabase REST API
    for use with Django. For more complex usage, consider using
    the official supabase-py package.
    """
    
    def __init__(self, url=None, key=None):
        """Initialize with Supabase URL and API key."""
        self.url = url or settings.SUPABASE_URL
        self.key = key or settings.SUPABASE_KEY
        
        # Check if URL and key are set
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be provided either directly or in settings.")
        
        # Set up base headers for requests
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
    
    def _build_url(self, table, path=""):
        """Build the full Supabase REST URL for a table."""
        return f"{self.url}/rest/v1/{table}{path}"
    
    def select(self, table, columns="*", filters=None):
        """
        Select data from a table.
        
        Args:
            table (str): Table name
            columns (str): Columns to select, default is "*"
            filters (dict): Optional query filters
            
        Returns:
            list: List of records matching the query
        """
        url = self._build_url(table)
        params = {"select": columns}
        
        # Add filters if provided
        if filters:
            for key, value in filters.items():
                params[key] = value
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def insert(self, table, data):
        """
        Insert data into a table.
        
        Args:
            table (str): Table name
            data (dict or list): Data to insert (single record or list of records)
            
        Returns:
            dict: The inserted record(s)
        """
        url = self._build_url(table)
        
        # Ensure data is a list for consistency
        if not isinstance(data, list):
            data = [data]
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            response.raise_for_status()
    
    def update(self, table, data, filters):
        """
        Update data in a table.
        
        Args:
            table (str): Table name
            data (dict): Data to update
            filters (dict): Filters to identify records to update
            
        Returns:
            dict: The updated record(s)
        """
        url = self._build_url(table)
        params = filters or {}
        
        # Add special header for updates
        headers = self.headers.copy()
        headers["Prefer"] = "return=representation"
        
        response = requests.patch(url, headers=headers, json=data, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def delete(self, table, filters):
        """
        Delete data from a table.
        
        Args:
            table (str): Table name
            filters (dict): Filters to identify records to delete
            
        Returns:
            dict: The deleted record(s) if available
        """
        url = self._build_url(table)
        params = filters or {}
        
        # Add special header for deletes
        headers = self.headers.copy()
        headers["Prefer"] = "return=representation"
        
        response = requests.delete(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 204:
            return {"success": True}
        else:
            response.raise_for_status()
    
    def execute_sql(self, sql, params=None):
        """
        Execute raw SQL against the Supabase database.
        
        This requires the pg_execute function to be exposed in your Supabase project.
        
        Args:
            sql (str): SQL query to execute
            params (dict): Query parameters
            
        Returns:
            dict: Query result
        """
        url = f"{self.url}/rest/v1/rpc/execute_sql"
        data = {
            "query": sql,
            "params": params or {}
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


# Helper functions to use in Django views

def get_supabase_client():
    """Get a configured Supabase client."""
    return SupabaseClient()

def fetch_menu_items(category=None):
    """
    Fetch menu items, optionally filtered by category.
    
    Args:
        category (str, optional): Category to filter by
        
    Returns:
        list: List of menu items
    """
    client = get_supabase_client()
    
    if category:
        return client.select("items", filters={"category": f"eq.{category}"})
    else:
        return client.select("items")

def get_user_cart(user_id):
    """
    Get cart items for a user.
    
    Args:
        user_id (int): User ID
        
    Returns:
        list: Cart items with product details
    """
    client = get_supabase_client()
    
    # Join cart with items table to get full item details
    query = """
    SELECT c.id, c.quantity, c.created_at, 
           i.id as item_id, i.item_name, i.item_price, i.item_img, i.prep_time
    FROM cart c
    JOIN items i ON c.item_id = i.id
    WHERE c.user_id = $1
    """
    
    return client.execute_sql(query, {"user_id": user_id})

def create_order(user_id, total_price, cart_items, contact_number=None, 
                 delivery_location=None, latitude=None, longitude=None):
    """
    Create a new order from cart items.
    
    Args:
        user_id (int): User ID
        total_price (float): Total price of the order
        cart_items (list): List of cart items
        contact_number (str, optional): Contact number
        delivery_location (str, optional): Delivery location
        latitude (float, optional): Latitude coordinate
        longitude (float, optional): Longitude coordinate
        
    Returns:
        dict: Created order
    """
    client = get_supabase_client()
    
    # Create order
    order_data = {
        "user_id": user_id,
        "total_price": total_price,
        "status": "pending",
        "contact_number": contact_number,
        "delivery_location": delivery_location,
        "latitude": latitude,
        "longitude": longitude
    }
    
    # Remove None values
    order_data = {k: v for k, v in order_data.items() if v is not None}
    
    # Insert order
    order_result = client.insert("orders", order_data)
    order_id = order_result[0]["id"]
    
    # Create order items
    order_items = []
    for cart_item in cart_items:
        order_item = {
            "order_id": order_id,
            "item_id": cart_item["item_id"],
            "quantity": cart_item["quantity"],
            "price": cart_item["price"]
        }
        order_items.append(order_item)
    
    # Insert order items
    client.insert("order_items", order_items)
    
    # Clear cart
    client.delete("cart", {"user_id": f"eq.{user_id}"})
    
    return order_result[0] 