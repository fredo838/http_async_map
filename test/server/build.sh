TAG=$(date +%s )
TAG="unchanged"
echo ${TAG}
docker build -t dev.local/sleep:${TAG} -f Dockerfile .
echo ${TAG}
# docker run --name sleep --rm sleep
# minikube image load dev.local/sleep:${TAG} -p knative
kn service update sleep \
  --image dev.local/sleep:${TAG} \
  --port 8000 \
  --concurrency-limit 1 \
  --scale-metric concurrency \
  --scale-window 6s