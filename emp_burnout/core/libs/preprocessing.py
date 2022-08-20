import json
import pandas as pd
import logging

from pathlib import Path
from emp_burnout.utils.io import load_obj, save_obj
from ...utils import constants
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler


LOG = logging.getLogger(__name__)


@dataclass
class Preprocessor:
    config: dict
    
    def load_trainset_cols(self):
        with (Path(constants.SCHEMAS_DIR) / "columns.json").open() as stream:
            return json.load(stream)

    def save_trainset_cols(self, X):
        with (Path(constants.SCHEMAS_DIR) / "columns.json").open("w") as stream:
            json.dump(list(X), stream)

    def scale_features(self, X, training=True):
        save_path = Path(constants.EXTRAS_DIR) / "scaler.pkl"
        if training:
            scaler = StandardScaler()
            scaler.fit(X)
            save_obj(scaler, save_path, empty_dir=True)
            LOG.info("Saved scaler to %s", save_path)
        else:
            scaler = load_obj(save_path)
            LOG.info("Loaded scaler from %s", save_path)
        if len(X) > 0:
            X = scaler.transform(X)
        return X

    def add_missing_cols(self, df, cols):
        df_final = pd.DataFrame(data=None, columns=cols)
        df_final = pd.concat([df_final, df], ignore_index=True,sort=False)
        return df_final.fillna(0)

    def preprocess(self, df, training=True):
        # 1. drop unwanted cols
        df.drop("emp_id", axis=1, inplace=True)
        
        if training:
            missing_target_rows = df.loc[df["burn_rate"].isna(), :].index
            df = df.drop(missing_target_rows, axis=0).reset_index(drop=True)
        
        # 2. feature encoding
        df["date_of_joining"] = pd.to_datetime(df["date_of_joining"])
        df["join_month"] = df["date_of_joining"].apply(lambda x: x.month)
        df["join_day"] = df["date_of_joining"].apply(lambda x: x.day)
        df.drop("date_of_joining", axis=1, inplace=True)

        df["gender"] = df["gender"].replace({'Female': 0, 'Male': 1})
        df["company_type"] = df["company_type"].replace({'Product': 0, 'Service': 1})
        df["wfh_setup_available"] = df["wfh_setup_available"].replace({'No': 0, 'Yes': 1})

        # 3. imputing missing vals (TODO: fill with mean of trainset, if training=False)
        for column in ["resource_allocation", "mental_fatigue_score"]:
            df[column] = df[column].fillna(df[column].mean())

        # 4. feature-label split
        y = None

        if training:
            y = df["burn_rate"]
            X = df.drop("burn_rate", axis=1)
            self.save_trainset_cols(X)

        else:
            cols = self.load_trainset_cols()
            X = self.add_missing_cols(df, cols)

        # 5. scale X
        X = self.scale_features(X, training)
        
        return X, y
   