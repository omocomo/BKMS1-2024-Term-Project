from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    star: int
    long_term_use: bool
    repurchase: bool
    skin_type: str
    skin_concern: str
    irritation_level: str
    cleansing_power: str
    absorption_power: str
    texture_power: str
    review_content: str

class ReviewCreate(ReviewBase):
    product_id: int
    reviewer_id: int

class Review(ReviewBase):
    review_id: int

    class Config:
        orm_mode = True

class ReviewerBase(BaseModel):
    reviewer_name: str
    skin_type_oily: bool
    skin_type_dry: bool
    skin_type_sensitive: bool
    skin_type_combination: bool
    skin_concern_acne: bool
    skin_concern_pigmentation: bool
    skin_concern_blackhead: bool
    skin_concern_redness: bool
    skin_concern_wrinkles_whitening: bool
    cleansing_power_very_satisfied: bool
    cleansing_power_average: bool
    cleansing_power_somewhat_disappointed: bool
    cleansing_power_very_disappointed: bool
    irritation_level_no_irritation: bool
    irritation_level_slight_irritation: bool
    irritation_level_moderate_irritation: bool
    irritation_level_severe_irritation: bool
    absorption_power_very_satisfied: bool
    absorption_power_average: bool
    absorption_power_somewhat_disappointed: bool
    absorption_power_very_disappointed: bool
    texture_power_very_satisfied: bool
    texture_power_average: bool
    texture_power_somewhat_disappointed: bool
    texture_power_very_disappointed: bool

class ReviewerCreate(ReviewerBase):
    pass

class Reviewer(ReviewerBase):
    reviewer_id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    product_name: str
    product_category: str
    brand_name: str
    original_price: int
    final_price: int
    number_of_reviews: int
    review_rating: float
    review_5_star_ratio: float
    review_4_star_ratio: float
    review_3_star_ratio: float
    review_2_star_ratio: float
    review_1_star_ratio: float
    skin_type_dry: int
    skin_type_sensitive: int
    skin_type_oily: int
    skin_type_combination: int
    skin_concern_acne: int
    skin_concern_pigmentation: int
    skin_concern_blackhead: int
    skin_concern_redness: int
    skin_concern_wrinkles_whitening: int
    cleansing_power_very_satisfied: int
    cleansing_power_average: int
    cleansing_power_somewhat_disappointed: int
    cleansing_power_very_disappointed: int
    irritation_level_no_irritation: int
    irritation_level_slight_irritation: int
    irritation_level_moderate_irritation: int
    irritation_level_severe_irritation: int
    absorption_power_very_satisfied: int
    absorption_power_average: int
    absorption_power_somewhat_disappointed: int
    absorption_power_very_disappointed: int
    texture_power_very_satisfied: int
    texture_power_average: int
    texture_power_somewhat_disappointed: int
    texture_power_very_disappointed: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True
