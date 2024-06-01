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
    cleansing_power_review: Optional[str] = None
    spreadability_review: Optional[str] = None
    review_content: Optional[str] = None
    review_date: Optional[datetime] = None
    review_content_embedding: Optional[List[float]] = None


class ReviewCreate(ReviewBase):
    product_id: int
    reviewer_id: int


class Review(ReviewBase):
    review_id: int

    class Config:
        orm_mode = True


class ReviewerBase(BaseModel):
    reviewer_name: str
    skin_type_trouble_prone: Optional[bool] = None
    skin_type_oily: Optional[bool] = None
    skin_type_sensitive: Optional[bool] = None
    skin_type_dry: Optional[bool] = None
    skin_type_mildly_dry: Optional[bool] = None
    skin_type_combination: Optional[bool] = None
    skin_type_normal: Optional[bool] = None
    personal_color_spring_warm: Optional[bool] = None
    personal_color_cool: Optional[bool] = None
    personal_color_autumn_warm: Optional[bool] = None
    personal_color_winter_cool: Optional[bool] = None
    personal_color_summer_cool: Optional[bool] = None
    personal_color_warm: Optional[bool] = None
    skin_concern_keratin: Optional[bool] = None
    skin_concern_pores: Optional[bool] = None
    skin_concern_blackheads: Optional[bool] = None
    skin_concern_excess_sebum: Optional[bool] = None
    skin_concern_whitening: Optional[bool] = None
    skin_concern_redness: Optional[bool] = None
    skin_concern_wrinkles: Optional[bool] = None
    skin_concern_trouble: Optional[bool] = None
    skin_concern_dark_circles: Optional[bool] = None
    skin_concern_elasticity: Optional[bool] = None
    skin_concern_atopy: Optional[bool] = None
    skin_concern_spots: Optional[bool] = None


class ReviewerCreate(ReviewerBase):
    pass


class Reviewer(ReviewerBase):
    reviewer_id: int
    # reviews: List[Review] = []

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    product_name: str
    product_category: Optional[str] = None
    brand_name: Optional[str] = None
    original_price: Optional[int] = None
    final_price: Optional[int] = None
    number_of_reviews: Optional[int] = None
    review_rating: Optional[int] = None
    review_5_star_ratio: Optional[int] = None
    review_4_star_ratio: Optional[int] = None
    review_3_star_ratio: Optional[int] = None
    review_2_star_ratio: Optional[int] = None
    review_1_star_ratio: Optional[int] = None
    skin_type_dry: Optional[int] = None
    skin_type_combination: Optional[int] = None
    skin_type_oily: Optional[int] = None
    skin_concern_moisturizing: Optional[int] = None
    skin_concern_soothing: Optional[int] = None
    skin_concern_wrinkles_whitening: Optional[int] = None
    cleansing_power_very_satisfied: Optional[int] = None
    cleansing_power_average: Optional[int] = None
    cleansing_power_somewhat_disappointed: Optional[int] = None
    spreadability_very_satisfied: Optional[int] = None
    spreadability_average: Optional[int] = None
    spreadability_somewhat_disappointed: Optional[int] = None
    irritation_level_not_irritating: Optional[int] = None
    irritation_level_average: Optional[int] = None
    irritation_level_irritating: Optional[int] = None
    product_name_embedding: Optional[List[float]] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    product_id: int
    # reviews: List[Review] = []

    class Config:
        orm_mode = True
