<template>
  <v-app>
   <!-- Sizes your content based upon application components -->
    <v-main>
      <v-container fluid>

        <!-- If using vue-router -->
        <GraphView></GraphView>
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
import GraphView from './components/GraphView';

export default {
  name: 'App',

  components: {
    GraphView,
  },
};
</script>
