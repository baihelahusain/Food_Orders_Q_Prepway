from django import forms 
from .models import Item, Order

class ItemForm(forms.ModelForm):
    Item_name = forms.CharField(
        label="Item Name",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter item name',
            'autofocus': True
        }),
        help_text="Enter the name of your food item"
    )
    
    Item_desc = forms.CharField(
        label="Description",
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your food item',
            'rows': 3
        }),
        help_text="Provide a detailed description of the item"
    )
    
    Item_price = forms.IntegerField(
        label="Price (₹)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter price',
            'min': 0
        }),
        help_text="Enter the price in rupees (whole numbers only)"
    )
    
    Item_img = forms.CharField(
        label="Image URL (Optional)",
        max_length=1100,
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter image URL'
        }),
        help_text="Paste a URL to an image of your food item (leave empty to use uploaded image or default)"
    )
    
    item_image = forms.ImageField(
        label="Upload Image (Optional)",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text="Upload an image of your food item from your device"
    )
    
    prep_time = forms.CharField(
        label="Preparation Time",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 30 minutes, 2 hours'
        }),
        help_text="Enter the time needed to prepare this item"
    )
    
    category = forms.ChoiceField(
        label="Food Category",
        choices=Item.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select the category this food item belongs to"
    )
    
    class Meta:
        model = Item
        fields = ['Item_name', 'Item_desc', 'Item_price', 'Item_img', 'item_image', 'prep_time', 'category']
    
    def clean_Item_price(self):
        price = self.cleaned_data.get('Item_price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price

class CheckoutForm(forms.ModelForm):
    contact_number = forms.CharField(
        label="Contact Number",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your contact number',
            'required': True
        }),
        help_text="Please provide a valid contact number"
    )
    
    delivery_location = forms.CharField(
        label="Delivery Location",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your delivery address',
            'rows': 3,
            'required': True
        }),
        help_text="Enter your complete delivery address"
    )
    
    class Meta:
        model = Order
        fields = ['contact_number', 'delivery_location']