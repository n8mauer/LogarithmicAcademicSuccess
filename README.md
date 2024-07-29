## Predicting Undergraduate Academic Success

### Executive summary
This project aims to predict undergraduate student academic success based on several factors using log-log and power-law relationships. By utilizing the “Predict students' dropout and academic success” dataset from Kaggle, the analysis focuses on preprocessing data with logarithmic transformations to capture non-linear and multiplicative effects. The power-law relationship \( y = ax^b \) transforms to \( \log(y) = \log(a) + b\log(x) \), enabling the application of linear regression on log-transformed variables.

### Rationale
This project leverages machine learning to provide a nuanced understanding of the factors affecting academic success, enabling the development of effective and intentional educational strategies to populations that could be in need of additional resources.

Over the past 20 years, the undergraduate dropout rate in the United States has shown notable trends and variations. On average, about [40% of college students](https://www.thinkimpact.com/college-dropout-rates/) do not complete their degree programs. The dropout rate tends to be highest in the first year, with approximately [20-30% of freshmen](https://nutmegeducation.com/college-dropout-rates) not returning for their sophomore year.

Economic factors play a significant role in dropout rates. Financial instability is a primary reason for [38% of students](https://www.thinkimpact.com/college-dropout-rates/) leaving college. Additionally, demographic differences are evident, with higher dropout rates among certain racial and ethnic groups. For example, [Black and Native American students](https://nces.ed.gov/programs/coe/indicator/ctr/undergrad-retention-graduation) have higher dropout rates compared to [Asian students](https://nces.ed.gov/programs/coe/indicator/ctr/undergrad-retention-graduation), who tend to have the lowest dropout rates among all racial groups.

These trends highlight the complexity of the dropout issue, influenced by economic, institutional, and demographic factors. This data underscores the need for targeted interventions to support at-risk student populations and improve overall graduation rates.

### Research Question
Can an undergraduate student’s academic success be predicted based on several factors using Log-Log or Power-Log relationships?

### Data Source
The data can be found here:[Kaggle Dataset](https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention).

The dataset offers an overview of students enrolled in various undergraduate programs at a higher education institution. It encompasses demographic data, socioeconomic factors, and academic performance details, facilitating the analysis of potential predictors of student dropout and academic success. The dataset includes multiple separate databases with pertinent information available at enrollment, such as application mode, marital status, and chosen course. Moreover, it allows for the estimation of overall student performance at the end of each semester by evaluating credited, enrolled, assessed, and approved curricular units along with their respective grades. Additionally, regional economic indicators like unemployment rate, inflation rate, and GDP are included to explore how economic factors influence student dropout rates and academic success. This comprehensive analysis tool provides valuable insights into the factors that motivate students to either persist in their studies or withdraw, across a diverse array of disciplines including agronomy, design, education, nursing, journalism, management, social services, and technologies.

### Methodology
**Data Preprocessing**: Applying logarithmic transformations to both dependent and independent variables helps in linearizing multiplicative relationships. For example, doubling study hours may not linearly double academic performance due to diminishing returns.

**Feature Identification and Preparation**: Key factors influencing academic success, such as study hours and attendance, are identified and prepared. Interaction terms are created to capture the combined effects of multiple factors.

**Model Training**: Linear regression models are trained on log-transformed data to understand the elasticities and interaction effects among variables.

### Results
Upon analysis of the coefficients to understand the relationships, I found that coefficients represent elasticities; and, the intercept represents the expected log of academic success when all log-transformed factors are zero (which corresponds to the multiplicative constant in the original non-logarithmic scale). The insights gained from analysis can help in understanding how various factors combine and contribute to academic success in a non-linear, multiplicative manner, providing a more nuanced understanding that can inform targeted interventions and support strategies.

### Outline of project

- [Link to notebook 1]()

### Next steps
**Model Validation:**
Validate the model using cross-validation techniques to ensure robustness.
Compare the performance of the log-log model with other models, such as polynomial regression or non-linear models.

**Reporting and Visualization:**
Create visualizations to illustrate the relationships between variables and academic success.
    
**Implementation and Further Research:**
Prepare a comprehensive report summarizing the findings, including key insights and potential recommendations for interventions.Conduct further research to explore additional factors or to validate findings in different educational contexts or datasets.

#### Contact and Further Information
Name: Nate Mauer

Email: n8mauer@gmail.com

LinkedIn: https://www.linkedin.com/in/natemauer/
