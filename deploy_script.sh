#!/usr/bin/env sh
set -eu
: "${KUBE_CONTEXT:?Set explicit KUBE_CONTEXT}"
: "${1:?Pass immutable image reference}"
kubectl --context "$KUBE_CONTEXT" apply -f k8s/namespace.yaml
kubectl --context "$KUBE_CONTEXT" apply -f k8s/zookeeper.yaml -f k8s/kafka.yaml
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status statefulset/zookeeper --timeout=300s
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status statefulset/kafka --timeout=600s
# Постоянное приложение разворачивается именно как Deployment.
kubectl --context "$KUBE_CONTEXT" set image --local -f kafka-demo-deployment.yaml \
  "kafka-demo=$1" -o yaml | kubectl --context "$KUBE_CONTEXT" apply -f -
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status deployment/kafka-demo --timeout=180s
kubectl --context "$KUBE_CONTEXT" -n kafka-homework logs deployment/kafka-demo --tail=10
