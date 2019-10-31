from enum import Enum
from enum import unique

from garage.tf.optimizers import ConjugateGradientOptimizer
from garage.tf.optimizers import PenaltyLbfgsOptimizer

# Custom stuff
from quad_dynalearn.algos.npo import PGLoss
from quad_dynalearn.algos.npo import NPO

@unique
class KLConstraint(Enum):
    HARD = "hard"
    SOFT = "soft"


class TRPO(NPO):
    """
    Trust Region Policy Optimization.

    See https://arxiv.org/abs/1502.05477.
    """

    def __init__(self,
                 kl_constraint=KLConstraint.HARD,
                 optimizer=None,
                 optimizer_args=None,
                 **kwargs):
        if not optimizer:
            if kl_constraint == KLConstraint.HARD:
                optimizer = ConjugateGradientOptimizer
            elif kl_constraint == KLConstraint.SOFT:
                optimizer = PenaltyLbfgsOptimizer
            else:
                raise NotImplementedError("Unknown KLConstraint")

        if optimizer_args is None:
            optimizer_args = dict()

        super(TRPO, self).__init__(
            pg_loss=PGLoss.SURROGATE,
            optimizer=optimizer,
            optimizer_args=optimizer_args,
            name="TRPO",
            **kwargs)
