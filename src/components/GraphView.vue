<template>
  <v-container fluid fill-height>
    <v-row>
      <v-col cols="9">
        <cytoscape ref="cytoscape-component" :config="this.cytoscapeConfig" :preConfig="preConfig" :afterCreated="afterGraphCreated">
          <cy-element
              v-for="def in this.elements"
              :key="`${def.data.id}`"
              :definition="def"
          />
        </cytoscape>
      </v-col>
      <v-col cols="3">
        <NewIssueDialog @form-submit="formSubmit"></NewIssueDialog>
        <v-btn elevation="2" v-on:click="addNode"></v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// change eslint rule according to  https://github.com/vuejs/eslint-plugin-vue/issues/1004#issuecomment-568978285
// so it does not fail the dev build for this "unused" variable
import dagre from "cytoscape-dagre"
import { initialNodes, initialEdges } from '@/plugins/initialGraphData'
import NewIssueDialog from '@/components/NewIssueDialog'

export default {
  name: 'GraphView',
  components: {
    NewIssueDialog
  },
  data: () => ({
    $cy: {},
    loading: true,
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
        },
        {
          selector: '.principle',
          style: {
            'height': '80%',
            'width': '210%',
            'background-color': '#7C96ED',
            'text-wrap': 'wrap',
            'text-max-width': '130%',
            'font-size': '18pt'
          }
        },
        {
          selector: '.requirement',
          style: {
            'height': '60%',
            'width': '160%',
            'background-color': '#7CEDD3',
            'text-wrap': 'wrap',
            'text-max-width': '100%',
            'font-size': '14pt'
          }
        },
        {
          selector: '.sub-requirement',
          style: {
            'background-color': '#96ED7C'
          }
        }
      ]
    },
    nodes: initialNodes,
    edges: initialEdges
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
      let newEdge = {data: {id: 'a'+n, source: 'fairness', target: ''+n}}
      this.nodes.push(newNode)
      this.edges.push(newEdge)

      await this.$nextTick()
      this.$cy.layout(this.cytoscapeLayoutConfig).run()
    },
    formSubmit(formData) {
      console.log(formData)
    }
  },
}
</script>

