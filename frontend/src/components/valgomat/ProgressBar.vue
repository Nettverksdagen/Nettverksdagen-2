<template>
    <div class="progress-container">
      <div class="progress">
        <div
          class="progress-bar"
          :style="{ width: progress + '%' }"
          role="progressbar"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {{ Math.round(progress) }}%
        </div>
      </div>
    </div>
</template>

<script>
export default {
  props: {
    progress: {
      type: Number,
      required: true
    }
  }
}
</script>

<style scoped>
.progress-container {
    margin: 20px 0;
}

.progress {
    height: 20px;
    background-color: #f3f3f3;
    border-radius: 5px;
    overflow: hidden;
}

.progress-bar {
    background-color: #14403C;
    text-align: center;
    line-height: 20px;
    color: white;
    font-weight: bold;
}
</style>
