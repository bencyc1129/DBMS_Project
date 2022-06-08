<template>
  <div>
    <div class="row justify-content-center">
      <div class="dropdown col-auto">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
          {{ SQL }}
        </button>
        <ul class="dropdown-menu dropdown-menu-down" aria-labelledby="dropdownMenuButton1">
          <li v-for="(sql, i) in allSQL" :key="i">
            <a class="dropdown-item" href="#" @click="changeOp(sql)">{{ sql }}</a>
          </li>
        </ul>
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
  name: 'DropdownQuery',
  data() {
    return {
      SQL : "Choose the SQL",
      allSQL : [
        "SELECT userName, userPhone FROM user WHERE userId = 5;",
        "DELETE FROM user WHERE userName = 'Zac';",
        "INSERT INTO user (userName, userPhone) VALUES ('Pete', '0967123475');",
        "UPDATE user SET userName = 'Benny' WHERE userName = 'Ben';",
        "SELECT * FROM book WHERE bookLang IN ('jp', 'sv');",
        "SELECT * FROM book WHERE bookLang NOT IN ('jp', 'sv');",
        "SELECT * FROM library WHERE EXISTS (SELECT * FROM user WHERE userName = 'Pete');",
        "SELECT * FROM library WHERE NOT EXISTS (SELECT * FROM user WHERE userName = 'Pete');",
        "SELECT COUNT(bookIsbn) FROM book WHERE bookLang = 'jp';",
        "SELECT book_isbn, SUM(num) FROM collect GROUP BY book_isbn;",
        "SELECT MAX(point) FROM register;",
        "SELECT MIN(point) FROM register;",
        "SELECT AVG(point) FROM register;",
        "SELECT bookName, SUM(num) FROM (collect INNER JOIN book ON collect.book_isbn = book.bookIsbn) GROUP BY book_isbn HAVING SUM(num) > 10;",
      ],
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
        console.log(this.queryData, this.queryKey)
      }).catch(function (error) { 
        console.log(error)
      });
    },

    changeOp(SQL) {
      this.SQL = SQL;
    }
  },
}
</script>

<style>
.table-responsive {
    max-height:300px;
}
</style>