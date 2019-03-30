FROM alpine
RUN apk update
RUN apk add --no-cache openssh
RUN apk add --no-cache openssh-client
COPY sshconf/* /root/.ssh/
ADD https://github.com/sigtot/nvdagen-github-bot/releases/download/0.1/github-bot-alpine /bin/github-bot
RUN chmod +x /bin/github-bot
CMD github-bot
