from numba import njit
from numpy import dot, eye, zeros

γ = 1.4
μ = 1e-2


@njit
def sigma(dv):
    return μ * (dv + dv.T - 2 / 3 * (dv[0, 0] + dv[1, 1] + dv[2, 2]) * eye(3))


@njit
def pressure(ρ, E, v):
    return ρ * (γ - 1) * (E - dot(v, v) / 2)


def F_navier_stokes(Q, dQ, d):

    ret = zeros(5)

    dv = dQ[:, 2:5]

    ρ = Q[0]
    E = Q[1] / ρ
    v = Q[2:5] / ρ

    p = pressure(ρ, E, v)
    σ = sigma(dv)

    vd = v[d]
    ρvd = ρ * vd

    ret[0] = ρvd
    ret[1] = ρvd * E + p * vd
    ret[2:5] = ρvd * v
    ret[2 + d] += p

    σd = σ[d]
    ret[1] -= dot(σd, v)
    ret[2:5] -= σd

    return ret
