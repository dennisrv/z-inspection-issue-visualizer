<template>
  <v-row justify="center">
    <v-dialog
        v-model="dialog"
        max-width="90vw"
    >
      <template v-slot:activator="{ on, attrs}">
        <v-btn
            color="warning"
            dark
            v-bind="attrs"
            v-on="on"
        >
          Merge Issues
        </v-btn>
      </template>
      <v-card v-if="this.issues.error">
        <v-card-title>
          <span class="text-h5">{{ this.issues.error }}</span>
        </v-card-title>
        <v-card-actions>
          <v-btn
              color="blue darken-1"
              text
              @click="dialog=false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-card v-else>
        <v-card-title>
          <span class="text-h5">Merge Issues</span>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="4" v-for="(issue, issueIndex) in [this.issue1, this.mergedIssue, this.issue2]" :key="issueIndex">
              <v-form :disabled="issueIndex !== 1" :ref="issueIndex === 1 ? 'issueForm' : ''" v-model="valid[issueIndex]">
                <v-text-field
                    v-model="issue.id"
                    v-show="false"
                ></v-text-field>
                <v-row dense>
                  <v-col cols="12">
                    <v-radio-group
                        v-model="issue.issueType"
                        label="Issue type"
                        row dense required
                    >
                      <v-radio v-for="opt in formOptions.issueType"
                               :key="opt.value"
                               :label="opt.label"
                               :value="opt.value"
                      />
                    </v-radio-group>
                  </v-col>
                  <v-col cols="12">
                    <v-combobox
                        v-model="issue.areas"
                        :items="formOptions.areas"
                        label="Related Areas"
                        multiple
                        chips
                        dense
                    ></v-combobox>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                        dense required
                        label="Title"
                        v-model="issue.issueTitle"
                        :rules="formRules.valueRequiredRule"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row dense v-for="(item, index) in issue.related" :key="index">
                  <v-col cols="10" dense>
                    <v-row dense>
                      <v-col cols="4">
                        <v-autocomplete
                            v-model="item.principle"
                            :items="constant.principles"
                            :label="`Related Ethical Principle ${index + 1}`"
                            dense required
                            :rules="formRules.valueRequiredRule"
                        ></v-autocomplete>
                      </v-col>
                      <v-col cols="4">
                        <v-autocomplete
                            v-model="item.requirement"
                            :items="constant.principlesRequirementsMap[item.principle]"
                            :label="`Related Key Requirement ${index + 1}`"
                            dense required
                            :rules="formRules.valueRequiredRule"
                        ></v-autocomplete>
                      </v-col>
                      <v-col cols="4">
                        <v-autocomplete
                            v-model="item.subRequirement"
                            :items="constant.requirementsSubrequirementsMap[item.requirement]"
                            :label="`Related Sub-Requirement ${index + 1}`"
                            dense required
                            :rules="formRules.valueRequiredRule"
                        ></v-autocomplete>
                      </v-col>
                    </v-row>
                  </v-col>
                  <v-col cols="2" class="d-flex justify-end" dense v-if="issueIndex === 1">
                    <v-btn
                        color="error"
                        x-small fab
                        @click="deleteRequirement(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row dense v-if="issueIndex === 1">
                  <v-col cols="12">
                    <v-btn color="accent"
                           @click="addRelated()"
                           small
                    >Additional Principle
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col cols="12">
                    <v-textarea
                        outlined required
                        label="Description"
                        v-model="issue.issueDescription"
                        :rules="formRules.valueRequiredRule"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-form>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn
              color="blue darken-1"
              type="submit"
              :disabled="!valid[1]"
              @click="submitMerge()"
          >
            Merge Issues
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="dialog=false"
          >
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              color="error"
              float-left
              @click="updateMergedIssue()"
          >
            Reset
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import {
  ethicalPrinciples,
  principlesRequirementsMap,
  requirementsSubrequirementsMap
} from '../constants/principlesAndRequirements'
import {createEmptyIssueDetails} from "./IssueDetailsCard";

export default {
  name: 'MergeDialog',
  props: ['issues'],
  data: () => ({
    dialog: false,
    valid: [false, false, false],
    formOptions: {
      issueType: [
        {
          label: 'Ethical Issue',
          value: 'ethical-issue'
        },
        {
          label: 'Flag',
          value: 'flag'
        }
      ],
      areas: ['Ethical', 'Social', 'Medical', 'Technical', 'Regulatory'],
    },
    formRules: {
      typeRules: [
        t => !!t || "Please select 'Ethical Issue' or 'Flag'"
      ],
      valueRequiredRule: [
        v => !!v || "Value required"
      ],
    },
    constant: {
      principlesRequirementsMap: principlesRequirementsMap,
      requirementsSubrequirementsMap: requirementsSubrequirementsMap,
      principles: ethicalPrinciples,
    },
    mergedIssue: createEmptyIssueDetails(),
    issue1: createEmptyIssueDetails(),
    issue2: createEmptyIssueDetails(),
  }),
  watch: {
    issues: function () {
      if (!this.issues.error) {
        this.issue1 = this.issues.issue1
        this.issue2 = this.issues.issue2
        this.updateMergedIssue()
      }
    }
  },
  methods: {
    submitMerge() {
      let eventData = {
        oldIssueIds: [this.issue1.id, this.issue2.id],
        mergedIssueData: this.mergedIssue
      }
      this.$emit('mergeSubmit', eventData)
      this.dialog = false
    },
    updateMergedIssue() {
      this.mergedIssue.areas = Array(...new Set(this.issue1.areas.concat(this.issue2.areas)))
      if (this.issue1.issueType === "flag" && this.issue2.issueType === "flag") {
        this.mergedIssue.issueType = "flag"
      } else {
        this.mergedIssue.issueType = "ethical-issue"
      }
      // the workaround with JSON.stringify is to make a set of objects
      this.mergedIssue.related = Array.from(
          new Set(
              this.issue1.related
                  .concat(this.issue2.related)
                  .map(JSON.stringify)
          )
      ).map(JSON.parse)
    },
    addRelated() {
      this.mergedIssue.related.push(this.createEmptyRelatedItem())
    },
    resetFormValues() {
      this.updateMergedIssue()
      // after reset form should not complain if values are missing (submit is not working anyways)
      this.$refs.issueForm.resetValidation()
    },
    deleteRequirement(index) {
      this.mergedIssue.related.splice(index, 1)
      if (this.mergedIssue.related.length === 0) {
        this.mergedIssue.related.push(this.createEmptyRelatedItem())
      }
    },
    createEmptyRelatedItem() {
      return {
        principle: null,
        requirement: null,
        subRequirement: null
      }
    }
  },
}
</script>