from builtins import range
import sys
sys.path.insert(1,"../../../")
import h2o
from tests import pyunit_utils
from h2o.estimators.deeplearning import H2ODeepLearningEstimator


def offset_init_train_deeplearning():
    # Connect to a pre-existing cluster
    cars = h2o.upload_file(pyunit_utils.locate("smalldata/junit/cars_20mpg.csv"))
    cars = cars[cars["economy_20mpg"].isna() == 0]
    offset = h2o.H2OFrame([[.5]]*398)
    offset.set_names(["x1"])
    cars = cars.cbind(offset)

    # offset_column passed in the train method
    dl_train = H2ODeepLearningEstimator(hidden=[20, 20], epochs=10)
    dl_train.train(x=list(range(2, 8)), y="economy_20mpg", training_frame=cars, offset_column="x1")
    predictions_train = dl_train.predict(cars)

    # test offset_column passed in estimator init
    dl_init = H2ODeepLearningEstimator(hidden=[20, 20], epochs=10, offset_column="x1")
    dl_init.train(x=list(range(2, 8)), y="economy_20mpg", training_frame=cars)
    predictions_init = dl_init.predict(cars)

    # case the both offset column parameters are set and only the parameter in train will be used
    dl_init_train = H2ODeepLearningEstimator(hidden=[20, 20], epochs=10, offset_column="x1")
    dl_init_train.train(x=list(range(2, 8)), y="economy_20mpg", training_frame=cars, offset_column="x1")
    predictions_init_train = dl_init_train.predict(cars)

    assert predictions_train == predictions_init, "Expected predictions of a model with offset_column in train method has to be same as predictions of a model with offset_column in constructor."
    assert predictions_train == predictions_init_train, "Expected predictions of a model with offset_column in train method has to be same as predictions of a model with offset_column in both constructor and init."


if __name__ == "__main__":
    pyunit_utils.standalone_test(offset_init_train_deeplearning)
else:
    offset_init_train_deeplearning()
