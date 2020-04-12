<template>
  <div id="dashboard">
    <b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand href="#">Monte Carlo Simulator</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-button size="sm" class="my-2 my-sm-0" variant="primary">Simulate</b-button>
        </b-nav-form>

      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
    <b-container fluid v-if="ready" class="mt-2">
      <b-row>
        <b-col lg="12" md="12" sm="12"><hr /></b-col>
        <b-col lg="4" md="4" sm="12">
          <label class="tx-12">Choose Exchange:</label>
          <b-form-select class="tx-12" v-model="exchange" :options="exchanges" @change="changeExchange(exchange)"></b-form-select>
        </b-col>
         <b-col lg="4" md="4" sm="12">
          <label class="tx-12">Time Range</label>
            <b-form-select class="tx-12" v-model="range">
              <b-form-select-option v-for="x in ranges" :key="x.value" :value="x.value">{{ x.text }}</b-form-select-option>
            </b-form-select>
          </b-col>
         <b-col lg="4" md="4" sm="12">
          <label class="tx-12">Choose Stock</label>
          <basic-select
            :options="stocks"
            :selected-option="item"
            placeholder="select item"
            @select="onSelect"
            class="tx-12"
          >
          </basic-select>
        </b-col>
      </b-row>
      <b-row class="mt-4">
         <b-col lg="4" md="4" sm="12" v-if="portfolio.length > 0">
           <label class="tx-12">Portfolio</label>
           <p v-for="(x, index) in portfolio" :key="x.Symbol" class="tx-12">
            <strong>{{ x.Symbol }}</strong> | {{ x.Company_Name }}
            <i class="fa fa-times-circle float-right pointer" @click="removeStock(index)"></i>

            </p>
         </b-col>
          <b-col lg="8" md="8" sm="12" v-if="stock != null">
           <label class="tx-12">Selected Stock</label>
           <p>{{ stock.Company_Name }}</p>
           <highcharts :options="chartOptions"></highcharts>

         </b-col>
      </b-row>
        <!-- <pre>{{ view }}</pre> -->
    </b-container>
    <b-container  v-else>
      <p>loading...</p>
    </b-container>
  </div>
</template>

<script>

import { BasicSelect } from 'vue-search-select'

export default {
  name: 'HelloWorld',
  data() {
    return { 
      ready: false,
      view: null,
      exchange: "NASDAQ",
      currentExchange: null,
      stock: null,
      stocks: [],
      range: 'ytd',
      ranges: [
        {
          value: '1d',
          text: 'Today'
        },
        {
          value: '5d',
          text: 'Past 5 Days'
        },
        {
          value: '1mo',
          text: 'Past Month'
        },
        {
          value: '3mo',
          text: 'Past 3 Months'
        },
        {
          value: '6mo',
          text: 'Past 6 Months'
        },
        {
          value: 'ytd',
          text: 'Year to date'
        },
        {
          value: '1y',
          text: 'Past Year'
        },
        {
          value: '2y',
          text: 'Past 2 Years'
        },
        {
          value: '5y',
          text: 'Past 5 Years'
        },
        {
          value: '10y',
          text: 'Past 10 Years'
        }
      ],
      portfolio: [],
      searchText: '', 
      item: {
        value: '',
        text: ''
      },
      chartOptions: {
        zoomType: 'x',
        title: {
                text: ''
        },
        xAxis: {
                type: 'datetime'
        },
        yAxis: {
                title: {
                    text: 'Price'
                }
        },
        plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 2010
          }
        },
        series: []
      }

    }
  },
  components: {
    BasicSelect
  },
  mounted() {
    this.loadDashboard()
  },
  computed:{
    exchanges() {
      let x
      let A = []
      let exchanges = this.view.exchanges
      for(x in exchanges) {
        A.push(exchanges[x].name)
      }
      return A
    }
  },
  methods: {
    removeStock(index) {
      this.portfolio.splice(index, 1)
      if(this.portfolio.length < 1) {
        this.stock = null
        this.chartOptions.series = []
      }
    },
    onSelect (item) {
      this.$Progress.start()
      this.chartOptions.series = []
      let s       = item.value
      let stocks  = this.currentExchange.data
      this.item   = item
      this.axios.get('/api/stock/'+stocks[s].Symbol+'/'+this.range)
      .then(({ data }) => {  
        let x,
            open,
            close,
            series = { 'name' : stocks[s].Symbol, data:[] },
            d = JSON.parse(data)
            open  =  Object.entries(d.Open)
            close = Object.entries(d.Close)

        for(x in open) {
          open[x][0] = parseInt(open[x][0])
          close[x][0] = parseInt(close[x][0])
          series.data.push(open[x], close[x])
        }
        this.chartOptions.series.push(series)
        this.$Progress.finish()
      })
      .catch(function () {
        this.$Progress.fail()
      })
      this.stock  = stocks[s]
      this.portfolio.push(stocks[s])
    },
    reset () {
      this.item = {}
    },
     loadDashboard() {
        this.$Progress.start()
        this.axios.get('/api/dashboard')
          .then(({ data }) => { 
              this.view = data
              this.currentExchange = this.view.exchanges[0]
              let x
              let stocks = this.currentExchange.data
              for(x in stocks) {
                let input = { 'value': x, 'text': stocks[x].Symbol + ' ' + stocks[x].Company_Name }
                this.stocks.push(input)
              }
              this.ready = true
              this.$Progress.finish()
          })
          .catch(function () {
            this.$Progress.fail()
            alert('Error loading dashboard')
          })
      },
      changeExchange(exchange) {
        this.$Progress.start()
        let filter = this.view.exchanges.filter(item => item.name.includes(exchange))
        this.currentExchange = filter[0]
        let x
        let stocks = this.currentExchange.data
        for(x in stocks) {
          let input = { 'value': x, 'text': stocks[x].Symbol + ' ' + stocks[x].Company_Name }
          this.stocks.push(input)
        }
        this.$Progress.finish()
      },
      changeStock(index) {
        console.log(index)
        this.stock = this.currentExchange.data[index]
      }
  }
}
</script>

<style></style>
<!-- 
  SCRATCH BOARD
  <b-col lg="" md="" sm="">
 -->