<template>
  <v-container fluid fill-height>
    <v-row>
      <v-col cols="8" class="grey lighten-5">
        <!--    cytoscape core instance is now available at this.$refs['cytoscape-component']    -->
        <cytoscape v-if="this.elements.length" ref="cytoscape-component" :config="this.cytoscapeConfig" :preConfig="preConfig"
                   :afterCreated="afterGraphCreated">
          <cy-element
              v-for="def in this.elements"
              :key="`${def.data.id}`"
              :definition="def"
          />
        </cytoscape>
      </v-col>
      <v-col cols="4">
        <v-row>
          <v-col cols="12">
            <!--    newIssue event is emitted by the component when click on submit happens   -->
            <NewIssueDialogButton v-on:newIssue="onNewIssue"></NewIssueDialogButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-divider></v-divider>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <IssueDetailsCard
                title="Selected Issue"
                submit-button-text="Update"
                reset-button-text="Reset"
                :initial-form-values="selectedIssueDetails"
                :form-values="selectedIssueDetails"
                v-on:issueSubmit="onIssueUpdate"
            ></IssueDetailsCard>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// change eslint rule according to  https://github.com/vuejs/eslint-plugin-vue/issues/1004#issuecomment-568978285
// so it does not fail the dev build for this "unused" variable
import dagre from "cytoscape-dagre"
import http from "@/plugins/http"
import cytoscapeStyle from "@/constants/cytoscapeStyle";

import {toId, createNode, createEdge} from "@/util/graphUtils";

import NewIssueDialogButton from '@/components/NewIssueDialog'
import IssueDetailsCard, {createEmptyIssueDetails} from '@/components/IssueDetailsCard'

export default {
  name: 'GraphView',
  components: {
    NewIssueDialogButton,
    IssueDetailsCard
  },
  data: () => ({
    $cy: {},
    cytoscapeLayoutConfig: {
      name: 'dagre',
      rankDir: 'RL'
    },
    cytoscapeConfig: {
      autoRefreshLayout: true,
      style: cytoscapeStyle
    },
    elements: [],
    selectedIssueDetails: createEmptyIssueDetails()
  }),
  methods: {
    // inspired by https://github.com/rcarcasses/vue-cytoscape-cola/blob/master/src/App.vue
    preConfig(cytoscape) {
      cytoscape.use(dagre)
      // overwrite default height of component
      let el = document.getElementById('cytoscape-div')
      el.setAttribute('style', 'height: 95vh; back')
    },
    async afterGraphCreated(cy) {
      // sometimes the layout is not rendering correctly, this solves it
      // see https://github.com/rcarcasses/vue-cytoscape/issues/17
      await cy.instance
      this.$cy = cy
      this.$cy.layout(this.cytoscapeLayoutConfig).run()
      this.$cy.on('select', '.issue-node', event => {
        this.selectedIssueDetails = event.target._private.data.issueDetails
      })
      this.$cy.on('unselect', '.issue-node', () => {
        if (this.$cy.$(':selected').length === 0) {
          this.selectedIssueDetails = createEmptyIssueDetails()
        }
      })
    },
    onNewIssue(newIssueData) {

      let id = toId(newIssueData.issueTitle + Math.floor(Math.random() * 1000))
      let newNode = createNode(newIssueData.issueTitle, newIssueData.issueType + " issue-node", id)
      newNode['data']['issueDetails'] = newIssueData

      let newEdges = Object.values(newIssueData.related).map((rel) => createEdge(rel.subRequirement, id))

      this.nodes.push(newNode)
      this.edges.push(...newEdges)

      // relayout only after the elements are drawn
      this.$nextTick().then(() => this.$cy.layout(this.cytoscapeLayoutConfig).run())
    },
    onIssueUpdate(updatedIssueData) {
      console.log(updatedIssueData)
    }
  },
  created() {
    http
        .get('/nodes')
        .then((response) => {
          let responseData = response.data

          if(responseData.status === "success") {
            this.elements = responseData.data.nodes.concat(responseData.data.edges)
          }
        })
  },
}
</script>

