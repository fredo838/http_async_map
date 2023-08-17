# kn service create sleep --image ghcr.io/knative/helloworld-go:latest
  
kn service update sleep \
  --image dev.local/sleep:1692276786 \
  --port 8080 \
  --concurrency-limit 1 \
  --scale-metric concurrency

