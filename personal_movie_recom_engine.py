"""_summary_: Top ten movies for a user
"""
import pandas as pd

movie_df = pd.read_json('movie_data.json')
user_pref = pd.read_json('user_preference.json')
related_users = pd.read_json('related_users.json')


def per_user_data(user_id: int, no_of_records: int = 10):
    # Finding a recommendations for a user
    if user_pref[user_pref['user_id'] == user_id].empty:
        return None
    pref = user_pref[user_pref['user_id'] == user_id]['preference'].to_list()[
        0]
    
    genre = list(map(lambda x: x.get('genre'), pref))
    columns_name = movie_df.columns
    df = pd.DataFrame(columns=columns_name)
    for i in genre:
        data = movie_df[movie_df['genres'].map(lambda x:i in x)]
        # Sorting based on the release date
        data.sort_values(by='release_date')
        df = df.append(data.head(no_of_records))
    return df


def movies_recommendation(user_id: int) -> list:
    # Get a User Recommendation
    user_data = per_user_data(user_id)

    # Considering all related users based recommendations
    combined_related_users_data = pd.DataFrame(columns=movie_df.columns)
    friend_circle = related_users.get(user_id)
    if not friend_circle.empty:
        for f in friend_circle[0]:
            combined_related_users_data = combined_related_users_data.append(
                per_user_data(f.get('user_id'), 2))

    # finding the common movies based on the users top generated recommendations
    friends_recomm = combined_related_users_data[combined_related_users_data.movie_id.isin(
        user_data.movie_id)]
    # remaining recommendations
    users_recomm = user_data.sample(n=10-len(friends_recomm))
    users_recomm = users_recomm.append(friends_recomm)
    return users_recomm['movie_name'].to_list()


if __name__ == '__main__':
    user_id = 398  # int(input("Enter user ID: "))
    result = movies_recommendation(user_id)
    print(f"Top 10 Recommended Movies for a user:{user_id}\n {result}")
