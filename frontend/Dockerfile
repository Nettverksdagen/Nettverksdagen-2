FROM node as base
RUN mkdir /frontend
RUN chown node:node /frontend
WORKDIR /frontend
ADD . /frontend/
RUN ["npm", "install"]

FROM base as builder
ENV NODE_ENV production
COPY --from=base /frontend /frontend
WORKDIR /frontend
RUN ["npm", "run", "build"]
