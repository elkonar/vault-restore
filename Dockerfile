FROM hashicorp/vault:2.0.2

USER root

RUN apk add --no-cache curl jq python3

RUN apk update && apk add --no-cache \
    curl \
    ca-certificates \
    gcompat && \
    update-ca-certificates && \
    curl -LO "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/
