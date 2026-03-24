# 🐄 Model Documentation: LinearRegression

## 📌 Objective
Predict cattle weight (peso_kg) based on physical attributes.

## ⚙️ Specifications

## 🧾 Expected Features
- idade_meses
- altura_cm
- comprimento_corpo_cm
- circunferencia_peito_cm
- raca_Angus
- raca_Brahman
- raca_Hereford
- raca_Nelore
- cor_pelagem_branca
- cor_pelagem_marrom
- cor_pelagem_preta
- sexo_femea
- sexo_macho

## 📥 Sample Input

| Column Name             | Sample value | Dtype   |
| ----------------------- | ------------ | ------- |
| idade_meses             | 10.0         | int64   |
| altura_cm               | 137.6        | float64 |
| comprimento_corpo_cm    | 150.2        | float64 |
| circunferencia_peito_cm | 197.6        | float64 |
| raca_Angus              | 0.0          | float64 |
| raca_Brahman            | 0.0          | float64 |
| raca_Hereford           | 0.0          | float64 |
| raca_Nelore             | 1.0          | float64 |
| cor_pelagem_branca      | 0.0          | float64 |
| cor_pelagem_marrom      | 1.0          | float64 |
| cor_pelagem_preta       | 0.0          | float64 |
| sexo_femea              | 1.0          | float64 |
| sexo_macho              | 0.0          | float64 |


## 📤 Sample Predictions

| y_i | Real Value | Predicted | Abs Error | dtype   |
| --- | ---------- | --------- | --------- | ------- |
| y0  | 573.10     | 614.27    | 41.17     | float64 |
| y1  | 610.60     | 620.07    | 9.47      | float64 |
| y2  | 585.60     | 610.19    | 24.59     | float64 |
| y3  | 627.30     | 612.05    | 15.25     | float64 |
| y4  | 633.40     | 619.84    | 13.56     | float64 |

