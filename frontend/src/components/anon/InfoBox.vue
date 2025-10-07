<template>
  <div class="p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded-md shadow-md w-full max-w-4xl mx-auto my-6">
    <h2 class="text-xl font-bold mb-2">{{ title }}</h2>
    <div v-if="paragraph" class="list-disc pl-5 text-gray-700 space-y-1">
      {{paragraph}}
    </div>
    <p v-else class="text-gray-500 italic">Ingen informasjon la ennå…</p>
  </div>
</template>

<script>
export default {
  name: "InfoBox",
  props: {
    title: {
      type: String,
      default: "Viktig informasjon"
    },
    paragraph: {
      type: String,
      default: "" //"Ingen informasjon la ennå…"
    }
  },
};
</script>
