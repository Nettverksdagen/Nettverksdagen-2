FROM node:22 AS base
RUN mkdir /frontend
RUN chown node:node /frontend
WORKDIR /frontend
COPY . /frontend/
# COPY node_modules /frontend/
# COPY package.json /frontend/
# COPY package-lock.json /frontend/
# RUN ["npm", "install"]

FROM base AS builder
ENV NODE_ENV production
COPY --from=base /frontend /frontend
WORKDIR /frontend
RUN ["npm", "install", "&&", "npm", "run", "build"]
