import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 참고용 #

# FastAPI 서버 URL
api_url = "http://localhost:8000"

# 페이지 선택
page = st.sidebar.selectbox("Select a page", ["Reviewers", "Reviews", "Reviews Search", "Recommendation"])

# @st.cache_data
# def fetch_reviewer_info(reviewer_id):
#     response = requests.get(f"{api_url}/reviewers/{reviewer_id}")
#     if response.status_code == 404:
#         return None
#     else:
#         return response.json()

# def create_update_reviewer(action):
#     st.header(action + " Reviewer")
#     reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
#     reviewer_info = fetch_reviewer_info(reviewer_id) if action == "Update" else None

#     if action == "Update" and reviewer_info is None:
#         st.warning("Reviewer not found.")

#     name = st.text_input("Name", value=reviewer_info['reviewer_name'] if reviewer_info else "")
#     skin_types = ["Trouble Prone", "Oily", "Sensitive", "Dry", "Mildly Dry", "Combination", "Normal"]
#     personal_colors = ["Spring Warm", "Cool", "Autumn Warm", "Winter Cool", "Summer Cool", "Warm"]
#     skin_concerns = ["Keratin", "Pores", "Blackheads", "Excess Sebum", "Whitening", "Redness", 
#                      "Wrinkles", "Trouble", "Dark Circles", "Elasticity", "Atopy", "Spots"]

#     col1, col2, col3 = st.columns([0.8, 1, 1.5])

#     with col1:
#         st.subheader("Skin Type")
#         skin_type_values = {type.lower().replace(" ", "_"): st.checkbox(type, value=reviewer_info.get(f'skin_type_{type.lower().replace(" ", "_")}', False) if reviewer_info else False) for type in skin_types}
    
#     with col2:
#         st.subheader("Personal Color")
#         personal_color_values = {color.lower().replace(" ", "_"): st.checkbox(color, value=reviewer_info.get(f'personal_color_{color.lower().replace(" ", "_")}', False) if reviewer_info else False) for color in personal_colors}
    
#     with col3:
#         st.subheader("Skin Concern")
#         col4, col5 = st.columns(2)
#         with col4:
#             skin_concern_values = {concern.lower().replace(" ", "_"): st.checkbox(concern, value=reviewer_info.get(f'skin_concern_{concern.lower().replace(" ", "_")}', False) if reviewer_info else False) for concern in skin_concerns[:6]}
#         with col5:
#             skin_concern_values = {concern.lower().replace(" ", "_"): st.checkbox(concern, value=reviewer_info.get(f'skin_concern_{concern.lower().replace(" ", "_")}', False) if reviewer_info else False) for concern in skin_concerns[6:]}

#     if st.button(action):
#         response = None
#         if action == "Create":
#             response = requests.post(f"{api_url}/reviewers/", json={**skin_type_values, **personal_color_values, **skin_concern_values, "reviewer_name": name})
#         elif action == "Update":
#             response = requests.put(f"{api_url}/reviewers/{reviewer_id}", json={**skin_type_values, **personal_color_values, **skin_concern_values, "reviewer_name": name})

#         if response:
#             response_json = response.json()
#             reviewer = {
#                 "reviewer_id": response_json.get("reviewer_id"),
#                 "reviewer_name": response_json.get("reviewer_name")
#             }
#             reviewer_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items() if value == True]
#             st.text(f"Reviewer ID: {reviewer['reviewer_id']}")
#             st.text(f"Reviewer Name: {reviewer['reviewer_name']}")
#             st.text("Selected Personal Info:")
#             st.write(", ".join([f"{value.capitalize()}" for value in reviewer_info]))
#             st.text(f"Reviewer {action.lower()}ed successfully!")


# # Reviewer CRUD
# if page == "Reviewers":
#     st.title("Reviewers Management")

#     action = st.radio("Action", ["Create", "Read", "Update", "Delete"])

#     if action in ["Create", "Update"]:
#         create_update_reviewer(action)
#     elif action == "Read":
#         st.header("Read Reviewers")
#         reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
#         if st.button("Read"):
#             reviewer_info = fetch_reviewer_info(reviewer_id)
#             if reviewer_info:
#                 st.text(f"Reviewer ID: {reviewer_info['reviewer_id']}")
#                 st.text(f"Reviewer Name: {reviewer_info['reviewer_name']}")
#                 st.text("Selected Personal Info:")
#                 selected_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in reviewer_info.items() if value == True]
#                 st.write(", ".join([f"{value.capitalize()}" for value in selected_info]))
#                 st.text("Reviewer read successfully!")
#             else:
#                 st.warning("Reviewer not found.")
#     elif action == "Delete":
#         st.header("Delete Reviewers")
#         reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
#         reviewer_info = fetch_reviewer_info(reviewer_id)
#         if reviewer_info:
#             st.text(f"Reviewer ID: {reviewer_info['reviewer_id']}")
#             st.text(f"Reviewer Name: {reviewer_info['reviewer_name']}")
#         else:
#             st.warning("Reviewer not found.")
#         if st.button("Delete"):
#             response = requests.delete(f"{api_url}/reviewers/{reviewer_id}")
#             st.text("Reviewer deleted successfully!")

#############################################################################################################

# @st.cache_data
def fetch_reviewer_info(reviewer_id):
    response = requests.get(f"{api_url}/reviewers/{reviewer_id}")
    if response.status_code == 404:
        return None
    else:
        return response.json()

# Reviewer CRUD
if page == "Reviewers":
    st.title("Reviewers Management")

    action = st.selectbox("Action", ["Create", "Read", "Update", "Delete"])

    if action == "Create":
        st.header("Create Reviewer")
        name = st.text_input("Name")
        col1, col2, col3 = st.columns([0.8,1,1.5])  # 한 줄에 3개의 checkbox를 표시하기 위한 열 생성

        with col1:
            st.subheader("Skin Type")
            skin_type_trouble_prone = st.checkbox("Trouble Prone")
            skin_type_oily = st.checkbox("Oily")
            skin_type_sensitive = st.checkbox("Sensitive")
            skin_type_dry = st.checkbox("Dry")
            skin_type_mildly_dry = st.checkbox("Mildly Dry")
            skin_type_combination = st.checkbox("Combination")
            skin_type_normal = st.checkbox("Normal")

        with col2:
            st.subheader("Personal Color")
            personal_color_spring_warm = st.checkbox("Spring Warm")
            personal_color_cool = st.checkbox("Cool")
            personal_color_autumn_warm = st.checkbox("Autumn Warm")
            personal_color_winter_cool = st.checkbox("Winter Cool")
            personal_color_summer_cool = st.checkbox("Summer Cool")
            personal_color_warm = st.checkbox("Warm")

        with col3:
            st.subheader("Skin Concern")
            col4, col5 = st.columns(2)
            with col4:
                skin_concern_keratin = st.checkbox("Keratin")
                skin_concern_pores = st.checkbox("Pores")
                skin_concern_blackheads = st.checkbox("Blackheads")
                skin_concern_excess_sebum = st.checkbox("Excess Sebum")
                skin_concern_whitening = st.checkbox("Whitening")
                skin_concern_redness = st.checkbox("Redness")
            with col5:
                skin_concern_wrinkles = st.checkbox("Wrinkles")
                skin_concern_trouble = st.checkbox("Trouble")
                skin_concern_dark_circles = st.checkbox("Dark Circles")
                skin_concern_elasticity = st.checkbox("Elasticity")
                skin_concern_atopy = st.checkbox("Atopy")
                skin_concern_spots = st.checkbox("Spots")
        if st.button("Create"):
            response = requests.post(f"{api_url}/reviewers/", 
                                     json={
                    "reviewer_name": name,
                    "skin_type_trouble_prone": skin_type_trouble_prone,
                    "skin_type_oily": skin_type_oily,
                    "skin_type_sensitive": skin_type_sensitive,
                    "skin_type_dry": skin_type_dry,
                    "skin_type_mildly_dry": skin_type_mildly_dry,
                    "skin_type_combination": skin_type_combination,
                    "skin_type_normal": skin_type_normal,
                    "personal_color_spring_warm": personal_color_spring_warm,
                    "personal_color_cool": personal_color_cool,
                    "personal_color_autumn_warm": personal_color_autumn_warm,
                    "personal_color_winter_cool": personal_color_winter_cool,
                    "personal_color_summer_cool": personal_color_summer_cool,
                    "personal_color_warm": personal_color_warm,
                    "skin_concern_keratin": skin_concern_keratin,
                    "skin_concern_pores": skin_concern_pores,
                    "skin_concern_blackheads": skin_concern_blackheads,
                    "skin_concern_excess_sebum": skin_concern_excess_sebum,
                    "skin_concern_whitening": skin_concern_whitening,
                    "skin_concern_redness": skin_concern_redness,
                    "skin_concern_wrinkles": skin_concern_wrinkles,
                    "skin_concern_trouble": skin_concern_trouble,
                    "skin_concern_dark_circles": skin_concern_dark_circles,
                    "skin_concern_elasticity": skin_concern_elasticity,
                    "skin_concern_atopy": skin_concern_atopy,
                    "skin_concern_spots": skin_concern_spots
                })
            response_json = response.json()
            reviewer = {
                "reviewer_id": response_json.get("reviewer_id"),
                "reviewer_name": response_json.get("reviewer_name")
            }
            reviewer_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items() if value == True]
            st.text(f"Reviewer ID: {reviewer['reviewer_id']}")
            st.text(f"Reviewer Name: {reviewer['reviewer_name']}")
            st.text("Selected Personal Info:")
            st.write(", ".join([f"{value.capitalize()}" for value in reviewer_info]))
            st.text("Reviewer created successfully!")

    elif action == "Read":
        st.header("Read Reviewers")
        reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
        if st.button("Read"):
            response = requests.get(f"{api_url}/reviewers/{reviewer_id}")
            response_json = response.json()
            reviewer = {
                "reviewer_id": response_json.get("reviewer_id"),
                "reviewer_name": response_json.get("reviewer_name")
            }
            reviewer_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items() if value == True]
            st.text(f"Reviewer ID: {reviewer['reviewer_id']}")
            st.text(f"Reviewer Name: {reviewer['reviewer_name']}")
            st.text("Selected Personal Info:")
            st.write(", ".join([f"{value.capitalize()}" for value in reviewer_info]))
            st.text("Reviewer read successfully!")

        if st.button("Read All"):
            response = requests.get(f"{api_url}/reviewers/")
            st.write(response.json())

    elif action == "Update":
        st.header("Update Reviewer")
        reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
        # 선택한 reviewer_id에 해당하는 정보 가져오기
        reviewer_info = fetch_reviewer_info(reviewer_id)
        if reviewer_info is None:
            st.warning("Reviewer not found.")
        else:
            st.text(f"Reviewer ID: {reviewer_info['reviewer_id']}")
            name = st.text_input("New Name", value=reviewer_info['reviewer_name'])
            col1, col2, col3 = st.columns([0.8, 1, 1.5])  

            with col1:
                st.subheader("Skin Type")
                skin_type_trouble_prone = st.checkbox("Trouble Prone", value=reviewer_info.get('skin_type_trouble_prone', False))
                skin_type_oily = st.checkbox("Oily", value=reviewer_info.get('skin_type_oily', False))
                skin_type_sensitive = st.checkbox("Sensitive", value=reviewer_info.get('skin_type_sensitive', False))
                skin_type_dry = st.checkbox("Dry", value=reviewer_info.get('skin_type_dry', False))
                skin_type_mildly_dry = st.checkbox("Mildly Dry", value=reviewer_info.get('skin_type_mildly_dry', False))
                skin_type_combination = st.checkbox("Combination", value=reviewer_info.get('skin_type_combination', False))
                skin_type_normal = st.checkbox("Normal", value=reviewer_info.get('skin_type_normal', False))

            with col2:
                st.subheader("Personal Color")
                personal_color_spring_warm = st.checkbox("Spring Warm", value=reviewer_info.get('personal_color_spring_warm', False))
                personal_color_cool = st.checkbox("Cool", value=reviewer_info.get('personal_color_cool', False))
                personal_color_autumn_warm = st.checkbox("Autumn Warm", value=reviewer_info.get('personal_color_autumn_warm', False))
                personal_color_winter_cool = st.checkbox("Winter Cool", value=reviewer_info.get('personal_color_winter_cool', False))
                personal_color_summer_cool = st.checkbox("Summer Cool", value=reviewer_info.get('personal_color_summer_cool', False))
                personal_color_warm = st.checkbox("Warm", value=reviewer_info.get('personal_color_warm', False))

            with col3:
                st.subheader("Skin Concern")
                col4, col5 = st.columns(2)
                with col4:
                    skin_concern_keratin = st.checkbox("Keratin", value=reviewer_info.get('skin_concern_keratin', False))
                    skin_concern_pores = st.checkbox("Pores", value=reviewer_info.get('skin_concern_pores', False))
                    skin_concern_blackheads = st.checkbox("Blackheads", value=reviewer_info.get('skin_concern_blackheads', False))
                    skin_concern_excess_sebum = st.checkbox("Excess Sebum", value=reviewer_info.get('skin_concern_excess_sebum', False))
                    skin_concern_whitening = st.checkbox("Whitening", value=reviewer_info.get('skin_concern_whitening', False))
                    skin_concern_redness = st.checkbox("Redness", value=reviewer_info.get('skin_concern_redness', False))
                with col5:
                    skin_concern_wrinkles = st.checkbox("Wrinkles", value=reviewer_info.get('skin_concern_wrinkles', False))
                    skin_concern_trouble = st.checkbox("Trouble", value=reviewer_info.get('skin_concern_trouble', False))
                    skin_concern_dark_circles = st.checkbox("Dark Circles", value=reviewer_info.get('skin_concern_dark_circles', False))
                    skin_concern_elasticity = st.checkbox("Elasticity", value=reviewer_info.get('skin_concern_elasticity', False))
                    skin_concern_atopy = st.checkbox("Atopy", value=reviewer_info.get('skin_concern_atopy', False))
                    skin_concern_spots = st.checkbox("Spots", value=reviewer_info.get('skin_concern_spots', False))
        
        # Update 버튼을 누르면 업데이트 요청을 보내고 결과를 보여줌
        if st.button("Update"):
            response = requests.put(f"{api_url}/reviewers/{reviewer_id}", 
                                    json={
                "reviewer_name": name,
                "skin_type_trouble_prone": skin_type_trouble_prone,
                "skin_type_oily": skin_type_oily,
                "skin_type_sensitive": skin_type_sensitive,
                "skin_type_dry": skin_type_dry,
                "skin_type_mildly_dry": skin_type_mildly_dry,
                "skin_type_combination": skin_type_combination,
                "skin_type_normal": skin_type_normal,
                "personal_color_spring_warm": personal_color_spring_warm,
                "personal_color_cool": personal_color_cool,
                "personal_color_autumn_warm": personal_color_autumn_warm,
                "personal_color_winter_cool": personal_color_winter_cool,
                "personal_color_summer_cool": personal_color_summer_cool,
                "personal_color_warm": personal_color_warm,
                "skin_concern_keratin": skin_concern_keratin,
                "skin_concern_pores": skin_concern_pores,
                "skin_concern_blackheads": skin_concern_blackheads,
                "skin_concern_excess_sebum": skin_concern_excess_sebum,
                "skin_concern_whitening": skin_concern_whitening,
                "skin_concern_redness": skin_concern_redness,
                "skin_concern_wrinkles": skin_concern_wrinkles,
                "skin_concern_trouble": skin_concern_trouble,
                "skin_concern_dark_circles": skin_concern_dark_circles,
                "skin_concern_elasticity": skin_concern_elasticity,
                "skin_concern_atopy": skin_concern_atopy,
                "skin_concern_spots": skin_concern_spots
            })

            response_json = response.json()
            reviewer = {
                "reviewer_id": response_json.get("reviewer_id"),
                "reviewer_name": response_json.get("reviewer_name")
            }
            reviewer_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items() if value == True]
            st.text(f"Reviewer ID: {reviewer['reviewer_id']}")
            st.text(f"Reviewer Name: {reviewer['reviewer_name']}")
            st.text("Selected Personal Info:")
            st.write(", ".join([f"{value.capitalize()}" for value in reviewer_info]))
            st.text("Reviewer updated successfully!")

    elif action == "Delete":
        st.header("Delete Reviewer")
        reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
        reviewer_info = fetch_reviewer_info(reviewer_id)
        if reviewer_info is None:
            st.warning("Reviewer not found.")
        else:
            st.text(f"Reviewer ID: {reviewer_info['reviewer_id']}")
            st.text(f"Reviewer Name: {reviewer_info['reviewer_name']}")
        if st.button("Delete"):
            response = requests.delete(f"{api_url}/reviewers/{reviewer_id}")
            response_json = response.json()
            reviewer = {
                "reviewer_id": response_json.get("reviewer_id"),
                "reviewer_name": response_json.get("reviewer_name")
            }
            reviewer_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items() if value == True]
            st.text(f"Reviewer ID: {reviewer['reviewer_id']}")
            st.text(f"Reviewer Name: {reviewer['reviewer_name']}")
            st.text("Selected Personal Info:")
            st.write(", ".join([f"{value.capitalize()}" for value in reviewer_info]))
            st.text("Reviewer deleted successfully!")

# # Product CRUD
# elif page == "Products":
#     st.title("Products Management")

#     action = st.radio("Action", ["Create", "Read", "Update", "Delete"])

#     if action == "Create":
#         st.header("Create Product")
#         name = st.text_input("Name")
#         description = st.text_input("Description")
#         if st.button("Create"):
#             response = requests.post(f"{api_url}/products/", json={"name": name, "description": description})
#             st.write(response.json())

#     elif action == "Read":
#         st.header("Read Products")
#         product_id = st.number_input("Product ID", min_value=0, step=1)
#         if st.button("Read"):
#             response = requests.get(f"{api_url}/products/{product_id}")
#             st.write(response.json())
#         if st.button("Read All"):
#             response = requests.get(f"{api_url}/products/")
#             st.write(response.json())

#     elif action == "Update":
#         st.header("Update Product")
#         product_id = st.number_input("Product ID", min_value=0, step=1)
#         name = st.text_input("New Name")
#         description = st.text_input("New Description")
#         if st.button("Update"):
#             response = requests.put(f"{api_url}/products/{product_id}", json={"name": name, "description": description})
#             st.write(response.json())

#     elif action == "Delete":
#         st.header("Delete Product")
#         product_id = st.number_input("Product ID", min_value=0, step=1)
#         if st.button("Delete"):
#             response = requests.delete(f"{api_url}/products/{product_id}")
#             st.write(response.json())

# Review CRUD
elif page == "Reviews":
    st.title("Reviews Management")

    action = st.selectbox("Action", ["Create", "Read", "Update", "Delete"])

    if action == "Create":
        st.header("Create Review")
        product_id = st.number_input("Product ID", min_value=0, step=1)
        reviewer_id = st.number_input("Reviewer ID", min_value=0, step=1)
        rating = st.number_input("Rating", min_value=0, max_value=5, step=1)
        content = st.text_area("Content")
        used_over_one_month = st.checkbox("Used over one month")
        if st.button("Create"):
            response = requests.post(
                f"{api_url}/reviews/",
                json={
                    "product_id": product_id,
                    "reviewer_id": reviewer_id,
                    "rating": rating,
                    "content": content,
                    "used_over_one_month": used_over_one_month
                }
            )
            st.write(response.json())

    elif action == "Read":
        st.header("Read Reviews")
        review_id = st.number_input("Review ID", min_value=0, step=1)
        if st.button("Read"):
            response = requests.get(f"{api_url}/reviews/{review_id}")
            print(response)
            # response_json = response.json()
            # review = {
            #     "review_id": response_json.get("review_id"),
            #     "reviewer_name": response_json.get("reviewer_name")
            # }
            # review_info = [' '.join(key.replace("_", " ").capitalize().split()[2:]) for key, value in response_json.items()[:-1] if value == True]
            # st.text(f"Reviewer ID: {review['reviewer_id']}")
            # st.text(f"Reviewer Name: {review['reviewer_name']}")
            # st.write(", ".join([f"{value.capitalize()}" for value in review_info]))
            # st.text("Review read successfully!")

        # if st.button("Read All"):
        #     response = requests.get(f"{api_url}/review/")
        #     st.write(response.json())


    elif action == "Update":
        st.header("Update Review")
        review_id = st.number_input("Review ID", min_value=0, step=1)
        rating = st.number_input("New Rating", min_value=0, max_value=5, step=1)
        content = st.text_area("New Content")
        used_over_one_month = st.checkbox("New Used over one month")
        if st.button("Update"):
            response = requests.put(
                f"{api_url}/reviews/{review_id}",
                json={
                    "rating": rating,
                    "content": content,
                    "used_over_one_month": used_over_one_month
                }
            )
            st.write(response.json())

    elif action == "Delete":
        st.header("Delete Review")
        review_id = st.number_input("Review ID", min_value=0, step=1)
        if st.button("Delete"):
            response = requests.delete(f"{api_url}/reviews/{review_id}")
            st.write(response.json())

# Reviews Search System
elif page == "Reviews Search":
    st.title("Reviews Search")
    # 검색 조건 입력
    search_type = st.selectbox("Search Type", ["By Product and Keyword", "By Rating", "By Date Range", "By Skin Type", "Brand Review Ratios"])

    if search_type == "By Product and Keyword":
        product_name = st.text_input("Product Name")
        keyword = st.text_input("Keyword")
        if st.button("Search"):
            response = requests.get(f"{api_url}/reviews/product/{product_name}/keyword/{keyword}")
            if response.status_code == 200:
                reviews = response.json()
                df = pd.DataFrame(reviews)
                st.write(df)
            else:
                st.error("Failed to fetch reviews")

    elif search_type == "By Rating":
        product_name = st.text_input("Product Name")
        if st.button("Search"):
            response = requests.get(f"{api_url}/reviews/product/{product_name}/rating")
            if response.status_code == 200:
                reviews = response.json()
                df = pd.DataFrame(reviews)
                st.write(df)
            else:
                st.error("Failed to fetch reviews")

    elif search_type == "By Date Range":
        start_date = st.date_input("Start Date", datetime(2023, 1, 1))
        end_date = st.date_input("End Date", datetime(2023, 12, 31))
        if st.button("Search"):
            response = requests.get(f"{api_url}/reviews/dates/", params={"start_date": start_date, "end_date": end_date})
            if response.status_code == 200:
                reviews = response.json()
                df = pd.DataFrame(reviews)
                st.write(df)
            else:
                st.error("Failed to fetch reviews")

    elif search_type == "By Skin Type":
        skin_type = st.text_input("Skin Type")
        if st.button("Search"):
            response = requests.get(f"{api_url}/reviews/skin_type/{skin_type}")
            if response.status_code == 200:
                reviews = response.json()
                df = pd.DataFrame(reviews)
                st.write(df)
            else:
                st.error("Failed to fetch reviews")

    elif search_type == "Brand Review Ratios":
        brand_name = st.text_input("Brand Name")
        if st.button("Search"):
            response = requests.get(f"{api_url}/reviews/brand/{brand_name}/ratios")
            if response.status_code == 200:
                reviews = response.json()
                df = pd.DataFrame(reviews)
                st.write(df)
            else:
                st.error("Failed to fetch reviews")

# Recommendation System
elif page == "Recommendation":
    st.title("Product Recommendation")

    # Recommendation system type selection
    # recsys_type = st.selectbox("Select Recommendation System", ["recsys1", "recsys2", "recsys3"])

    # Common user_vector input
    st.subheader("Skin Type & Concern")
    col1, col2 = st.columns(2)  
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            skin_type_trouble_prone = st.checkbox("Trouble Prone")
            skin_type_oily = st.checkbox("Oily")
            skin_type_sensitive = st.checkbox("Sensitive")
            skin_type_dry = st.checkbox("Dry")
        with col4:
            skin_type_mildly_dry = st.checkbox("Mildly Dry")
            skin_type_combination = st.checkbox("Combination")
            skin_type_normal = st.checkbox("Normal")
    with col2:
        col5, col6 = st.columns(2)
        with col5:
            # skin_concern_keratin = st.checkbox("Keratin")
            # skin_concern_pores = st.checkbox("Pores")
            # skin_concern_blackheads = st.checkbox("Blackheads")
            skin_concern_excess_sebum = st.checkbox("Excess Sebum")
            skin_concern_whitening = st.checkbox("Whitening")
            # skin_concern_redness = st.checkbox("Redness")
            skin_concern_wrinkles = st.checkbox("Wrinkles")
        with col6:
            skin_concern_trouble = st.checkbox("Trouble")
            # skin_concern_dark_circles = st.checkbox("Dark Circles")
            # skin_concern_elasticity = st.checkbox("Elasticity")
            skin_concern_atopy = st.checkbox("Atopy")
            # skin_concern_spots = st.checkbox("Spots")

    user_vector = {
        "reviewer_id": -1,
        "skin_type_trouble_prone": skin_type_trouble_prone,
        "skin_type_oily": skin_type_oily,
        "skin_type_sensitive": skin_type_sensitive,
        "skin_type_dry": skin_type_dry,
        "skin_type_mildly_dry": skin_type_mildly_dry,
        "skin_type_combination": skin_type_combination,
        "skin_type_normal": skin_type_normal,
        "skin_concern_trouble": skin_concern_trouble,
        "skin_concern_atopy": skin_concern_atopy,
        "skin_concern_excess_sebum": skin_concern_excess_sebum,
        "skin_concern_whitening": skin_concern_whitening,
        "skin_concern_wrinkles": skin_concern_wrinkles,

        # "skin_concern_keratin": skin_concern_keratin,
        # "skin_concern_pores": skin_concern_pores,
        # "skin_concern_blackheads": skin_concern_blackheads,
        # "skin_concern_redness": skin_concern_redness,
        # "skin_concern_dark_circles": skin_concern_dark_circles,
        # "skin_concern_elasticity": skin_concern_elasticity,
        # "skin_concern_atopy": skin_concern_atopy,
        # "skin_concern_spots": skin_concern_spots
    }

    # st.subheader("Select Product")
    # Product keyword selection
    st.text('특정 카테고리의 제품을 원할 경우 Query에 입력 \n예시) 크림, 에센스, 폼 클렌저, 미스트, 오일, 필링, 선크림, 토너, 클렌징 워터, 로션')
    
    # Check if any skin type or concern is selected
    any_skin_type_or_concern = any([
        skin_type_oily, skin_type_trouble_prone, skin_type_sensitive, skin_type_combination,
        skin_type_normal, skin_type_dry, skin_type_mildly_dry, skin_concern_excess_sebum,
        skin_concern_trouble, skin_concern_atopy, skin_concern_whitening, skin_concern_wrinkles
    ])

    # Input for the query
    st.subheader("What product are you looking for?")
    query = st.text_input("Query")

    if st.button("Get Recommendations"):
        if any_skin_type_or_concern and query:
            # recsys1: Both user vector and query provided
            response = requests.get(f"{api_url}/recsys1/{query}", json=user_vector)
        elif any_skin_type_or_concern:
            # recsys2: Only user vector provided
            response = requests.get(f"{api_url}/recsys2", json=user_vector)
        elif query:
            # recsys3: Only query provided
            response = requests.get(f"{api_url}/recsys3/{query}")
        else:
            st.error("Please provide either a query or select at least one skin type or concern.")

        recommendations = response.json()
        if len(recommendations) != 0:
            df = pd.DataFrame(recommendations)
            df = df.set_index(df.columns[0])
            st.write(df)
        else:
            st.error("Failed to search proper product")
