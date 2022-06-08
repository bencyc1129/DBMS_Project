<template>
  <div>
    <div class="row justify-content-center">
      <div class="col-auto w-50">
        <input type="text" class="form-control" v-bind:placeholder="SQL" v-model="SQL">
      </div>
      <div class="col-auto">
        <button @click="inputSQL" class="btn btn-primary">Query</button>
      </div>
    </div>
    <div class="container my-3 table-responsive">
      <table class="table table-striped table-bordered table-hover mx-auto">
        <thead>
          <tr>
            <th v-for="(keyName, i) in queryKey" :key="i"> {{ keyName }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in queryData" :key="i">
            <td v-for="(cell, j) in row" :key="j">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InputQuery',
  data() {
    return {
      SQL : "",
      queryData : [],
      queryKey : [],
    }
  },
  methods: {
    inputSQL() {
      this.axios.post('http://127.0.0.1:8000/inputSQL', {
        SQL : this.SQL
      }).then((res) => {
        this.queryData = res.data.data
        if (Object.keys(this.queryData).length != 0){
          this.queryKey = res.data.key
        }else{
          this.queryKey = []
        }
      }).catch(function (error) { 
        console.log(error)
      });
    },
  },
}
</script>

<style>
.table-responsive {
    max-height:300px;
}
</style>