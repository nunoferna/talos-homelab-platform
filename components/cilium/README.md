# Cilium

This directory records generic Talos-specific Cilium configuration. It is not
deployable until a stable chart version compatible with Kubernetes 1.37 is
pinned in a reviewed `HelmRelease`.

`values-talos.yaml` follows Cilium's Talos guidance:

- Kubernetes host-scope IPAM
- kube-proxy replacement
- Talos' existing cgroup v2 mount
- the node-local KubePrism endpoint
- the reduced Linux capability set required on Talos
- legacy host routing required for Talos host-DNS forwarding

The corresponding Talos machine configuration must set
`cluster.network.cni.name: none` and `cluster.proxy.disabled: true`. Those
machine-level changes belong to the foundation repository and must be delivered
only during the reviewed CNI cutover.

Do not place migration pod CIDRs, LAN addresses, API endpoints, or temporary
policy-disable overrides in this public repository. The private live repository
owns those values.

Before adding a release:

1. Confirm the stable Cilium compatibility matrix includes Kubernetes 1.37.
2. Pin the OCI chart version and immutable digest.
3. Verify its signature.
4. Render the chart and review all cluster-scoped permissions.
5. Validate the day-0 installation and Flux adoption use identical values.
