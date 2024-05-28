from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReviewBase(BaseModel):
    product_name: str
    reviewer_name: str
    rating: int
    used_over_one_month: bool
    repurchase_intention: bool
    skin_type_review: str
    skin_concern_review: str
    irritation_level_review: str
    cleansing_power_review: Optional[str]
    spreadability_review: Optional[str]
    review_content: str
    review_date: Optional[datetime]


class ReviewCreate(ReviewBase):
    product_id: int
    reviewer_id: int

class Review(ReviewBase):
    review_id: int

    class Config:
        orm_mode = True

class ReviewerBase(BaseModel):
    reviewer_name: str
    skin_type_trouble_prone: bool
    skin_type_oily: bool
    skin_type_sensitive: bool
    skin_type_dry: bool
    skin_type_mildly_dry: bool
    skin_type_combination: bool
    skin_type_normal: bool
    personal_color_spring_warm: bool
    personal_color_cool: bool
    personal_color_autumn_warm: bool
    personal_color_winter_cool: bool
    personal_color_summer_cool: bool
    personal_color_warm: bool
    skin_concern_keratin: bool
    skin_concern_pores: bool
    skin_concern_blackheads: bool
    skin_concern_excess_sebum: bool
    skin_concern_whitening: bool
    skin_concern_redness: bool
    skin_concern_wrinkles: bool
    skin_concern_trouble: bool
    skin_concern_dark_circles: bool
    skin_concern_elasticity: bool
    skin_concern_atopy: bool
    skin_concern_spots: bool


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
    review_rating: int
    review_5_star_ratio: int
    review_4_star_ratio: int
    review_3_star_ratio: int
    review_2_star_ratio: int	
    review_1_star_ratio: int	
    skin_type_dry: int
    skin_type_combination: int
    skin_type_oily: int
    skin_concern_moisturizing: int
    skin_concern_soothing: int
    skin_concern_wrinkles_whitening: int
    cleansing_power_very_satisfied: int
    cleansing_power_average: int
    cleansing_power_somewhat_disappointed: int
    spreadability_very_satisfied: int
    spreadability_average: int
    spreadability_somewhat_disappointed: int
    irritation_level_not_irritating: int
    irritation_level_average: int
    irritation_level_irritating: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True
