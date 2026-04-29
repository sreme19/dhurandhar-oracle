"""
hmm.py — Hidden Markov Model (Viterbi + forward-backward + Baum-Welch EM).

Ported and adapted from got-oracle/got_oracle/optimisation/hmm.py.
Same algorithm, new domain: hidden states are loyalty levels
(loyal | wavering | compromised | turned) instead of GoT power states.

Public API:
  HMMParams            — (A, B, pi) parameter bundle
  viterbi(p, obs)      — most likely hidden state sequence
  forward_backward(p, obs) — posterior marginals P(z_t | obs)
  baum_welch(p, seqs)  — EM parameter re-estimation from multiple sequences
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class HMMParams:
    """
    HMM parameter bundle.
    A:  |S|×|S|  transition matrix          A[i,j] = P(z_t=j | z_{t-1}=i)
    B:  |S|×|O|  emission matrix            B[i,k] = P(x_t=k | z_t=i)
    pi: |S|       initial state distribution
    """
    A:  np.ndarray   # (n_hidden, n_hidden)
    B:  np.ndarray   # (n_hidden, n_obs)
    pi: np.ndarray   # (n_hidden,)

    @classmethod
    def uniform(cls, n_hidden: int, n_obs: int) -> "HMMParams":
        """Initialise with uniform distributions."""
        A  = np.ones((n_hidden, n_hidden)) / n_hidden
        B  = np.ones((n_hidden, n_obs))    / n_obs
        pi = np.ones(n_hidden)             / n_hidden
        return cls(A=A, B=B, pi=pi)

    def _normalise(self) -> "HMMParams":
        A  = self.A  / (self.A.sum(axis=1, keepdims=True) + 1e-300)
        B  = self.B  / (self.B.sum(axis=1, keepdims=True) + 1e-300)
        pi = self.pi / (self.pi.sum() + 1e-300)
        return HMMParams(A=A, B=B, pi=pi)


def viterbi(
    params: HMMParams,
    obs: list[int],
) -> tuple[list[int], float]:
    """
    Viterbi algorithm: most likely hidden state sequence.

    Returns:
      path:     list of hidden state indices (length == len(obs))
      log_prob: log probability of the most likely path
    """
    params = params._normalise()
    T = len(obs)
    n = params.A.shape[0]

    log_A  = np.log(params.A  + 1e-300)
    log_B  = np.log(params.B  + 1e-300)
    log_pi = np.log(params.pi + 1e-300)

    delta   = np.full((T, n), -np.inf)
    psi     = np.zeros((T, n), dtype=int)

    delta[0] = log_pi + log_B[:, obs[0]]

    for t in range(1, T):
        for j in range(n):
            scores        = delta[t - 1] + log_A[:, j]
            psi[t, j]     = int(np.argmax(scores))
            delta[t, j]   = scores[psi[t, j]] + log_B[j, obs[t]]

    # Backtrack
    path = [int(np.argmax(delta[T - 1]))]
    for t in range(T - 1, 0, -1):
        path.insert(0, psi[t, path[0]])

    return path, float(delta[T - 1, path[-1]])


def forward_backward(
    params: HMMParams,
    obs: list[int],
) -> np.ndarray:
    """
    Forward-backward algorithm: posterior marginals P(z_t = i | obs).

    Returns:
      gamma: (T, n_hidden) array of posterior marginals
    """
    params = params._normalise()
    T = len(obs)
    n = params.A.shape[0]

    # Forward pass (scaled)
    alpha = np.zeros((T, n))
    scale = np.zeros(T)
    alpha[0] = params.pi * params.B[:, obs[0]]
    scale[0] = alpha[0].sum() + 1e-300
    alpha[0] /= scale[0]

    for t in range(1, T):
        alpha[t] = (alpha[t - 1] @ params.A) * params.B[:, obs[t]]
        scale[t] = alpha[t].sum() + 1e-300
        alpha[t] /= scale[t]

    # Backward pass (scaled)
    beta = np.zeros((T, n))
    beta[T - 1] = 1.0

    for t in range(T - 2, -1, -1):
        beta[t] = (params.A * (params.B[:, obs[t + 1]] * beta[t + 1])).sum(axis=1)
        beta[t] /= scale[t + 1]

    gamma = alpha * beta
    gamma /= gamma.sum(axis=1, keepdims=True) + 1e-300

    return gamma


def baum_welch(
    params: HMMParams,
    sequences: list[list[int]],
    n_iter: int = 20,
) -> HMMParams:
    """
    Baum-Welch EM: re-estimate (A, B, pi) from multiple observation sequences.

    Args:
      params:    Initial HMMParams (e.g. from HMMParams.uniform)
      sequences: List of observation sequences (each a list of int obs indices)
      n_iter:    Number of EM iterations

    Returns:
      Updated HMMParams
    """
    n = params.A.shape[0]
    n_obs = params.B.shape[1]

    for _ in range(n_iter):
        # Accumulators
        pi_acc  = np.zeros(n)
        A_acc   = np.zeros((n, n))
        B_acc   = np.zeros((n, n_obs))

        for obs in sequences:
            T     = len(obs)
            gamma = forward_backward(params, obs)
            # Need alpha, beta for xi — re-compute (TODO: refactor to avoid duplication)
            alpha = np.zeros((T, n))
            scale = np.zeros(T)
            alpha[0] = params.pi * params.B[:, obs[0]]
            scale[0] = alpha[0].sum() + 1e-300
            alpha[0] /= scale[0]
            for t in range(1, T):
                alpha[t] = (alpha[t - 1] @ params.A) * params.B[:, obs[t]]
                scale[t] = alpha[t].sum() + 1e-300
                alpha[t] /= scale[t]

            beta = np.zeros((T, n))
            beta[T - 1] = 1.0
            for t in range(T - 2, -1, -1):
                beta[t] = (params.A * (params.B[:, obs[t + 1]] * beta[t + 1])).sum(axis=1)
                beta[t] /= scale[t + 1]

            # xi[t,i,j] = P(z_t=i, z_{t+1}=j | obs)
            xi = np.zeros((T - 1, n, n))
            for t in range(T - 1):
                xi[t] = (alpha[t][:, None] * params.A
                         * (params.B[:, obs[t + 1]] * beta[t + 1])[None, :])
                xi[t] /= xi[t].sum() + 1e-300

            pi_acc  += gamma[0]
            A_acc   += xi.sum(axis=0)
            for k in range(n_obs):
                mask = np.array([o == k for o in obs], dtype=float)
                B_acc[:, k] += (gamma * mask[:, None]).sum(axis=0)

        # M-step: normalise
        params = HMMParams(
            A=A_acc  / (A_acc.sum(axis=1,  keepdims=True) + 1e-300),
            B=B_acc  / (B_acc.sum(axis=1,  keepdims=True) + 1e-300),
            pi=pi_acc / (pi_acc.sum() + 1e-300),
        )

    return params
