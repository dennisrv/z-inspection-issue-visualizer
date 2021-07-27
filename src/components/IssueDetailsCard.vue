<template>
  <v-card>
    <v-card-title v-if="title != null">
      <span class="text-h5">{{ title }}</span>
    </v-card-title>
    <v-card-text>
      <v-form ref="issueForm" v-model="valid">
        <v-row dense>
          <v-col cols="12">
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
            >Additional Principle
            </v-btn>
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
          @click="resetIssue()"
      >
        {{ resetButtonText }}
      </v-btn>
      <v-btn
          color="blue darken-1"
          type="submit"
          :disabled="!valid"
          @click="submitIssue()"
      >
        {{ submitButtonText }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import {
  ethicalPrinciples,
  principlesRequirementsMap,
  requirementsSubrequirementsMap
} from '@/constants/principlesAndRequirements'

export const createEmptyIssueDetails = function () {
  return {
    issueType: null,
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
  }
}

export default {
  name: 'IssueDetailsCard',
  props: {
    title: String,
    resetButtonText: String,
    submitButtonText: String,
    initialFormValues: {
      // if no form values are given, we use null for everything
      default: createEmptyIssueDetails
    }
  },
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
    formRules: {
      typeRules: [
        t => !!t || "Please select 'Ethical Issue' or 'Flag'"
      ],
      valueRequiredRule: [
        v => !!v || "Value required"
      ],
    },
    formValues: {}
  }),
  methods: {
    submitIssue() {
      this.dialog = false
      this.$emit('issueSubmit', this.formValues)
      this.resetFormValues()
    },
    resetIssue() {
      this.resetFormValues()
      this.$emit('issueReset')
    },
    addRelated() {
      this.formValues.related.push(this.createEmptyRelatedItem())
    },
    resetFormValues() {
      this.formValues = Object.assign({}, this.initialFormValues)
      // after reset form should not complain if values are missing (submit is not working anyways)
      this.$refs.issueForm.resetValidation()
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
  watch: {
    initialFormValues: function () {
      this.resetFormValues()
    }
  },
  mounted() {
    this.resetFormValues()
  }
}
</script>