### Predicting Undergraduate Academic Success

#### Executive summary
This project aims to predict undergraduate student academic success based on several factors using log-log and power-law relationships. By utilizing the “Predict students' dropout and academic success” dataset from Kaggle, the analysis focuses on preprocessing data with logarithmic transformations to capture non-linear and multiplicative effects. The power-law relationship \( y = ax^b \) transforms to \( \log(y) = \log(a) + b\log(x) \), enabling the application of linear regression on log-transformed variables.

#### Rationale
This project leverages machine learning to provide a nuanced understanding of the factors affecting academic success, enabling the development of effective educational strategies.

#### Research Question
Can an undergraduate student’s academic success be predicted based on several factors using Log-Log or Power-Log relationships?

#### Data Sources
https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention

#### Methodology
1. **Data Preprocessing**: Applying logarithmic transformations to both dependent and independent variables helps in linearizing multiplicative relationships. For example, doubling study hours may not linearly double academic performance due to diminishing returns.
2. **Feature Identification and Preparation**: Key factors influencing academic success, such as study hours and attendance, are identified and prepared. Interaction terms are created to capture the combined effects of multiple factors.
3. **Model Training**: Linear regression models are trained on log-transformed data to understand the elasticities and interaction effects among variables.


#### Results
Upon analysis of the coefficients to understand the relationships, I found that coefficients represent elasticities; and, the intercept represents the expected log of academic success when all log-transformed factors are zero (which corresponds to the multiplicative constant in the original non-logarithmic scale). The insights gained from analysis can help in understanding how various factors combine and contribute to academic success in a non-linear, multiplicative manner, providing a more nuanced understanding that can inform targeted interventions and support strategies.

#### Next steps
What suggestions do you have for next steps?

#### Outline of project

- [Link to notebook 1]()


##### Contact and Further Information
Model Validation:
Validate the model using cross-validation techniques to ensure robustness.
Compare the performance of the log-log model with other models, such as polynomial regression or non-linear models.

Reporting and Visualization:
Create visualizations to illustrate the relationships between variables and academic success.
    
Implementation and Further Research:
Prepare a comprehensive report summarizing the findings, including key insights and potential recommendations for interventions.Conduct further research to explore additional factors or to validate findings in different educational contexts or datasets.
