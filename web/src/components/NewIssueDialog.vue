<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="800px"
    >
      <template v-slot:activator="{ on, attrs}">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          New Issue
        </v-btn>
      </template>
      <IssueDetailsCard
          title="Add new Ethical Issue / Flag"
          submit-button-text="Add"
          reset-button-text="Cancel"
          v-on:issueSubmit="onIssueAdded"
          v-on:issueReset="onIssueReset"
      ></IssueDetailsCard>
    </v-dialog>
  </v-row>
</template>

<script>
import IssueDetailsCard from "@/components/IssueDetailsCard";

export default {
  name: 'NewIssueDialog',
  components: { IssueDetailsCard },
  data: () => ({
    dialog: false,
  }),
  methods: {
    onIssueAdded(newIssueData) {
      this.$emit('newIssue', newIssueData)
      this.dialog = false
    },
    onIssueReset() {
      this.dialog = false
    }
  }
}
</script>