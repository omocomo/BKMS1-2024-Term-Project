from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from .database import Base
from sqlalchemy.types import UserDefinedType

class Vector(UserDefinedType):
    def get_col_spec(self):
        return "vector(768)"
    
    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col

class Reviewer(Base):
    __tablename__ = "reviewer"
    reviewer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewer_name = Column(String(255), nullable=False)
    skin_type_trouble_prone = Column(Boolean, nullable=True)
    skin_type_oily = Column(Boolean, nullable=True)
    skin_type_sensitive = Column(Boolean, nullable=True)
    skin_type_dry = Column(Boolean, nullable=True)
    skin_type_mildly_dry = Column(Boolean, nullable=True)
    skin_type_combination = Column(Boolean, nullable=True)
    skin_type_normal = Column(Boolean, nullable=True)
    personal_color_spring_warm = Column(Boolean, nullable=True)
    personal_color_cool = Column(Boolean, nullable=True)
    personal_color_autumn_warm = Column(Boolean, nullable=True)
    personal_color_winter_cool = Column(Boolean, nullable=True)
    personal_color_summer_cool = Column(Boolean, nullable=True)
    personal_color_warm = Column(Boolean, nullable=True)
    skin_concern_keratin = Column(Boolean, nullable=True)
    skin_concern_pores = Column(Boolean, nullable=True)
    skin_concern_blackheads = Column(Boolean, nullable=True)
    skin_concern_excess_sebum = Column(Boolean, nullable=True)
    skin_concern_whitening = Column(Boolean, nullable=True)
    skin_concern_redness = Column(Boolean, nullable=True)
    skin_concern_wrinkles = Column(Boolean, nullable=True)
    skin_concern_trouble = Column(Boolean, nullable=True)
    skin_concern_dark_circles = Column(Boolean, nullable=True)
    skin_concern_elasticity = Column(Boolean, nullable=True)
    skin_concern_atopy = Column(Boolean, nullable=True)
    skin_concern_spots = Column(Boolean, nullable=True)

    reviews = relationship(
        "Review", backref=backref("reviewer"), cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)
    product_category = Column(String(255), nullable=True)
    brand_name = Column(String(255), nullable=True)
    original_price = Column(Integer, nullable=True)
    final_price = Column(Integer, nullable=True)
    number_of_reviews = Column(Integer, nullable=True)
    review_rating = Column(Float, nullable=True)
    review_5_star_ratio = Column(Float, nullable=True)
    review_4_star_ratio = Column(Float, nullable=True)
    review_3_star_ratio = Column(Float, nullable=True)
    review_2_star_ratio = Column(Float, nullable=True)
    review_1_star_ratio = Column(Float, nullable=True)
    skin_type_dry = Column(Integer, nullable=True)
    skin_type_combination = Column(Integer, nullable=True)
    skin_type_oily = Column(Integer, nullable=True)
    skin_concern_moisturizing = Column(Integer, nullable=True)
    skin_concern_soothing = Column(Integer, nullable=True)
    skin_concern_wrinkles_whitening = Column(Integer, nullable=True)
    cleansing_power_very_satisfied = Column(Integer, nullable=True)
    cleansing_power_average = Column(Integer, nullable=True)
    cleansing_power_somewhat_disappointed = Column(Integer, nullable=True)
    spreadability_very_satisfied = Column(Integer, nullable=True)
    spreadability_average = Column(Integer, nullable=True)
    spreadability_somewhat_disappointed = Column(Integer, nullable=True)
    irritation_level_not_irritating = Column(Integer, nullable=True)
    irritation_level_average = Column(Integer, nullable=True)
    irritation_level_irritating = Column(Integer, nullable=True)
    product_name_embedding = Column(Vector, nullable=True) 

    reviews = relationship(
        "Review", backref=backref("product"), cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("reviewer.reviewer_id"), nullable=False)
    product_name = Column(String(255), nullable=True)
    reviewer_name = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=True)
    used_over_one_month = Column(Boolean, nullable=True)
    repurchase_intention = Column(Boolean, nullable=True)
    skin_type_review = Column(String(255), nullable=True)
    skin_concern_review = Column(String(255), nullable=True)
    irritation_level_review = Column(String(255), nullable=True)
    cleansing_power_review = Column(String(255), nullable=True)
    spreadability_review = Column(String(255), nullable=True)
    review_content = Column(Text, nullable=True)
    review_date = Column(DateTime, nullable=True)
    review_content_embedding = Column(Vector, nullable=True) 
