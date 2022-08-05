<template>
    <div style="width: 50%;margin: auto;">
        <center>
            <b-card class="change-color-div" align="center" style="background-color: #ccc;" border-variant="light" no-body>
                <!-- <b-card no-body bg-variant="light" border-variant="light"> -->
                <div class="h1 mb-0">
                    <b-icon icon="exclamation-triangle" variant="danger" style="width: 150px; height: 150px;"/>
                    <b-card-text class="text-danger">404 Page Not Found</b-card-text>
                </div>
                <!-- </b-card> -->
            </b-card>
        </center>
    </div>
</template>

<script>

  export default {
    name: 'NotFound'
  }

</script>

<style scoped>

  center {
    margin: 15vw;
  }

  h1 {
    color: var(--border);
    font-size: 2em;
  }

</style>