# Talos homelab platform

Public, reusable Kubernetes platform resources for a Talos Linux homelab. This
repository is a component catalog; it is not a live Flux reconciliation root.

The private live repository selects reviewed commits from this repository and
provides environment-specific values. Do not add internal addresses, DNS names,
hardware identifiers, credentials, cluster history, or recovery material here.

## Dependency and bootstrap order

1. Cilium, permanently managed by OpenTofu in the public foundation repository
2. Flux, which begins reconciliation of this platform catalog
3. persistent storage
4. OpenBao
5. External Secrets Operator
6. narrowly allowlisted SOPS exceptions
7. applications and namespace-scoped network policies

Cilium is a reviewed day-0 dependency because Flux requires working pod
networking. This repository must not contain a Cilium `HelmRelease` or otherwise
compete with OpenTofu for ownership.

## Cilium ownership

The public foundation repository contains the dedicated Cilium OpenTofu root,
the chart and values pins, and the separate encrypted state configuration. Flux
starts above this boundary and manages the remaining platform components.

## Validation

```sh
python -m pip install --requirement requirements-dev.txt
yamllint .
python scripts/check_public_boundary.py
```

CI scans Git history for secrets, validates YAML, rejects Kubernetes `Secret`
objects, and rejects common private-value patterns in platform manifests.
