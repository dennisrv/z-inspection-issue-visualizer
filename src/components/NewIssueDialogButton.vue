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
          New Ethical Issue / Flag
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Add new Ethical Issue / Flag</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="issueForm" v-model="valid">
            <v-row dense>
              <v-col cols="12" >
                <v-radio-group
                    v-model="formValues.issueType"
                    :rules="formRules.typeRules"
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
                    v-model="formValues.areas"
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
                    v-model="formValues.issueTitle"
                    :rules="formRules.valueRequiredRule"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row dense v-for="(item, index) in formValues.related" :key="index">
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
              <v-col cols="2" class="d-flex justify-end" dense>
                <v-btn
                    color="error"
                    x-small fab
                    @click="deleteRequirement(index)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12">
                <v-btn color="accent"
                       @click="addRelated()"
                       small
                >Additional Principle</v-btn>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12">
                <v-textarea
                    outlined required
                    label="Description"
                    v-model="formValues.issueDescription"
                    :rules="formRules.valueRequiredRule"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="resetFormValues();dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            type="submit"
            :disabled="!valid"
            @click="submitAction()"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import {ethicalPrinciples, principlesRequirementsMap, requirementsSubrequirementsMap} from '@/constants/principlesAndRequirements'

export default {
  name: 'NewIssueDialogButton',
  data: () => ({
    valid: false,
    constant: {
      principlesRequirementsMap: principlesRequirementsMap,
      requirementsSubrequirementsMap: requirementsSubrequirementsMap,
      principles: ethicalPrinciples,
    },
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
    initialFormValues: {
      issueType: null,
      numRelated: 1,
      areas: [],
      related: [
        {
          principle: null,
          requirement: null,
          subRequirement: null
        }
      ],
      issueTitle: null,
      issueDescription: null,
    },
    formRules: {
      typeRules: [
          t => !!t || "Please select 'Ethical Issue' or 'Flag'"
      ],
      valueRequiredRule: [
          v => !!v || "Value required"
      ],
    },
    formValues: {},
    dialog: false,
  }),
  computed: {

  },
  methods: {
    resetFormValues() {
      this.formValues = Object.assign({}, this.initialFormValues)
    },
    addRelated() {
      this.formValues.related.push(this.createEmptyRelatedItem())
    },
    submitAction() {
      this.dialog = false
      this.$emit('newIssue', this.formValues)
      this.resetFormValues()
    },
    deleteRequirement(index) {
      this.formValues.related.splice(index, 1)
      if (this.formValues.related.length === 0) {
        this.formValues.related.push(this.createEmptyRelatedItem())
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
  created() {
    this.resetFormValues()
  }
}
</script>