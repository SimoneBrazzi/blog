import pandas as pd
import pickle

# read pickle file in python which is a model grid search result
path = "~/R/blog/posts/credit_score/kaggle/credit_score_grid_search_dtc_f1.pkl"
with open(path, 'rb') as f:
    x = pickle.load(f)

