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

## Pinned Cilium release

The target cluster runs Kubernetes 1.37.0. Cilium 1.20.2 guarantees compatibility
through Kubernetes 1.36; the operator independently validated and explicitly
accepted its use with Kubernetes 1.37. Treat that decision as a documented risk
acceptance, not as upstream support.

The generic Talos values are recorded in
[`components/cilium/values-talos.yaml`](components/cilium/values-talos.yaml).
The chart version, immutable OCI digest, downloaded-chart checksum, and signing
identity are pinned in [`components/cilium/release.yaml`](components/cilium/release.yaml).
Environment-specific migration values remain private.

## Validation

```sh
python -m pip install --requirement requirements-dev.txt
yamllint .
python scripts/check_public_boundary.py
```

CI scans Git history for secrets, validates YAML, rejects Kubernetes `Secret`
objects, and rejects common private-value patterns in platform manifests.
