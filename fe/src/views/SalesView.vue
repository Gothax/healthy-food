<template>
  <main class="p-6">
    <h1 class="text-2xl font-bold mb-4">Sales Page</h1>
    <br>
    <div class="mb-6">
      <label for="year-select" class="mr-2 font-bold">Year:</label>
      <select id="year-select" v-model="selectedYear">
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>

    <h2 class="text-2xl font-bold mb-4">연도별 총 판매 현황</h2>
    <div class="mb-6">
      <p>총 판매건수: {{ totalSalesCount }}</p>
      <p>총 판매금액: {{ totalSalesAmount }}</p>
    </div>

    <h2 class="text-2xl font-bold mb-4">월별 판매 현황</h2>
    <div class="chart-container" style="position: relative; height: 60vh; width: 80vw; margin-bottom: 20px; justify-content: center;">
      <h2 class="text-1xl font-bold mb-4">그래프</h2>
      <canvas id="salesChart"></canvas>
    </div>

    <br>
    <div>
      <h2 class="text-1xl font-bold mb-4">테이블</h2>
      <table class="min-w-full border-collapse border border-slate-400">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 border border-slate-300">월별</th>
            <th class="px-4 py-2 border border-slate-300">판매건수</th>
            <th class="px-4 py-2 border border-slate-300">판매금액</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="monthly in filteredSales" :key="monthly.month" class="bg-white even:bg-gray-50">
            <td class="px-4 py-2 border border-slate-300 text-center">{{ formatMonth(monthly.month) }}</td>
            <td class="px-4 py-2 border border-slate-300 text-right">{{ monthly.total_count }}</td>
            <td class="px-4 py-2 border border-slate-300 text-right">{{ monthly.total_sales }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import Chart from 'chart.js/auto';

export default {
  name: 'SalesView',
  data() {
    return {
      chart: null,
      sales: { monthly_sales: [] },
      selectedYear: new Date().getFullYear(),
      years: []
    };
  },
  async mounted() {
    await this.getSales();
    this.updateYears();
    this.createChart();
    this.updateChartData();
  },
  computed: {
    filteredSales() {
      if (this.sales && Array.isArray(this.sales.monthly_sales)) {
        return this.sales.monthly_sales.filter(data => moment(data.month).year() === this.selectedYear);
      }
      return [];
    },
    totalSalesCount() {
      return this.filteredSales.reduce((total, monthly) => total + monthly.total_count, 0);
    },
    totalSalesAmount() {
      return this.filteredSales.reduce((total, monthly) => total + monthly.total_sales, 0);
    }
  },
  watch: {
    selectedYear(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.updateChartData();
      }
    }
  },
  methods: {
    async getSales() {
      try {
        const response = await axios.get('api/seller/sales/');
        this.sales = response.data;
        console.log('Sales data:', this.sales);
        this.updateYears();
        this.updateChartData(); // Update chart data when sales data is fetched
      } catch (error) {
        console.error('Sales data fetch failed:', error);
      }
    },
    updateYears() {
      this.years = [...new Set(this.sales.monthly_sales.map(data => moment(data.month).year()))].sort();
      if (!this.years.includes(this.selectedYear)) {
        this.selectedYear = this.years[0] || new Date().getFullYear();
      }
    },
    createChart() {
      const ctx = document.getElementById('salesChart').getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [
            {
              label: '판매 금액',
              data: [],
              yAxisID: 'A',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            },
            {
              label: '판매 건수',
              data: [],
              yAxisID: 'B',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: '누적 판매 금액',
              data: [],
              type: 'line',
              yAxisID: 'A',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              fill: false
            }
          ]
        },
        options: {
          scales: {
            A: {
              type: 'linear',
              position: 'left',
            },
            B: {
              type: 'linear',
              position: 'right',
              grid: {
                drawOnChartArea: false,
              },
            }
          }
        }
      });
    },
    updateChartData() {
      if (this.chart) {
        this.chart.destroy(); // 기존 차트를 파괴
      }

      const ctx = document.getElementById('salesChart').getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.filteredSales.map(data => this.formatMonth(data.month)),
          datasets: [
            {
              label: '판매 금액',
              data: this.filteredSales.map(data => data.total_sales),
              yAxisID: 'A',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            },
            {
              label: '판매 건수',
              data: this.filteredSales.map(data => data.total_count),
              yAxisID: 'B',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: '누적 판매 금액',
              data: this.filteredSales.reduce((acc, cur, index) => {
                if (index === 0) return [cur.total_sales];
                acc.push(acc[index - 1] + cur.total_sales);
                return acc;
              }, []),
              type: 'line',
              yAxisID: 'A',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              fill: false
            }
          ]
        },
        options: {
          scales: {
            A: {
              type: 'linear',
              position: 'left',
            },
            B: {
              type: 'linear',
              position: 'right',
              grid: {
                drawOnChartArea: false,
              },
            }
          }
        }
      });
    },
    formatMonth(dateString) {
      return moment(dateString).format('MM');
    }
  }
};
</script>

<style scoped>
.table-container {
  overflow-x: auto;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
}
.table th {
  background-color: #f3f3f3;
}
.table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>