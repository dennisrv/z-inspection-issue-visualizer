<template>
  <v-container fluid fill-height>
    <v-row>
      <v-col cols="9">
        <!--    cytoscape core instance is now available at this.$refs['cytoscape-component']    -->
        <cytoscape ref="cytoscape-component" :config="this.cytoscapeConfig" :preConfig="preConfig" :afterCreated="afterGraphCreated">
          <cy-element
              v-for="def in this.elements"
              :key="`${def.data.id}`"
              :definition="def"
          />
        </cytoscape>
      </v-col>
      <v-col cols="3">
        <!--    newIssue event is emitted by the component when click on submit happens   -->
        <NewIssueDialogButton v-on:newIssue="onNewIssue"></NewIssueDialogButton>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// change eslint rule according to  https://github.com/vuejs/eslint-plugin-vue/issues/1004#issuecomment-568978285
// so it does not fail the dev build for this "unused" variable
import dagre from "cytoscape-dagre"
import { initialNodes, initialEdges } from '@/constants/initialGraphData'
import cytoscapeStyle from "@/constants/cytoscapeStyle";

import { toId, createNode, createEdge } from "@/util/graphUtils";

import NewIssueDialogButton from '@/components/NewIssueDialog'

export default {
  name: 'GraphView',
  components: {
    NewIssueDialogButton
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
      style: cytoscapeStyle
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
    async onNewIssue(newNodeData) {

      let id = toId(newNodeData.issueTitle + Math.floor(Math.random() * 1000))
      let newNode = createNode(newNodeData.issueTitle, newNodeData.issueType, id)

      let newEdges = Object.values(newNodeData.related).map((rel) => createEdge(rel.subRequirement, id))

      this.nodes.push(newNode)
      this.edges.push(...newEdges)

      await this.$nextTick()
      this.$cy.layout(this.cytoscapeLayoutConfig).run()
    },
  },
}
</script>

