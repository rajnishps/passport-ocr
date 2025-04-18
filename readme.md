<!-- build docker image -->

docker build -t passport-ocr .

<!-- run docker image -->

docker run -p 8000:8000 passport-ocr

<!-- run html file -->

python -m http.server 8001
