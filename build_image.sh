#!/bin/bash -e
image_name="demotto/kfserving-controller"
image_tag="0.2.1"
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker push "$full_image_name"

# Output the strict image name (which contains the sha256 image digest)
#docker inspect --format="{{index .RepoDigests 0}}" "${IMAGE_NAME}"
