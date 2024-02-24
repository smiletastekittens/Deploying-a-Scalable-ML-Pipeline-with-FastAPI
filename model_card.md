# Model Card

## Model Details
This is a standard logistic regression model with default hyperparameters that predicts if an individual makes more or less than $50,000 as a yearly salary.    The model was generated using Scikit Learn.

## Intended Use
The intended use of this model is for research and ML devops testing purposes as the model was originally created as part of the Udacity Machine Learning DevOps nanodegree course.  Use of this model in production is inadvisable.

## Training Data
The model was trained on data from the UCI Census Income Dataset which originated from the 1994 census database.  This dataset includes respondent's demographic data, such as gender, age, marital status, and occupation, as well as their yearly income.  Categorical features were processed through a one-hot encoder, and labels were processed through a label binarizer.

## Evaluation Data
The evaluation data was comprised of a train / test split, where 25% of the testing data was taken from the dataset (as per Scikit Learn's default parameters).  Testing data was processed using the same methodology as training data.

## Metrics
_Please include the metrics used and your model's performance on those metrics._
The metrics used to evaluate this model were precision, recall, and F1 score.  The results are as follows:

Precision: 0.7285
Recall: 0.2635
F1: 0.3870

## Ethical Considerations
The training dataset contains a disproportionate amount of White males, which may bias the model toward more accurate predictions for that demographic than others.  Additionally, respondents with The United States as their native country are also disproportionately represented in the training data, and as such there may be bias against predictions for non-American individuals.

## Caveats and Recommendations
It is inadvisable to perform any manner of actionable prediction with this model due to its poor performance and uncorrected bias in the training data.  However, this model would make a great placeholder model that can be used when developing and testing machine learning pipelines.