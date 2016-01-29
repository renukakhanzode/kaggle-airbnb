import pandas as pd
import numpy as np

from utils.preprocessing import one_hot_encoding
from sklearn.preprocessing import LabelEncoder
from xgboost.sklearn import XGBClassifier

# Define data path and suffix
processed_data_path = '../data/processed/'
suffix = '3'

# Load raw data
train_users = pd.read_csv(processed_data_path + 'train_users.csv' + suffix)
test_users = pd.read_csv(processed_data_path + 'test_users.csv' + suffix)

# Join users
users = pd.concat((train_users, test_users), axis=0, ignore_index=True)

# Set ID as index
users = users.set_index('id')
train_users = train_users.set_index('id')
test_users = test_users.set_index('id')

# Drop columns
drop_list = [
    'date_account_created',
    'date_first_active',
    'timestamp_first_active'
]

users.drop(drop_list, axis=1, inplace=True)

# Encode categorical features
categorical_features = [
    'gender', 'signup_method', 'signup_flow', 'language', 'affiliate_channel',
    'affiliate_provider', 'first_affiliate_tracked', 'signup_app',
    'first_device_type', 'first_browser', 'most_used_device'
]

users = one_hot_encoding(users, categorical_features)

# Split into train and test users
train_users = users.loc[train_users.index]
test_users = users.loc[test_users.index]
test_users.drop('country_destination', inplace=True, axis=1)

# Fill NaN
# users.fillna(-1, inplace=True)

# TODO: Move this to select_features function
# Get important features from XGBClassifier
# y_train = train_users['country_destination']
# train_users.drop(['country_destination'], axis=1, inplace=True)
# label_encoder = LabelEncoder()
# encoded_y_train = label_encoder.fit_transform(y_train)
#
#
# clf = XGBClassifier(
#     max_depth=6,
#     learning_rate=0.2,
#     n_estimators=100,
#     nthread=-1,
#     seed=42
# )
#
# clf.fit(train_users, encoded_y_train)
# booster = clf.booster()
#
# train_users = train_users[booster.get_fscore().keys()]
# test_users = test_users[booster.get_fscore().keys()]
#
# train_users = pd.concat([train_users, y_train], axis=1)

# Set -1 to NaNs to save disk space
# train_users.replace(-1, np.nan, inplace=True)
# test_users.replace(-1, np.nan, inplace=True)

# IDEA: Add cluster
# from sklearn.cluster import KMeans
#
# m = KMeans(12, n_jobs=-2)
# m.fit_predict(train_users)
#
# print m

# IDEA: Average distance to N neighbors of each class

# Save to csv
prefix = 'processed_'
train_users.to_csv(processed_data_path + prefix + 'train_users.csv' + suffix)
test_users.to_csv(processed_data_path + prefix + 'test_users.csv' + suffix)
