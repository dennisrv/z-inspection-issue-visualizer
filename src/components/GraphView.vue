<template>
  <v-container fluid fill-height>
    <v-row>
      <v-col col-3>
        <v-btn elevation="2" v-on:click="addNode"></v-btn>
      </v-col>
      <v-col col-9>
        <cytoscape ref="cy" :config="this.cytoscapeConfig" :preConfig="preConfig" :afterCreated="afterGraphCreated">
          <cy-element
              v-for="def in this.elements"
              :key="`${def.data.id}`"
              :definition="def"
          />
        </cytoscape>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// change eslint rule according to  https://github.com/vuejs/eslint-plugin-vue/issues/1004#issuecomment-568978285
// so it does not fail the dev build for this "unused" variable
import dagre from "cytoscape-dagre"

export default {
  name: 'GraphView',
  data: () => ({
    $cy: {},
    cytoscapeLayout: {},
    cytoscapeLayoutConfig: {
      name: 'dagre',
      rankDir: 'LR'
    },
    cytoscapeConfig: {
      autoRefreshLayout: true,
      style: [
        {
          selector: 'node',
          style: {
            'content': 'data(label)',
            'height': '50%',
            'width': '130%',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-wrap': 'wrap',
            'text-max-width': '80%',
            'font-size': '11pt'
          }
        },
        {
          selector: 'edge',
          style: {
            'curve-style': 'taxi',
            'taxi-direction': 'horizontal'
          }
        }
      ]
    },
    nodes: [
      {data: {id: 'a', label: 'a'}},
      {data: {id: 'b', label: 'b'}}
    ],
    edges: [
      {data: {id: 'ab', source: 'a', target: 'b'}}
    ]
  }),
  computed: {
    elements: function() {
      return this.nodes.concat(this.edges)
    }
  },
  methods: {
    // inspired by https://github.com/rcarcasses/vue-cytoscape-cola/blob/master/src/App.vue
    preConfig(cytoscape) {
      cytoscape.use(dagre)
      // overwrite default height of component
      let el = document.getElementById('cytoscape-div')
      el.setAttribute('style', 'height: 95vh')
    },
    async afterGraphCreated(cy) {
      // sometimes the layout is not rendering correctly, this solves it
      // see https://github.com/rcarcasses/vue-cytoscape/issues/17
      await cy.instance
      this.$cy = cy
      this.$cy.layout(this.cytoscapeLayoutConfig).run()
    },
    async addNode() {
      let n = Math.floor(Math.random() * 10) + 1
      let newNode = {data: {id: ''+n, label: ''+n}}
      let newEdge = {data: {id: 'a'+n, source: 'a', target: ''+n}}
      this.nodes.push(newNode)
      this.edges.push(newEdge)

      await this.$nextTick()
      this.$cy.layout(this.cytoscapeLayoutConfig).run()
    }
  },
  created() {
    console.log('created')
  },
}
</script>

