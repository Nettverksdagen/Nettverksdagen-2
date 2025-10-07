import axios from "axios";

export const infobox = {
  namespaced: true,

  state: {
    infoboxes: [],
    loading: false,
    error: null,
  },

  getters: {
    allInfoboxes: (state) => state.infoboxes,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null,
  },

  mutations: {
    SET_INFOBOXES(state, infoboxes) {
      state.infoboxes = infoboxes;
    },
    ADD_INFOBOX(state, infobox) {
      state.infoboxes.push(infobox);
    },
    UPDATE_INFOBOX(state, updatedInfobox) {
      const index = state.infoboxes.findIndex((i) => i.id === updatedInfobox.id);
      if (index !== -1) {
        state.infoboxes.splice(index, 1, updatedInfobox);
      }
    },
    DELETE_INFOBOX(state, id) {
      state.infoboxes = state.infoboxes.filter((i) => i.id !== id);
    },
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
  },

  actions: {
    async fetchInfoboxes({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await axios.get("/api/infoboxes/");
        commit("SET_INFOBOXES", response.data);
      } catch (error) {
        commit("SET_ERROR", error);
        console.error("Feil ved henting av infobokser:", error);
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async createInfobox({ commit }, infobox) {
      try {
        const response = await axios.post("/api/infoboxes/", infobox);
        commit("ADD_INFOBOX", response.data);
      } catch (error) {
        commit("SET_ERROR", error);
        console.error("Feil ved oppretting:", error);
        throw error;
      }
    },

    async updateInfobox({ commit }, infobox) {
      try {
        const response = await axios.put(`/api/infoboxes/${infobox.id}/`, infobox);
        commit("UPDATE_INFOBOX", response.data);
      } catch (error) {
        commit("SET_ERROR", error);
        console.error("Feil ved oppdatering:", error);
        throw error;
      }
    },

    async deleteInfobox({ commit }, id) {
      try {
        await axios.delete(`/api/infoboxes/${id}/`);
        commit("DELETE_INFOBOX", id);
      } catch (error) {
        commit("SET_ERROR", error);
        console.error("Feil ved sletting:", error);
        throw error;
      }
    },
  },
};
