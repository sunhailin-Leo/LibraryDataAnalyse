<template>
	<section class="chart-container">
		<el-row>
			<el-card class="box_card">
				<div id="brmonths" style="width:100%; height:400px;"></div>
			</el-card>
		</el-row>
		<el-row>
			<el-card class="box_card">
				<div id="brweeks" style="width:100%; height:400px;"></div>
			</el-card>
		</el-row>
		<el-row>
			<el-card class="box_card">
				<div id="brquantums" style="width:100%; height:400px;"></div>
			</el-card>
		</el-row>
	</section>
</template>
<script>
	import echarts from 'echarts'
	import { getBRMonthInfo, getBRWeekInfo, getBRQuantumInfo } from '../../api/api';

	export default {
		data() {
			return {
                brmonths: null,
				brweeks: null,
				brquantums: null
			}
		},
		methods: {
		    drawBRMonths() {
		        this.brmonths = echarts.init(document.getElementById('brmonths'));
		        //加载数据
				this.listLoading = true;
				getBRMonthInfo().then((res) => {
				    this.listLoading = false;
				    this.brmonths.setOption(res);
				})
			},
			drawBRWeeks() {
		        this.brweeks = echarts.init(document.getElementById('brweeks'));
		        //加载数据
				this.listLoading = true;
				getBRWeekInfo().then((res) => {
				    this.listLoading = false;
				    this.brweeks.setOption(res);
				})
			},
			drawBRQuantums() {
		        this.brquantums = echarts.init(document.getElementById('brquantums'));
		        //加载数据
				this.listLoading = true;
				getBRQuantumInfo().then((res) => {
				    this.listLoading = false;
				    this.brquantums.setOption(res);
				})
			}

		},
		mounted() {
			this.drawBRMonths();
			this.drawBRWeeks();
			this.drawBRQuantums();
		}
	};

</script>

<style scoped>
	.chart-container {
		margin-top: 20px;
		width: 100%;
		float: left;
	}
	.el-row {
		margin-bottom: 20px;
	}
</style>