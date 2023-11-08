import os
import pickle
from typing import Tuple, Union, List
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split


FILENAME_MODEL = os.path.abspath(f"{os.curdir}/challenge/models/reg_model_2.pk")
THRESHOLD_IN_MINUTES = 15


class DelayModel:

    def __init__(
        self
    ):
        self._model = self.__load_model(FILENAME_MODEL)

    @property
    def train_columns(self):
        return [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

    def __load_model(self, filename: str):
        with open(filename, 'rb') as fp:
            return pickle.load(fp)

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        def get_delay_col(data):
            fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
            fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
            delay = 1 if (((fecha_o - fecha_i).total_seconds()) / 60) > THRESHOLD_IN_MINUTES else 0
            return delay

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')],
            axis=1
        )
        if target_column is not None:
            data[target_column] = data.apply(get_delay_col, axis=1)
            return features[self.train_columns], pd.DataFrame(data[target_column])
        return features[self.train_columns]

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train, x_test, y_train, y_test = train_test_split(features, target,
                                                                test_size = 0.33, random_state = 42)

        self._model.fit(x_train, y_train)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return self._model.predict(features).tolist()