# Jason Stys: derived non-root-only PostgreSQL lab image; remove unused vulnerable root-switch helper.
# BASE: exact official PostgreSQL image digest below. Runtime user: postgres; no root entrypoint path supported.
FROM postgres:18-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873
USER root
# gosu is only used by the upstream entrypoint when started as root; this lab always starts as postgres.
# This removes the unused component rather than ignoring its vulnerability findings.
RUN rm /usr/local/bin/gosu
USER postgres
