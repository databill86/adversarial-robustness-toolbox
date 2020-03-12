import pytest
import logging
import numpy as np
from art.attacks import BoundaryAttack
import unittest
from tests.attacks.utils import backend_targeted_tabular, backend_untargeted_tabular, backend_targeted_images
from tests.attacks.utils import back_end_untargeted_images, backend_test_classifier_type_check_fail

from art.utils import random_targets

from tests.utils import TestBase
from tests.utils import get_image_classifier_tf, get_image_classifier_kr, get_image_classifier_pt
from tests.utils import get_tabular_classifier_tf, get_tabular_classifier_kr, get_tabular_classifier_pt

logger = logging.getLogger(__name__)


@pytest.fixture()
def fix_get_mnist_subset(get_mnist_dataset):
    (x_train_mnist, y_train_mnist), (x_test_mnist, y_test_mnist) = get_mnist_dataset
    n_train = 10
    n_test = 10
    yield (x_train_mnist[:n_train], y_train_mnist[:n_train], x_test_mnist[:n_test], y_test_mnist[:n_test])


@pytest.mark.parametrize("clipped_classifier, targeted", [(True, True), (True, False), (False, True), (False, False)])
def test_tabular(get_tabular_classifier_list, framework, get_iris_dataset, clipped_classifier, targeted):
    classifier_list = get_tabular_classifier_list(BoundaryAttack, clipped=clipped_classifier)
    if classifier_list is None:
        logging.warning("Couldn't perform  this test because no classifier is defined")
        return

    for classifier in classifier_list:

        attack = BoundaryAttack(classifier, targeted=targeted, max_iter=10)
        if targeted:
            backend_targeted_tabular(attack, get_iris_dataset)
        else:
            backend_untargeted_tabular(attack, get_iris_dataset, clipped=clipped_classifier)


@pytest.mark.parametrize("targeted", [True, False])
def test_images(fix_get_mnist_subset, get_image_classifier_list_for_attack, framework, targeted):
    classifier_list = get_image_classifier_list_for_attack(BoundaryAttack)
    if classifier_list is None:
        logging.warning("Couldn't perform  this test because no classifier is defined")
        return

    for classifier in classifier_list:

        attack = BoundaryAttack(classifier=classifier, targeted=targeted, max_iter=20)
        if targeted:
            backend_targeted_images(attack, fix_get_mnist_subset)
        else:
            back_end_untargeted_images(attack, fix_get_mnist_subset, framework)


def test_classifier_type_check_fail():
    backend_test_classifier_type_check_fail(BoundaryAttack)