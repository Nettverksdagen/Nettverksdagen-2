<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Rediger Viktig informasjon</h1>

    <label class="block mb-2">Tittel</label>
    <input v-model="title" class="border p-2 w-full mb-4"/>

    <label class="block mb-2">Informasjonspunkter</label>
    <div v-for="(item, index) in items" :key="index" class="flex gap-2 mb-2">
      <input v-model="items[index]" class="border p-2 w-full"/>
      <button @click="removeItem(index)" class="bg-red-500 text-white px-2 rounded">X</button>
    </div>

    <button @click="addItem" class="bg-blue-500 text-white px-3 py-1 rounded">Legg til punkt</button>

    <hr class="my-6"/>

    <button @click="saveChanges" class="bg-green-600 text-white px-4 py-2 rounded">
      Lagre endringer
    </button>

    <h2 class="text-xl font-semibold mt-6 mb-2">Forhåndsvisning</h2>
    <InfoBox :title="title" :items="items" />
  </div>
</template>

<script>
import { reactive } from "vue";
import InfoBox from "@/components/anon/InfoBox.vue";

export default {
  name: "InfoboxAdminView",
  components: { InfoBox },
  setup() {
    const state = reactive({
      title: localStorage.getItem("infobox_title") || "Viktig informasjon",
      items: JSON.parse(localStorage.getItem("infobox_items") || "[]")
    });

    function addItem() {
      state.items.push("");
    }

    function removeItem(index) {
      state.items.splice(index, 1);
    }

    function saveChanges() {
      localStorage.setItem("infobox_title", state.title);
      localStorage.setItem("infobox_items", JSON.stringify(state.items));
      alert("Lagret!");
    }

    return { ...state, addItem, removeItem, saveChanges };
  }
};
</script>
