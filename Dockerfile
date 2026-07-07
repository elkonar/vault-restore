FROM hashicorp/vault:2.0

USER root

RUN apk add --no-cache curl jq

RUN apk update && apk add --no-cache \
    curl \
    ca-certificates \
    gcompat && \
    update-ca-certificates && \
    curl -LO "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/
