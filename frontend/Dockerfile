FROM node as base
RUN mkdir frontend
WORKDIR /frontend
ADD . /frontend/
RUN ["npm", "install"]

FROM base as builder
COPY . . 
RUN npm run build
