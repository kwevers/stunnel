FROM registry.access.redhat.com/ubi9/ubi-minimal:9.5-1731593028

RUN set -x \
  && microdnf -y install stunnel \
  && useradd -r stunnel

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
