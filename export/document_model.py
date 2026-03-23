import os
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Literal, Any
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

OutputFormat = Literal['.md', '.txt', '.html']


def document_model(
    model: LinearRegression | RandomForestRegressor | Any,
    model_name: str,
    model_metadata: dict[str, Any],
    model_features: list[str],
    x: pd.DataFrame,
    y: pd.Series,
    output_format: OutputFormat = '.md',
    timestamp: bool = False
) -> None:
    """
    Gera a documentação de um modelo de regressão treinado.
    """

    # ==================================================
    # Helpers
    # ==================================================

    def format_model_input_summary(df: pd.DataFrame) -> str:
        first_row = df.iloc[0]

        col1_width = max(len("Column Name"), *(len(col) for col in df.columns))
        values = [str(first_row[col]) for col in df.columns]
        col2_width = max(len("Sample value"), *(len(v) for v in values))
        dtypes = [str(df[col].dtype) for col in df.columns]
        col3_width = max(len("Dtype"), *(len(d) for d in dtypes))

        header = (
            f"| {'Column Name'.ljust(col1_width)} "
            f"| {'Sample value'.ljust(col2_width)} "
            f"| {'Dtype'.ljust(col3_width)} |"
        )

        separator = (
            f"| {'-' * col1_width} "
            f"| {'-' * col2_width} "
            f"| {'-' * col3_width} |"
        )

        lines = [header, separator]

        for col in df.columns:
            value = str(first_row[col])
            dtype = str(df[col].dtype)
            lines.append(
                f"| {col.ljust(col1_width)} "
                f"| {value.ljust(col2_width)} "
                f"| {dtype.ljust(col3_width)} |"
            )

        return "\n".join(lines)

    def format_model_output_summary(
        series: pd.Series,
        model,
        x_subset: pd.DataFrame,
        target_name: str = "y"
    ) -> str:
        preds = model.predict(x_subset)

        dtype = str(series.dtype)

        labels = [f"{target_name}{i}" for i in range(min(5, len(series)))]
        real_values = [f"{series.iloc[i]:.2f}" for i in range(len(labels))]
        pred_values = [f"{preds[i]:.2f}" for i in range(len(labels))]
        errors = [f"{abs(series.iloc[i] - preds[i]):.2f}" for i in range(len(labels))]

        col1_width = max(len("y_i"), *(len(l) for l in labels))
        col2_width = max(len("Real Value"), *(len(v) for v in real_values))
        col3_width = max(len("Predicted"), *(len(v) for v in pred_values))
        col4_width = max(len("Abs Error"), *(len(v) for v in errors))
        col5_width = max(len("dtype"), len(dtype))

        header = (
            f"| {'y_i'.ljust(col1_width)} "
            f"| {'Real Value'.ljust(col2_width)} "
            f"| {'Predicted'.ljust(col3_width)} "
            f"| {'Abs Error'.ljust(col4_width)} "
            f"| {'dtype'.ljust(col5_width)} |"
        )

        separator = (
            f"| {'-' * col1_width} "
            f"| {'-' * col2_width} "
            f"| {'-' * col3_width} "
            f"| {'-' * col4_width} "
            f"| {'-' * col5_width} |"
        )

        lines = [header, separator]

        for i in range(len(labels)):
            lines.append(
                f"| {labels[i].ljust(col1_width)} "
                f"| {real_values[i].ljust(col2_width)} "
                f"| {pred_values[i].ljust(col3_width)} "
                f"| {errors[i].ljust(col4_width)} "
                f"| {dtype.ljust(col5_width)} |"
            )

        return "\n".join(lines)

    # ==================================================
    # Prepare content
    # ==================================================

    x_head_text = format_model_input_summary(x)
    y_head_text = format_model_output_summary(y, model=model, x_subset=x)

    x_head_html = x.head().to_html()
    y_head_html = y.head().to_frame(name="peso_kg").to_html()

    specs = model_metadata
    model_type = specs['model']
    parameters = specs['specifications']

    # Diretório
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    os.makedirs(models_dir, exist_ok=True)

    filename = f'model_documentation_{model_name}{output_format}'

    filename_raw = filename
    if timestamp:
        base, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{ts}{ext}"
        filename_raw = f"{base}_{ts}"

    filepath = os.path.join(models_dir, filename)

    # ==================================================
    # Write file
    # ==================================================

    if output_format == '.md':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 🐄 Model Documentation: {model_type}\n\n")

            f.write("## 📌 Objective\n")
            f.write("Predict cattle weight (peso_kg) based on physical attributes.\n\n")

            f.write("## ⚙️ Specifications\n")
            for k, v in parameters.items():
                f.write(f"- **{k}**: `{v}`\n")

            f.write("\n## 🧾 Expected Features\n")
            for feature in model_features:
                f.write(f"- {feature}\n")

            f.write("\n## 📥 Sample Input\n")
            f.write("\n" + x_head_text + "\n\n")

            f.write("\n## 📤 Sample Predictions\n")
            f.write("\n" + y_head_text + "\n\n")

    elif output_format == '.txt':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Model Documentation: {model_type}\n\n")

            f.write("Objective:\nPredict cattle weight (peso_kg)\n\n")

            f.write("Specifications:\n")
            for k, v in parameters.items():
                f.write(f"- {k}: {v}\n")

            f.write("\nExpected Features:\n")
            for feature in model_features:
                f.write(f"- {feature}\n")

            f.write("\nSample Input:\n")
            f.write(x_head_text + "\n")

            f.write("\nSample Predictions:\n")
            f.write(y_head_text + "\n")

    elif output_format == '.html':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"<h1>🐄 Model Documentation: {model_type}</h1>\n")
            f.write("<h2>Objective</h2>")
            f.write("<p>Predict cattle weight (peso_kg)</p>")

            f.write("<h2>Specifications</h2><ul>")
            for k, v in parameters.items():
                f.write(f"<li><b>{k}</b>: {v}</li>")
            f.write("</ul>")

            f.write("<h2>Expected Features</h2><ul>")
            for feature in model_features:
                f.write(f"<li>{feature}</li>")
            f.write("</ul>")

            f.write("<h2>Sample Input</h2>")
            f.write(x_head_html)

            f.write("<h2>Sample Predictions</h2>")
            f.write(y_head_html)

    else:
        raise ValueError("Invalid output_format.")

    print(f"📁 Arquivo salvo com sucesso:")
    print(f"   → ./models/{filename_raw}{output_format}")