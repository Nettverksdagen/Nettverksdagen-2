<template>
    <Content>

        <div>
            <h1 class="text-center">Title</h1>

            <div class="container">
                <div class="two-thirds">
                    <h1 class="text-center">SmallTitle</h1>
                </div>
                <div class="one-third">
                    <div class="sub-box">
                        <p>Content for the first 1/3 sub-box</p>
                    </div>
                    <div class="sub-box">
                        <p>Content for the second 1/3 sub-box</p>
                    </div>
                    <div class="sub-box">
                        <p>Content for the third 1/3 sub-box</p>
                    </div>
                </div>
            </div>
        </div>
    </Content>
</template>



<script>
</script>



<style scoped lang="scss">
.container {
  display: flex;
  width: 100%;
}

.two-thirds {
  flex: 2;
  background-color: white;
  padding: 10px; /* Reduce padding for better space management */
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.one-third {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px; /* Reduce padding for better space management */
  overflow-y: auto; /* Enable vertical scrolling if content exceeds box height */
  max-height: 100%; /* Set a maximum height for the box */
}

.sub-box {
  flex: 1;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 10px; /* Reduce padding for better space management */
  margin-bottom: 10px;
  overflow-y: auto; /* Enable vertical scrolling if content exceeds box height */
}

</style>
