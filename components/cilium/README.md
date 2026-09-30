# Cilium

This directory records generic Talos-specific Cilium configuration. Cilium
1.20.2 is pinned after explicit operator acceptance of its Kubernetes 1.37
compatibility risk; upstream's guaranteed matrix for this release ends at 1.36.

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

Before installing or changing the release:

1. Reconfirm the upstream compatibility matrix and documented risk acceptance.
2. Verify the pinned OCI manifest digest and downloaded chart checksum.
3. Verify the signature against the pinned issuer and identity expression.
4. Render the chart and review all cluster-scoped permissions.
5. Validate the day-0 installation and Flux adoption use identical values.
