from sklearn.linear_model import LogisticRegression

from cuisines import *


def construct_model(x: list[bool], y: bool) -> LogisticRegression:
    """
    Constructs a logistic regression model using the training data.
    
    @param  x   one-hot representation of ingredient presence (always exactly 3 trues)
    @param  y   is this an example of the cuisine?
    @return     logistic regression model which attempts to fit x and y
    """
    ...

