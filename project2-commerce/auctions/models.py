from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import URLField
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Listing(models.Model):
    """
    MENS_APPAREL = "MA"
    MENS_BAGS_AND_ACCESSORIES = "MBA"
    MENS_SHOES = "MS"
    WOMENS_BAGS = "WB"
    WOMENS_ACCESSORIES = "WAC"
    WOMENS_APPAREL = "WAP"
    WOMENS_SHOES = "WS"
    HEALTH_AND_PERSONAL_CARE = "HPC"
    MAKEUP_AND_FRAGRANCES = "MF"
    CAMERAS = "CA"
    MOBILES_AND_GADGETS = "MOG"
    MOBILE_ACCESSORIES = "MOA"
    LAPTOPS_AND_COMPUTERS = "LC"
    AUDIO = "AUD"
    GAMING = "GAM"
    DIGITAL_GOODS_AND_VOUCHERS = "DGV"
    HOME_APPLIANCES = "HA"
    HOME_ENTERTAINMENT = "HE"
    HOME_AND_LIVING = "HL"
    GROCERIES = "GRO"
    BABIES_AND_KIDS = "BK"
    TOYS_GAMES_COLLECTIBLES = "TGC"
    MOTORS = "MO"
    SPORTS_AND_TRAVEL = "ST"
    PET_CARE = "PET"
    OTHERS = "OT"
    """

    MENS_APPAREL = "Men's-Apparel"
    MENS_BAGS_AND_ACCESSORIES = "Men's-Bags-Accessories"
    MENS_SHOES = "Men's-Shoes"
    WOMENS_BAGS = "Women's-Bags"
    WOMENS_ACCESSORIES = "Women's-Accessories"
    WOMENS_APPAREL = "Women's-Apparel"
    WOMENS_SHOES = "Women's-Shoes"
    HEALTH_AND_PERSONAL_CARE = "Health-Personal-Care"
    MAKEUP_AND_FRAGRANCES = "Makeup-Frargances"
    CAMERAS = "Cameras"
    MOBILES_AND_GADGETS = "Mobiles-Gadgets"
    MOBILE_ACCESSORIES = "Mobile-Accessories"
    LAPTOPS_AND_COMPUTERS = "Laptops-Computers"
    AUDIO = "Audio"
    GAMING = "Gaming"
    DIGITAL_GOODS_AND_VOUCHERS = "Digital-Goods-Vouchers"
    HOME_APPLIANCES = "Home-Appliances"
    HOME_ENTERTAINMENT = "Home-Entertainment"
    HOME_AND_LIVING = "Home-Living"
    GROCERIES = "Groceries"
    BABIES_AND_KIDS = "Babies-Kids"
    TOYS_GAMES_COLLECTIBLES = "Toys-Games-Collectibles"
    MOTORS = "Motors"
    SPORTS_AND_TRAVEL = "Sports-Travel"
    PET_CARE = "Pet-Care"
    OTHERS = "Others"
    CATEGORIES_CHOICES = [
        (MENS_APPAREL, "Men's Apparel"),
        (MENS_BAGS_AND_ACCESSORIES, "Men's Bags & Accessories"),
        (MENS_SHOES, "Men's Shoes"),
        (WOMENS_BAGS, "Women's Bags"),
        (WOMENS_ACCESSORIES, "Women's Accessories"),
        (WOMENS_APPAREL, "Women's Apparel"),
        (WOMENS_SHOES, "Women's Shoes"),
        (HEALTH_AND_PERSONAL_CARE, "Health & Personal Care"),
        (MAKEUP_AND_FRAGRANCES, "Makeup & Fragrances"),
        (CAMERAS, "Cameras"),
        (MOBILES_AND_GADGETS, "Mobiles & Gadgets"),
        (MOBILE_ACCESSORIES, "Mobile Accessories"),
        (LAPTOPS_AND_COMPUTERS, "Laptops & Computers"),
        (AUDIO, "Audio"),
        (GAMING, "Gaming"),
        (DIGITAL_GOODS_AND_VOUCHERS, "Digital Goods & Vouchers"),
        (HOME_APPLIANCES, "Home Appliances"),
        (HOME_ENTERTAINMENT, "Home Entertainment"),
        (HOME_AND_LIVING, "Home & Living"),
        (GROCERIES, "Groceries"),
        (BABIES_AND_KIDS, "Babies & Kids"),
        (TOYS_GAMES_COLLECTIBLES, "Toys, Games & Collectibles"),
        (MOTORS, "Motors"),
        (SPORTS_AND_TRAVEL, "Sports & Travel"),
        (PET_CARE, "Pet Care"),
        (OTHERS, "Others"),
    ]
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES)
    image_url = models.URLField(verbose_name="Image URL", blank=True, null=True)
    starting_bid = models.FloatField(
        verbose_name="Starting Bid",
        validators=[
            MinValueValidator(0),
        ],
    )

    def __str__(self):
        return f"{self.title} (id: {self.id})"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user}"


class Bid(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_price = models.FloatField(
        validators=[
            MinValueValidator(0),
        ],
    )

    def __str__(self):
        return f"{self.listing}"


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=1000)
