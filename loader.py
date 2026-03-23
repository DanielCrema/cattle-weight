import pandas as pd
from helpers.parsers import parse_categoricals
from helpers.plot_feature import plot_feature


class DataLoader:
    def __init__(self, train_path='data/gado_train.csv', test_path='data/gado_test.csv'):
        self.train_path = train_path
        self.test_path = test_path
        self.train: pd.DataFrame = pd.DataFrame()
        self.test: pd.DataFrame = pd.DataFrame()

    def load_data(self):
        try:
            self.train = pd.read_csv(self.train_path)
            self.test = pd.read_csv(self.test_path)
        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")
            return

        # Parse categoricals
        categorical_cols = ["raca", "cor_pelagem", "sexo"]

        self.train = parse_categoricals(self.train, categorical_cols)
        self.test = parse_categoricals(self.test, categorical_cols)

        print("Dados carregados com sucesso!\n")

    # =========================
    # 📊 INFO
    # =========================
    def train_info(self):
        print("=> Train dataset info:\n")
        print(self.train.info()) # type: ignore
        print()

    def test_info(self):
        print("=> Test dataset info:\n")
        print(self.test.info())
        print()

    # =========================
    # 📈 FEATURES (PLOTS)
    # =========================
    def train_features(self):
        print("=> TRAIN dataset features:\n")
        for feature in self.train.columns:
            plot_feature(self.train, feature)

    def test_features(self):
        print("=> TEST dataset features:\n")
        for feature in self.test.columns:
            plot_feature(self.test, feature)

    # =========================
    # 📦 GETTERS (útil depois)
    # =========================
    def get_train(self):
        return self.train

    def get_test(self):
        return self.test