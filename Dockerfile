# TODO: use different docker context. now only using binary (therefore python-specific context not necessary)

FROM python:3

# Add docker-compose-wait tool
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

COPY ./dist/gantree_node_watchdog /watchdog/gantree_node_watchdog
WORKDIR /watchdog

CMD ["/watchdog/gantree_node_watchdog"]
