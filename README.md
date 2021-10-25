### Build Image

```
docker build -f Docker/dev/Dockerfile -t <myimage:mytag> . 
```

### Running unit tests

```
docker run --rm <myimage:mytag> pytest
```