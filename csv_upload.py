import psycopg2
import csv

#Establishing the connection
conn = psycopg2.connect(
   database="", user='postgres', password='', host='localhost', port= '5432'
)

#Setting auto commit false
conn.autocommit = False

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

def replace_empty_with_none(row):
    return [None if x == '' else x for x in row]

# with open('./csv/reviewer.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader) # Skip the header row.
#     for row in reader:
#         cursor.execute(
#         "INSERT INTO reviewer (reviewer_id, reviewer_name, skin_concern_keratin, skin_concern_pores, skin_concern_blackheads, \
#             skin_concern_excess_sebum, personal_color_spring_warm, personal_color_cool, skin_type_trouble_prone, skin_type_oily, \
#             personal_color_autumn_warm, skin_type_sensitive, skin_concern_whitening, skin_concern_redness, skin_concern_wrinkles, \
#             skin_type_dry, personal_color_winter_cool, skin_type_mildly_dry, skin_concern_trouble, skin_type_combination, \
#             skin_concern_dark_circles, skin_concern_elasticity, skin_type_normal, skin_concern_atopy, personal_color_summer_cool, \
#             skin_concern_spots, personal_color_warm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
#             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

# with open('./csv/product.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader) # Skip the header row.
#     for row in reader:
#         row = replace_empty_with_none(row)
#         cursor.execute(
#         "INSERT INTO product (product_id, product_name, product_category, brand_name, original_price, final_price, number_of_reviews, \
#             review_rating, review_5_star_ratio, review_4_star_ratio, review_3_star_ratio, review_2_star_ratio, review_1_star_ratio, \
#             skin_type_dry, skin_type_combination, skin_type_oily, skin_concern_moisturizing, skin_concern_soothing, \
#             skin_concern_wrinkles_whitening, cleansing_power_very_satisfied, cleansing_power_average, cleansing_power_somewhat_disappointed, \
#             spreadability_very_satisfied, spreadability_average, spreadability_somewhat_disappointed, irritation_level_not_irritating, \
#             irritation_level_average, irritation_level_irritating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
#             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

with open('./csv/review.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        row = replace_empty_with_none(row)
        cursor.execute(
        "INSERT INTO review (review_id, product_id, reviewer_id, product_name, reviewer_name, rating, used_over_one_month, repurchase_intention, \
            skin_type_review, skin_concern_review, irritation_level_review, cleansing_power_review, spreadability_review, review_content, \
            review_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

conn.commit()