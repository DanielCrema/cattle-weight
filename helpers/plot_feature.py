import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from helpers.label_plot import label_plot
from helpers.plot_central_tendency import plot_central_tendency

def plot_histplot(df: pd.DataFrame, feature: str) -> None:
    """
    Gera um histograma com curva de densidade para uma variável numérica
    do DataFrame.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados para visualização.
    feature : str
        - Nome da variável numérica a ser plotada.

    Retorna
    -------
    None
    """
    plt.figure(figsize=(6, 4))
    sns.histplot(list(df[feature]), kde=True, color='green', alpha=0.7)

    label_plot(title=f'Distribution of {feature}', xlabel=feature, ylabel='Frequency', fontsizes='large')
    plot_central_tendency(df[feature])
    
    plt.show()
    plt.close()

def plot_barplot(df: pd.DataFrame, feature: str) -> None:
    """
    Gera um gráfico de barras para visualizar a distribuição de uma
    variável categórica do DataFrame.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados para visualização.
    feature : str
        - Nome da variável categórica a ser plotada.

    Retorna
    -------
    None
    """
    counts = df[feature].value_counts().reset_index()
    counts.columns = [feature, "count"]
    counts = counts.sort_values(by="count", ascending=False)
    
    plt.figure(figsize=(6, 4))
    sns.barplot(
        data=counts,
        x=feature,
        y="count",
        order=counts[feature],
        hue=counts.index,
        legend=False,
        palette='Set2'
    )

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    minor_bar = min(df[feature].value_counts().values)
    greater_bar = max(df[feature].value_counts().values)
    plt.ylim(minor_bar * 0.35, greater_bar * 1.05)

    label_plot(title=f'Distribution of {feature}', xlabel=feature, ylabel='Frequency', fontsizes='large')
    for i, v in enumerate(df[feature].value_counts().values):
        plt.text(i, v, v, ha='center', va='bottom')

    if df[feature].unique().shape[0] > 3:
        plt.xticks(rotation=25)

    plt.tight_layout()
    plt.show()
    plt.close()

def plot_feature(df: pd.DataFrame, feature: str) -> None:
    """
    Seleciona automaticamente o tipo de gráfico com base no tipo da
    variável e realiza a visualização correspondente.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados para visualização.
    feature : str
        - Nome da variável a ser analisada.

    Retorna
    -------
    None
    """
    if df[feature].dtype == 'int64' or df[feature].dtype == 'int32' or df[feature].dtype == 'int16' or df[feature].dtype == 'int8' or df[feature].dtype == 'float64' or df[feature].dtype == 'float32' or df[feature].dtype == 'float16' or df[feature].dtype == 'float8':
        plot_histplot(df, feature)
    else:
        plot_barplot(df, feature)