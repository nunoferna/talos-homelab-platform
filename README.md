# Talos homelab platform

Public, reusable Kubernetes platform resources for a Talos Linux homelab. This
repository is a component catalog; it is not a live Flux reconciliation root.

The private live repository selects reviewed commits from this repository and
provides environment-specific values. Do not add internal addresses, DNS names,
hardware identifiers, credentials, cluster history, or recovery material here.

## Bootstrap order

1. Cilium
2. Flux
3. persistent storage
4. OpenBao
5. External Secrets Operator
6. narrowly allowlisted SOPS exceptions
7. applications and namespace-scoped network policies

Cilium is installed once as a reviewed day-0 operation because Flux requires
working pod networking. Flux then adopts the identical release and values.

## Current compatibility gate

The target cluster runs Kubernetes 1.37.0. Stable Cilium 1.20.2 guarantees
compatibility only through Kubernetes 1.36, while Cilium 1.21 is prerelease.
This repository intentionally contains no deployable Cilium release until a
stable version explicitly lists Kubernetes 1.37 in its tested matrix.

The generic Talos values are recorded in
[`components/cilium/values-talos.yaml`](components/cilium/values-talos.yaml).
They do not include a chart version or environment-specific migration values.

## Validation

```sh
python -m pip install --requirement requirements-dev.txt
yamllint .
python scripts/check_public_boundary.py
```

CI scans Git history for secrets, validates YAML, rejects Kubernetes `Secret`
objects, and rejects common private-value patterns in platform manifests.
