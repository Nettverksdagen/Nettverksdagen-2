FROM node:10.23.0 as base
RUN mkdir /frontend
RUN chown node:node /frontend
WORKDIR /frontend
COPY package.json /frontend/
RUN ["npm", "install"]
COPY . /frontend/

FROM base as builder
ENV NODE_ENV production
COPY --from=base /frontend /frontend
WORKDIR /frontend
RUN ["npm", "run", "build"]
