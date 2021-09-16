<template>
  <v-row justify="center">
    <v-dialog
        v-model="dialog"
        max-width="800px"
    >
      <template v-slot:activator="{ on, attrs}">
        <v-btn
            color="success"
            dark
            v-bind="attrs"
            v-on="on"
        >
          Filter Issues
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Filter issues</span>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-row dense v-for="(item, index) in queries.related" :key="index">
              <v-col cols="10" dense>
                <v-row dense>
                  <v-col cols="4">
                    <v-autocomplete
                        v-model="item.principle"
                        :items="constant.principles"
                        :label="`Related Ethical Principle ${index + 1}`"
                        dense
                    ></v-autocomplete>
                  </v-col>
                  <v-col cols="4">
                    <v-autocomplete
                        v-model="item.requirement"
                        :items="constant.principlesRequirementsMap[item.principle]"
                        :label="`Related Key Requirement ${index + 1}`"
                        dense
                    ></v-autocomplete>
                  </v-col>
                  <v-col cols="4">
                    <v-autocomplete
                        v-model="item.subRequirement"
                        :items="constant.requirementsSubrequirementsMap[item.requirement]"
                        :label="`Related Sub-Requirement ${index + 1}`"
                        dense
                    ></v-autocomplete>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="2" class="d-flex justify-end" dense>
                <v-btn
                    color="error"
                    x-small fab
                    @click="deleteRelatedFilter(index)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12">
                <v-btn color="accent"
                       @click="addRelatedFilter()"
                       small
                >Additional Principle
                </v-btn>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="12">
                <v-text-field
                    outlined
                    clearable
                    label="Contains text (leave blank for all)"
                    v-model="queries.containedText"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
              color="blue darken-1"
              type="submit"
              @click="submitFilter()"
          >
            Filter
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="this.dialog=false"
          >
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              color="error"
              float-left
              @click="clearAllFilters()"
          >
            Clear All Filters
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
} from '@/constants/principlesAndRequirements'

function createEmptyRelatedItem() {
  return {
    principle: null,
    requirement: null,
    subRequirement: null
  }
}

export function createEmptyFilter() {
  return {
    containedText: null,
    related: [createEmptyRelatedItem()]
  }
}

export default {
  name: 'FilterDialog',
  data: () => ({
    dialog: false,
    constant: {
      principlesRequirementsMap: principlesRequirementsMap,
      requirementsSubrequirementsMap: requirementsSubrequirementsMap,
      principles: ethicalPrinciples,
    },
    queries: createEmptyFilter(),
  }),
  methods: {
    submitFilter() {
      this.$emit('filterSubmit', this.queries)
      this.dialog = false
    },
    clearAllFilters() {
      if (confirm("Reset all Filters?")) {
        this.queries.related = [createEmptyRelatedItem()]
        this.queries.containedText = null
        this.submitFilter()
      }
    },
    addRelatedFilter() {
      this.queries.related.push(createEmptyRelatedItem())
    },
    deleteRelatedFilter(index) {
      this.queries.related.splice(index, 1)
      if (this.queries.related.length === 0) {
        this.queries.related.push(createEmptyRelatedItem())
      }
    },
  },
}
</script>