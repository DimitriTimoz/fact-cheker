# Use a newer base image with a compatible GLIBC version
FROM rust:1.80 as builder

WORKDIR /usr/src/crawler
COPY . .

RUN cargo build --release

FROM debian:bookworm-slim


COPY --from=builder /usr/src/crawler/target/release/crawler /usr/local/bin/crawler
WORKDIR /usr/src
COPY ./newspapers.json /usr/src/newspapers.json
CMD ["crawler"]
