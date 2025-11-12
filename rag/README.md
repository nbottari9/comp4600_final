# RAG Building pipeline

## `fetch-data`

Usage: ./fetch-data.sh <links-file>
- Arg 1: File with newline seperated links. URLs used for downloading.

## `vectorize`

Usage: ./vectorize.sh <mode> <directory OR oci-image-name>

- Arg 1: Vectorization mode
    - `local` - Store vectorized data locally on the device (Windows/Linux)
    - `local-mac` - Same as local but for Macs
    - `ECR` - Vectorize and push to ECR registry

## `build-rag`

Usage: ./build-rag <links-file> <mode> <directory OR oci-image-name>

Args are a compound of the scripts above. Check above.


